import pandas as pd
from pandas import DataFrame
from scraping import get_urls
import asyncio

def clean_scraping():

    scraping_data = get_urls(
        "https://www.admisionunt.info/padron",
        "container-main",
        "accordion-container"
        )
    
    raw_description: DataFrame = pd.DataFrame(
        scraping_data,
        columns=['periodo', 'modalidad', 'descripcion', 'link']
    )

    raw_description.to_csv("./get_data/raw_description.csv", index=False)

def read_urls(url, encoding, name_column, n_df):
    df = pd.read_csv(url, encoding=encoding, names={ name_column:0 })
    df['n_df'] = n_df
    return df

async def join_all_data(url, css_selector, encoding, name_column):

    urls = get_urls(url, css_selector)

    df = await asyncio.gather(
        *[asyncio.to_thread(read_urls, url, encoding, name_column, index) for index, url in enumerate(urls)]
    )

    final = pd.concat(df)

    final.to_csv('./get_data/raw_data.csv', index=False)
    return


clean_scraping()