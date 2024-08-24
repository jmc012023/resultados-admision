import re
import pandas as pd
from names.definitions import LinksDataColumnNames

def delete_white_spaces(raw_data):
    many_white_spaces = re.compile(r'\s+')
    one_white_space = ' '

    raw_data[LinksDataColumnNames.ALL_RESULT.value] = (
        raw_data[LinksDataColumnNames.ALL_RESULT.value]
        .str.replace(
            many_white_spaces,
            one_white_space,
            regex=True
            )
        .str.strip()
    )

    return raw_data

def divide(raw_data):
    fourt_digits = re.compile(r'^\d{4}')

    filter_by_digits = (
        raw_data
        [LinksDataColumnNames.ALL_RESULT.value]
        .str.contains(fourt_digits, regex=True)
    )

    raw_titles = (
        raw_data
        [~filter_by_digits]
    )

    raw_results = (
        raw_data
        [filter_by_digits]
    )

    return (raw_titles, raw_results)

def join_headers_with_body_results(headers, results):

    joined_data = pd.merge(
        results,
        headers,
        left_on=LinksDataColumnNames.N_DF.value,
        right_index=True
    )

    return joined_data

def join_results_with_twp_content(results, description):
    return (
        pd.merge(
            results,
            description,
            left_on=LinksDataColumnNames.N_DF.value,
            right_index=True
        )
    )