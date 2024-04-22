from get_data.scraping import get_urls
from get_data.appending_data import join_all_data, clean_scraping
import sys

async def generate_raw_data(url, id_selector, class_selector, encoding, name_column):

    scraping_data = get_urls(url, id_selector, class_selector)
    
    try:
        description = clean_scraping(scraping_data)
        results = await join_all_data(description, encoding, name_column)

    except:
        print("Error Transform to DataFrame is not possible")
        sys.exit(1)

    else:
        return (description, results)