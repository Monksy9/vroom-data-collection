import pandas as pd
import logging
from client import fetch_car_makes, fetch_listings
from parser import parse_listings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(test: bool = True):
    logging.info("🚘 Starting Autotrader scrape using ScraperAPI...")

    try:
        logging.info("Fetching car makes...")
        makes_data = fetch_car_makes()

        if not makes_data:
            logging.warning("No car makes found or failed to fetch.")
            return

        makes_df = pd.DataFrame(makes_data)
        logging.info(f"Found {len(makes_df)} car makes.")

    except Exception as e:
        logging.error(f"❌ Failed to fetch car makes: {e}", exc_info=True)
        return

    if test:
        makes_to_process = makes_df.head(2)  # Process only the first 2 makes in test mode
        logging.info(f"Running in test mode. Processing first {len(makes_to_process)} makes.")
    else:
        makes_to_process = makes_df
        logging.info(f"Processing all {len(makes_to_process)} makes found.")

    all_results = []

    # for index, make_row in makes_to_process.iterrows():
    #     make = make_row["value"]
    #     logging.info(f"--- Fetching models for Make: {make} ---")
    #     try:
    #         #here you would implement the fetch models function.
    #         models_data = fetch_models(make, vehicle_type = 'car')
    #         #models_df = pd.DataFrame(models_data)
    #         #models_to_process = models_df
    #         #for index, model_row in models_to_process.iterrows():
    #             #model = model_row['value']
    #             #logging.info(f"--- Fetching listings for Model: {model} ---")
    #             #listing_json = fetch_listings(make=make, model=model, vehicle_type='car')
    #             #listings_df = parse_listings(listing_json)
    #             #if not listings_df.empty:
    #                 #all_results.append(listings_df)
    #                 #logging.info(f"✅ {make} {model} - Found {len(listings_df)} results")
    #             #else:
    #                 #pass
    #     except Exception as e:
    #         logging.error(f"❌ Failed to fetch data for {make}: {e}", exc_info=True)

    if all_results:
        full_df = pd.concat(all_results, ignore_index=True)
        output_filename = f"autotrader_car_listings_{'test' if test else 'full'}.csv"
        try:
            full_df.to_csv(output_filename, index=False)
            logging.info(f"📦 Saved {len(full_df):,} rows to {output_filename}")
        except Exception as e:
            logging.error(f"Failed to save DataFrame to CSV: {e}")
    else:
        logging.warning("⚠️ No results gathered to save.")

    logging.info("🏁 Autotrader scrape finished.")

if __name__ == "__main__":
    main(test=True)