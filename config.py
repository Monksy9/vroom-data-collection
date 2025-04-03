# config.py
import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

SCRAPER_API_KEY = os.getenv("SCRAPER_API_KEY")
assert SCRAPER_API_KEY, "❌ SCRAPER_API_KEY not found in environment"

FACETS_ENDPOINT = "https://www.autotrader.co.uk/at-graphql?opname=SearchFormFacetsQuery" # Endpoint for fetching facets.
LISTINGS_ENDPOINT = "https://www.autotrader.co.uk/at-gateway?opname=SearchResultsFacetsWithGroupsQuery" #Endpoint for fetching listings.
DETAILS_ENDPOINT = "https://www.autotrader.co.uk/at-graphql?opname=VehicleDetailsQuery" #Endpoint for vehicle details.

SCRAPER_API_ENDPOINT = "https://api.scraperapi.com"

HEADERS = {
    "Content-Type": "application/json"
}

def get_scraperapi_url(target_url):
    """Constructs the ScraperAPI URL with the target URL encoded."""
    encoded_url = urllib.parse.quote(target_url)
    return f"{SCRAPER_API_ENDPOINT}?api_key={SCRAPER_API_KEY}&url={encoded_url}"