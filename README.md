# read-cloudflare-dns-records
This repository contains the script to read and print all the DNS records in the CloudFlare DNS zone.
Pre-requisistes:
1. Python3
1. python requests lib (`pip3 install requests`)

You need to have the following:
1. CloudFlare API token ([instructions](https://developers.cloudflare.com/fundamentals/api/get-started/create-token/))
1. CloudFlare zone_id (can be found in overvew page of your dns zone. Right bottom)
1. CloudFlare account_id (can be found in overvew page of your dns zone. Right bottom)

The following values have to be updated accordingly in the `get_cf_records.py` file
```python
zone_id = "zone_id"
auth_key = "auth_key"
account_id = "account_id"
```

The scipt can be executed as the following:
```bash
python3 get_cf_records.py
```
The scipt produces the json output that can be used as an input for the [terraform-aws-route53/records terrafrom module](https://github.com/terraform-aws-modules/terraform-aws-route53/tree/master/modules/records)
```json
  {
    "name": "example.com",
    "type": "A",
    "ttl": 300,
    "records": [
      "10.10.10.10"
    ]
  },
```
The output should be saved into the file. Next the contenxts can be read with terrafrom/terragrunt and specified as inputs to the [terraform-aws-route53/records terrafrom module](https://github.com/terraform-aws-modules/terraform-aws-route53/tree/master/modules/records)
```terraform
    records_jsonencoded = jsondecode(file("dns_records.json"))
```

The following is the analogue with `curl`
```bash
zone_id="<..zone_id..>"
auth_key="<..auth_key..>"
account_id="<..account_id..>"

curl -X GET "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records" \
    -H "Authorization: Bearer $auth_key" \
    -H "X-Auth-Account-Id: $account_id" \
    -H "Content-Type: application/json"
```