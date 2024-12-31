import os
from dotenv import load_dotenv
from scrapingbee import ScrapingBeeClient
from requests import codes

def fetch_url_scrapingbee(url):
    load_dotenv()
    api_key = os.getenv('SCRAPINGBEE_API_KEY')

    client = ScrapingBeeClient(api_key)
    response = client.get(url)

    if response.status_code == codes.ok:
        print(f"{url} fetched successfully.")
        return response.text, None
    else:
        print(f"Failed to fetch {url}. Status code: {response.status_code}")
        return None, response.status_code
