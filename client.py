# client.py

import requests
from config import FACETS_ENDPOINT, LISTINGS_ENDPOINT, HEADERS, get_scraperapi_url
import json

def fetch_car_makes() -> list:
    """Fetches all car makes using ScraperAPI."""
    vehicle_type = "car"  # Set vehicle type to car
    graphql_payload = build_makes_query(vehicle_type)
    api_url = get_scraperapi_url(FACETS_ENDPOINT)

    try:
        response = requests.post(
            api_url,
            json=graphql_payload,
            headers=HEADERS,
            timeout=60,
        )
        response.raise_for_status() 
        data = response.json()
        makes = parse_makes(data)
        return makes
    except requests.exceptions.RequestException as e:
        print(f"Error fetching car makes: {e}")
        return []
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing car makes: {e}")
        return [] 

def build_makes_query(vehicle_type: str) -> list:
    """Builds the GraphQL query to fetch car makes."""
    payload_string = '[{"operationName":"SearchFormFacetsQuery","variables":{"advertQuery":{"advertisingLocations":["at_cars"],"advertClassification":["standard"],"postcode":"se58db","homeDeliveryAdverts":"include"},"facets":["make"]},"query":"query SearchFormFacetsQuery($advertQuery: AdvertQuery!, $facets: [SearchFacetName]) {\\n  search {\\n    adverts(advertQuery: $advertQuery) {\\n      facets(facets: $facets) {\\n        name\\n        values {\\n          name\\n          value\\n          count\\n          selected\\n          __typename\\n        }\\n        __typename\\n      }\\n      __typename\\n    }\\n    __typename\\n  }\\n}\\n"}]'.replace(
        "at_cars", f"at_{vehicle_type}s"
    )
    return json.loads(payload_string)

def parse_makes(data: dict) -> list[dict]:
    """Parses the API response to extract car makes."""
    facets = data[0]["data"]["search"]["adverts"]["facets"]
    makes_data = [f for f in facets if f["name"] == "make"][0]["values"]
    makes = [
        {"value": m["value"], "label": f"{m['value']} ({m['count']:,})"}
        for m in makes_data
    ]
    return makes

def fetch_listings(make: str, model: str, vehicle_type: str) -> list:
    """Fetches search results/listings for a given make, model, and vehicle type via ScraperAPI."""
    graphql_payload = build_results_query(make, model, vehicle_type)
    api_url = get_scraperapi_url(LISTINGS_ENDPOINT)

    try:
        response = requests.post(
            api_url,
            json=graphql_payload,
            headers=HEADERS,
            timeout=5,
        )
        response.raise_for_status()  # Check for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching listings: {e}")
        return []
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error parsing listings: {e}")
        return []

def build_results_query(make: str, model: str, vehicle_type: str) -> list:
    # NOTE: The original query uses 'filters' which might be slightly different
    # from the 'advertQuery' structure in facets. Adjust if needed based on API observation.
    # This structure below seems more aligned with typical AutoTrader search result queries.
    return [
        {
            "operationName": "SearchResultsQuery",
            "variables": {
                "searchParameters": { # Common structure seen in AutoTrader requests
                    "make": [make],
                    "model": [model],
                    "postcode": "SE5 8DB", # Consider making configurable
                    "advertisingLocations": [f"at_{vehicle_type}s"],
                    "pageNumber": 1, # Add pagination support if needed
                    "pageSize": 100 # Fetch more results per page if desired/allowed
                },
                "sort": "relevance" # Or "price-asc", "price-desc", etc.
            },
            "query": """
                query SearchResultsQuery($searchParameters: SearchParametersInput, $sort: AdvertSortOrder) {
                    search(searchParameters: $searchParameters) {
                        results {
                            adverts {
                                advertId # Often the unique ID
                                vehicle {
                                    make
                                    model
                                    derivative # More specific trim/version
                                    year # Year of manufacture
                                }
                                pricing {
                                    advertPrice {
                                        displayPrice # Formatted price string (e.g., £10,000)
                                        # rawPrice # Might contain numeric price
                                    }
                                }
                                advertUrls { # Check the exact structure via browser dev tools
                                    canonical # Usually the main link
                                }
                                # Add other fields you need: mileage, images, specs etc.
                            }
                            pagination {
                                pageNumber
                                pageSize
                                totalPages
                                totalResults
                            }
                        }
                    }
                }
            """
        }
    ]