import pandas as pd
import re

class RawData:

    @staticmethod
    def delete_white_spaces(raw_data):
        many_white_spaces = re.compile(r'\s+')
        one_white_space = ' '

        raw_data['main'] = (
            raw_data['main']
            .str.replace(
                many_white_spaces,
                one_white_space,
                regex=True
                )
            .str.strip()
        )

        return raw_data

    @staticmethod
    def divide(raw_data):
        fourt_digits = re.compile(r'^\d{4}')

        filter_by_digits = (
            raw_data
            ['main']
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


def handle(df):
    raw_data = RawData.delete_white_spaces(df)
    raw_titles, raw_results = RawData.divide(raw_data)
    return raw_titles, raw_results