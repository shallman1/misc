### 1\. `/dga` - Detect DGAs

**Usage:** `/dga <domain>`

-   **Purpose:** Detects Domain Generation Algorithm (DGA) patterns in subdomains of the provided domain.
-   **Parameters:**
    -   `domain` - The domain to analyze.
-   **Output:** Lists suspected DGA domains and includes a button to view paginated results if multiple DGAs are found.

* * * * *

### 2\. `/dnscount` - DNS Count Analysis

**Usage:** `/dnscount <domain>` or `/dnscount -plot <domain>`

-   **Purpose:** Provides a count of DNS records for the domain and its subdomains. Optionally, generates a timeline plot.
-   **Parameters:**
    -   `domain` - The domain to analyze.
    -   `-plot` (optional) - Generates a timeline of DNS records if specified.
-   **Output:** A bar chart or timeline plot showing DNS record counts.

* * * * *

### 3\. `/dns_history` - DNS History Analysis

**Usage:** `/dns_history <domain_or_ip1>,<domain_or_ip2>,...`

-   **Purpose:** Checks for shared historical infrastructure between provided domains/IPs based on DNS history.
-   **Parameters:**
    -   `domain_or_ip1, domain_or_ip2, ...` - A comma-separated list of domains or IP addresses to analyze.
-   **Output:** Lists overlapping IPs and hostnames shared among the provided domains or IPs.

* * * * *


### 4\. `/mx_security` - Email Security Check

**Usage:** `/mx_security <domain>`

-   **Purpose:** Checks the domain's email security configuration, focusing on SPF, DKIM, and DMARC records.
-   **Parameters:**
    -   `domain` - The domain to analyze.
-   **Output:** A report of SPF, DKIM, and DMARC records found for the domain, detailing each record's first and last seen dates and security settings.

* * * * *

### 5\. `/subdomains` - Subdomain Enumeration

**Usage:** `/subdomains <domain1,domain2,...>`

-   **Purpose:** Identifies subdomains of the provided domains.
-   **Parameters:**
    -   `domain1, domain2, ...` - A comma-separated list of domains to analyze.
-   **Output:** A hierarchical, paginated list of subdomains with indentation to indicate structure.

* * * * *

### 6\. `/supplychain` - Supply Chain Analysis

**Usage:** `/supplychain <domain1,domain2,...>`

-   **Purpose:** Analyzes subdomains for brand terms, helping identify supply chain-related domains.
-   **Parameters:**
    -   `domain1, domain2, ...` - A comma-separated list of domains to analyze.
-   **Output:** A list of subdomains containing known brand terms, indicating the last time each subdomain was observed.

* * * * *

### 7\. `/timeline` - DNS Record Timeline

**Usage:** `/timeline <domain>`

-   **Purpose:** Visualizes changes in A/AAAA records for a domain over time.
-   **Parameters:**
    -   `domain` - The domain to analyze.
-   **Output:** A timeline image showing DNS record changes, uploaded to Slack.

* * * * *

### 8\. `/track` - Domain Tracking

**Usage:** `/track <search_hash>`

-   **Purpose:** Initiates tracking for infrastructure or domain patterns based on a search hash.
-   **Parameters:**
    -   `search_hash` - The search hash identifier to track.
-   **Output:** A CSV file with tracking results, stored locally and a Slack notification for any significant changes in the tracked data. This will be delivered via a private message from slack_bot. It currently checks for changes once per day.
