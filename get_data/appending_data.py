import pandas as pd
from get_data.scraping_data import get_urls
import asyncio

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
