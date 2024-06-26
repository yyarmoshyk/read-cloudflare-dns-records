import json
import requests

cloudflare_api = "https://api.cloudflare.com/client/v4/"
zone_id = "zone_id"
auth_key = "auth_key"
account_id = "account_id"

headers = {
    'Authorization': 'Bearer '+auth_key,
    'X-Auth-Account-Id': account_id,
    'Content-Type': 'application/json'
}

cloudflare_dns = f"{cloudflare_api}zones/{zone_id}/dns_records"
response = requests.get(cloudflare_dns, headers=headers)

if response.status_code == 200:
    dns_records = response.json()["result"]
    filtered_dns_records = []

    # Extract the name, type, and content of each DNS record
    for record in dns_records:
        filtered_record = {
            "name": record['name'],
            "type": record['type'],
            "ttl": record['ttl'],
        }
        
        # Remove \" from the record values
        if isinstance(record['content'], str) and record['content'].startswith("\"") and record['content'].endswith("\""):
            content = json.loads(record['content'])
        else:
            content = record['content']


        # Include priority for SRV and MX records into the result
        if record['type'] in ['SRV', 'MX']:
            filtered_record["records"] = [record['priority'], content]
        else:
            filtered_record["records"] = [content]

        filtered_dns_records.append(filtered_record)
    
    # Convert the list to JSON and print it
    print(json.dumps(filtered_dns_records, indent=2))

else:
    print("status_code " + str(response.status_code))    

