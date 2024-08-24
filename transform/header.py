import numpy as np
import pandas as pd
from pandas import Series
import re
from names.definitions import LinksDataColumnNames, ResultColumnNames

CN_N_ROWS = 'n_rows'
CN_SEQUENCE = 'sequence'
CN_FIRST = 'first'
CN_SECOND = 'second'
CN_THIRD = 'third'
CN_FOURTH = 'fourth'
        
def replace_repeated_pattern(raw_headers):
    repeated_pattern = re.compile(r'Pag\.\s\d+')
    empty_string = ''

    return (
        raw_headers[LinksDataColumnNames.ALL_RESULT.value]
        .str.replace(
            repeated_pattern,
            empty_string,
            regex=True
        )
        .str.rstrip()
    )
    
def delete_repeated_pattern(raw_headers):
    return (
        raw_headers
        .drop_duplicates([LinksDataColumnNames.ALL_RESULT.value, LinksDataColumnNames.N_DF.value])
    )
    
def extract_rows_before_sign(grouped_titles):
    equal_sign = "="

    filter_by_equal_sign = (
        grouped_titles
        [LinksDataColumnNames.ALL_RESULT.value]
        .str.startswith(equal_sign)
    )
    
    position_equal_sign_row = (
        grouped_titles
        [filter_by_equal_sign]
        .index
        [0]
    )

    return (
        grouped_titles
        .loc[:position_equal_sign_row - 1]
    )
    
def get_rows_before_sing(raw_headers):

    headers = map(lambda group: extract_rows_before_sign(group[1]),
                    raw_headers.groupby(LinksDataColumnNames.N_DF.value))
    
    filtered_headers = pd.concat(headers)

    return filtered_headers
    
def filter_rows(raw_headers):
    raw_headers.loc[:, LinksDataColumnNames.ALL_RESULT.value] = replace_repeated_pattern(raw_headers)
    raw_headers = delete_repeated_pattern(raw_headers)
    filtered_headers = get_rows_before_sing(raw_headers)

    return filtered_headers
    
def count_number_rows_per_group(filtered_headers):
    name = [CN_N_ROWS]

    n_rows_per_group = filtered_headers.groupby(LinksDataColumnNames.N_DF.value).count()
    n_rows_per_group.columns = name

    return n_rows_per_group
    
def join_headers_with_number_rows(headers, number_rows):
    joined_headers = (
        pd.merge(
            headers,
            number_rows,
            left_on=LinksDataColumnNames.N_DF.value,
            right_on=LinksDataColumnNames.N_DF.value
        )
    )
    return joined_headers
    
def add_sequence(grouped_titles):
    max_value = grouped_titles[CN_N_ROWS].max()
    grouped_titles[CN_SEQUENCE] = range(max_value)

    return grouped_titles
    
def generate_sequence(joined_headers):
    sequence = map(lambda group: add_sequence(group[1]),
                    joined_headers.groupby(LinksDataColumnNames.N_DF.value))
    
    sequence_headers = pd.concat(sequence)

    return sequence_headers
    
def generate_titles_with_sequence(joined_titles):
    titles_with_sequence = generate_sequence(joined_titles)
    return titles_with_sequence

def unstack_titles(titles_sequence):
    return (
        titles_sequence
        .loc[:, [LinksDataColumnNames.N_DF.value, CN_SEQUENCE, LinksDataColumnNames.ALL_RESULT.value]]
        .set_index([LinksDataColumnNames.N_DF.value, CN_SEQUENCE])
        .unstack()
        .droplevel([CN_SEQUENCE], axis=1)
    )
    
def generate_unstacked_headers(raw_headers):
    filtered = filter_rows(raw_headers)
    rows = count_number_rows_per_group(filtered)
    joined_headers = join_headers_with_number_rows(filtered, rows)
    headers_sequence = generate_sequence(joined_headers)
    unstacked_headers = unstack_titles(headers_sequence)

    column_names = [CN_FIRST, CN_SECOND, CN_THIRD, CN_FOURTH]
    # la columna first posiblemente no se use

    unstacked_headers.columns = column_names

    return unstacked_headers

def get_date(titles, column_name):
    valid_date = re.compile(r'(\d\d/\d\d/\d+)')

    return (
        titles
        [column_name]
        .str.extract(valid_date)
        [0]
    )

def change_to_date_format(dates: Series):

    return (
        pd.to_datetime(
            dates,
            format="%d/%m/%Y"
        )
    )
    
def handle_columns(titles, *names):

    _, second, third, _ = names

    second_date = get_date(titles, second)
    third_date = get_date(titles, third)

    empty_string = ''

    dates: Series = (
        second_date
        .str.cat(third_date, na_rep=empty_string)
        .replace(empty_string, np.nan, regex=False)
    )

    dates = change_to_date_format(dates)
    dates.name = ResultColumnNames.DATE.value

    return dates
    
def headers_to_columns(raw_headers):
    unstacked_headers = generate_unstacked_headers(raw_headers)
    date_column = handle_columns(
        unstacked_headers,
        CN_FIRST,
        CN_SECOND,
        CN_THIRD,
        CN_FOURTH
    )
    
    return date_column