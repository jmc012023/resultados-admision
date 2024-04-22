import pandas as pd
from pandas import DataFrame
from get_data.cleaning import clean_data
import asyncio

def clean_scraping(data_scraping: list[tuple[str, str, str, str]]):

    raw_description: DataFrame = pd.DataFrame(
        data_scraping,
        columns=['periodo', 'tipo_exam', 'descripcion', 'link']
    )

    raw_description.to_csv("./get_data/raw_description.csv", index=False)

    description = clean_data(raw_description)

    return description

def read_urls(url, encoding, name_column, n_df):
    df = pd.read_csv(url, encoding=encoding, names={ name_column:0 })
    df['n_df'] = n_df
    return df

async def join_all_data(description: DataFrame, encoding: str, name_column: str):

    df = await asyncio.gather(
        *[asyncio.to_thread(read_urls, link, encoding, name_column, index) for index, link in enumerate(description['link'])]
    )

    final = pd.concat(df)

    final = final.reset_index().drop(['index'], axis=1)

    return final