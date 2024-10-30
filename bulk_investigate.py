import requests
import json

# Configuration
API_URL = "https://api.domaintools.com/v1/iris-investigate/"
API_USERNAME = "INSERT_API_USERNAME_HERE"  # Replace with your actual API username
API_KEY = "INSERT_API_KEY_HERE"  # Replace with your actual API key
BATCH_SIZE = 100  # Batch size limit as specified
DOMAIN_FILE = "domains.txt"  # File containing the list of domains
OUTPUT_FILE = "bulk_investigate_data.json"  # Output file

def load_domains(filename):
    """Load domains from a file, one per line."""
    with open(filename, "r", encoding="utf-8") as file:
        domains = [line.strip() for line in file if line.strip()]
    return domains

def batch_domains(domains, batch_size):
    """Split domains into batches of specified size."""
    for i in range(0, len(domains), batch_size):
        yield domains[i:i + batch_size]

def lookup_domains(batch):
    """Perform a POST request to the Iris Investigate API with a batch of up to 100 domains."""
    domain_list = ",".join(batch)
    response = requests.post(API_URL, data={
        "api_username": API_USERNAME,
        "api_key": API_KEY,
        "domain": domain_list
    })
    
    if response.status_code == 200:
        return response.json()  # Return JSON response for each batch
    else:
        print(f"Error for domains {domain_list}: {response.status_code} {response.text}")
        return None

def main():
    domains = load_domains(DOMAIN_FILE)
    results = []  # List to store all batch results

    for batch in batch_domains(domains, BATCH_SIZE):
        batch_result = lookup_domains(batch)
        if batch_result:
            results.append(batch_result)  # Add successful batch results to the list

    # Save all results to a JSON file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=4)

    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
