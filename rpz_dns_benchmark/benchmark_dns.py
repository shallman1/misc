# -*- coding: utf-8 -*-
"""
DNS resolution benchmark against a specific Unbound server.

Examples:
  py benchmark_dns.py --server 127.0.0.1 --port 53 --outfile rpz_on.csv --label rpz_on
  py benchmark_dns.py --server 127.0.0.1 --port 53 --outfile rpz_off.csv --label rpz_off
"""

import argparse
import csv
from datetime import datetime, timezone
from time import perf_counter_ns
import dns.exception
import dns.rcode
import dns.resolver

def idna_ascii(name: str) -> str:
    """Convert unicode domain to ASCII punycode if needed."""
    try:
        return name.encode("idna").decode("ascii")
    except Exception:
        return name

def make_resolver(server: str, port: int, timeout: float) -> dns.resolver.Resolver:
    r = dns.resolver.Resolver(configure=False)  # ignore OS resolver config
    r.nameservers = [server]
    r.port = int(port)
    r.timeout = float(timeout)   # per-try timeout (seconds)
    r.lifetime = float(timeout)  # overall lifetime (seconds)
    r.use_search_by_default = False
    return r

def resolve_once(resolver: dns.resolver.Resolver, domain: str, qtype: str) -> dict:
    """Resolve one (domain, qtype), timing in ms; record errors too."""
    raw = domain.strip()
    if not raw or raw.startswith("#"):
        return {}

    qname = idna_ascii(raw)
    if not qname.endswith("."):
        qname += "."

    ts_start = datetime.now(timezone.utc)
    start_ns = perf_counter_ns()

    status = "OK"
    rcode_text = ""
    answers_text = ""
    answer_count = 0
    error_text = ""

    try:
        ans = resolver.resolve(qname, qtype, raise_on_no_answer=True)
        rcode_text = dns.rcode.to_text(ans.response.rcode())
        if ans.rrset is not None:
            answers_text = ";".join(r.to_text() for r in ans)
            answer_count = len(ans)
        else:
            status = "NOANSWER"
    except dns.resolver.NXDOMAIN as e:
        status = "NXDOMAIN"
        # fill rcode if response present, else fall back to status
        rcode_text = getattr(getattr(e, "response", None), "rcode", lambda: None)()
        rcode_text = dns.rcode.to_text(rcode_text) if rcode_text is not None else status
        error_text = str(e)
    except (dns.resolver.LifetimeTimeout, dns.exception.Timeout) as e:
        status = "TIMEOUT"
        error_text = str(e)
    except dns.resolver.NoAnswer as e:
        status = "NOANSWER"
        error_text = str(e)
    except dns.resolver.NoNameservers as e:
        status = "NONAMESERVERS"
        error_text = str(e)
    except dns.exception.DNSException as e:
        status = e.__class__.__name__.upper()
        error_text = str(e)

    end_ns = perf_counter_ns()
    ts_end = datetime.now(timezone.utc)

    elapsed_ms = (end_ns - start_ns) / 1_000_000.0  # ns -> ms

    return {
        "timestamp_start_utc": ts_start.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "timestamp_end_utc": ts_end.isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "domain": qname,
        "qtype": qtype,
        "elapsed_ms": f"{elapsed_ms:.3f}",
        "status": status,
        "rcode": rcode_text or status,
        "answer_count": answer_count,
        "answers": answers_text,
        "error": error_text,  
    }

def load_domains(path: str) -> list[str]:
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            items.append(line)
    return items

def main():
    ap = argparse.ArgumentParser(description="Benchmark DNS resolution times using a specific Unbound server.")
    ap.add_argument("--server", default="127.0.0.1", help="Unbound DNS server IP (default: 127.0.0.1)")
    ap.add_argument("--port", type=int, default=53, help="Unbound DNS server port (default: 53)")
    ap.add_argument("--timeout", type=float, default=3.0, help="Timeout/lifetime in seconds per query (default: 3.0)")
    ap.add_argument("--qtypes", nargs="+", default=["A"], help="Record types to query (e.g., A AAAA)")
    ap.add_argument("--domains", default="domains.txt", help="Input file with FQDNs (default: domains.txt)")
    ap.add_argument("--outfile", required=True, help="Output CSV path")
    ap.add_argument("--label", default="", help="Run label to embed in CSV (e.g., rpz_on or rpz_off)")
    args = ap.parse_args()

    resolver = make_resolver(args.server, args.port, args.timeout)
    domains = load_domains(args.domains)

    # Include every key we write, including 'error'
    fields = [
        "run_label", "timestamp_start_utc", "timestamp_end_utc",
        "domain", "qtype", "elapsed_ms", "status", "rcode",
        "answer_count", "answers", "error",
        "server", "port", "timeout_s"
    ]

    rows_written = 0
    with open(args.outfile, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for d in domains:
            for qt in args.qtypes:
                result = resolve_once(resolver, d, qt)
                if not result:
                    continue
                result["run_label"] = args.label
                result["server"] = args.server
                result["port"] = args.port
                result["timeout_s"] = args.timeout
                w.writerow(result)
                rows_written += 1

    print(f"Wrote {rows_written} rows to {args.outfile}")

if __name__ == "__main__":
    main()
