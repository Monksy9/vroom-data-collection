# parser.py
import pandas as pd
import logging

def parse_facets(raw_json: list) -> pd.DataFrame:
    """Parses the JSON response containing search facets."""
    output = []
    try:
        facets = raw_json[0].get("data", {}).get("search", {}).get("adverts", {}).get("facets", [])
        if not facets:
            logging.warning("No facets found in the response JSON.")
            return pd.DataFrame(output)

        for facet in facets:
            name = facet.get("name")
            values = facet.get("values", [])
            if not name or not values:
                continue 

            for value_data in values:
                output.append({
                    "facet": name,
                    "label": value_data.get("name"),
                    "value": value_data.get("value"),
                    "count": value_data.get("count"),
                    "selected": value_data.get("selected")
                })
    except (AttributeError, TypeError, IndexError, KeyError) as e:
        logging.error(f"Error parsing facets JSON: {e} - JSON structure might be unexpected.")
        logging.debug(f"Raw JSON causing error: {raw_json}") # Log raw JSON for debugging if needed
    return pd.DataFrame(output)


def parse_listings(raw_json: list) -> pd.DataFrame:
    """Parses the JSON response containing search results/listings."""
    results_list = []
    try:
        search_results = raw_json[0].get("data", {}).get("search", {}).get("results", {})
        adverts = search_results.get("adverts", [])

        if not adverts:
            logging.info("No listings ('adverts') found in the current response page.")
            return pd.DataFrame(results_list)

        for advert in adverts:
            vehicle = advert.get("vehicle", {})
            pricing = advert.get("pricing", {}).get("advertPrice", {})
            urls = advert.get("advertUrls", {})

            results_list.append({
                "id": advert.get("advertId"),
                "make": vehicle.get("make"),
                "model": vehicle.get("model"),
                "derivative": vehicle.get("derivative"),
                "year": vehicle.get("year"),
                "price": pricing.get("displayPrice"), 
                "advert_link": urls.get("canonical"),
            })

    except (AttributeError, TypeError, IndexError, KeyError) as e:
        logging.error(f"Error parsing listings JSON: {e} - JSON structure might be unexpected.")
        logging.debug(f"Raw JSON causing error: {raw_json}")

    return pd.DataFrame(results_list)