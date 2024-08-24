import pandas as pd
from pandas import Series
from names.definitions import LinksDataColumnNames
import asyncio

ENCODING = "ISO-8859-1"

def create_frame_by_link(url, n_df):
    frame_link_content = pd.read_csv(url, encoding=ENCODING, names={ LinksDataColumnNames.ALL_RESULT.value:0 })
    frame_link_content[LinksDataColumnNames.N_DF.value] = n_df
    return frame_link_content

async def join_data_links(link_column: Series):

    content_links = await asyncio.gather(
        *[asyncio.to_thread(create_frame_by_link, link, index) for index, link in enumerate(link_column)]
    )

    frame_content_links = pd.concat(content_links)
    frame_content_links = frame_content_links.reset_index().drop(['index'], axis=1)

    return frame_content_links