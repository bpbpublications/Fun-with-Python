import requests

MAIN_URL = "https://beta.virusbay.io/sample/data"

response = requests.get(MAIN_URL)
if response.status_code == 200:
    data = response.json()
    with open("virusbay.bin", "w", encoding="utf8") as f:
        for item in data["recent"]:
            virus_md5 = item["md5"]
            details_url = f"https://beta.virusbay.io/sample/data/{virus_md5}"
            details_response = requests.get(details_url)
            if details_response.status_code == 200:
                data = details_response.json()
                if "sha256" in data:
                    f.write(f"{data['sha256']}\n")
