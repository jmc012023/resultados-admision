from abc import ABC
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import re

class HandleRawTitles:
    def __init__(self, raw_titles):
        self._raw_titles = raw_titles
        
    def _replace_repeated_pattern(self):
        repeated_pattern = re.compile(r'Pag\.\s\d+')
        empty_string = ''

        return (
            self._raw_titles['main']
            .str.replace(
                repeated_pattern,
                empty_string,
                regex=True
            )
            .str.rstrip()
        )
    
    def _delete_repeated_pattern(self, raw_titles):
        return (
            raw_titles
            .drop_duplicates(['main', 'n_df'])
        )
    
    def _extract_rows_before_sign(self, grouped_titles):
        equal_sign = "="

        filter_by_equal_sign = (
            grouped_titles
            ['main']
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
    
    def _get_rows_before_sing(self, raw_titles):

        titles = map(lambda group: self._extract_rows_before_sign(group[1]),
                     raw_titles.groupby('n_df'))
        
        filtered_titles = pd.concat(titles)

        return filtered_titles
    
    def _filter_rows(self):
        self._raw_titles.loc[:, 'main'] = self._replace_repeated_pattern()
        self._raw_titles = self._delete_repeated_pattern(self._raw_titles)

        filtered_titles = self._get_rows_before_sing(self._raw_titles)

        return filtered_titles
    
    def _count_number_rows_per_group(self, filtered_titles):
        name = ['n_rows']

        n_rows_per_group = filtered_titles.groupby("n_df").count()
        n_rows_per_group.columns = name

        return n_rows_per_group
    
    def _join_titles_with_number_rows(self, titles, number_rows):
        joined_titles = (
            pd.merge(
                titles,
                number_rows,
                left_on='n_df',
                right_on='n_df'
            )
        )
        return joined_titles
    
    def _add_sequence(self, grouped_titles):
        max_value = grouped_titles['n_rows'].max()
        grouped_titles['sequence'] = range(max_value)

        return grouped_titles
    
    def _generate_sequence(self, joined_titles):
        sequence = map(lambda group: self._add_sequence(group[1]),
                       joined_titles.groupby('n_df'))
        
        sequence_titles = pd.concat(sequence)

        return sequence_titles
    
    def _generate_titles_with_sequence(self, joined_titles):
        titles_with_sequence = self._generate_sequence(joined_titles)
        return titles_with_sequence
    
    def _unstack_titles(self, titles_sequence):
        return (
            titles_sequence
            .loc[:, ['n_df', 'sequence', 'main']]
            .set_index(['n_df', 'sequence'])
            .unstack()
            .droplevel(['sequence'], axis=1)
        )
    
    def generate_unstacked_titles(self):
        filtered = self._filter_rows()
        rows = self._count_number_rows_per_group(filtered)
        joined_titles = self._join_titles_with_number_rows(filtered, rows)
        titles_sequence = self._generate_sequence(joined_titles)
        unstacked_titles = self._unstack_titles(titles_sequence)

        column_names = ['first', 'second', 'third', 'fourth']
        # la columna first posiblemente no se use

        unstacked_titles.columns = column_names

        return unstacked_titles

class GetDataTitle(ABC):

    @staticmethod
    def get_date(titles, column_name):
        valid_date = re.compile(r'(\d\d/\d\d/\d+)')

        return (
            titles
            [column_name]
            .str.extract(valid_date)
            [0]
        )
    
class CleanSecondTitle(GetDataTitle):
    ...

class CleanThirdTitle(GetDataTitle):
    ...

class CleanFourthTitle(GetDataTitle):
    ...

class HandleTitles:

    @staticmethod
    def _change_to_date_format(dates: Series):

        return (
            pd.to_datetime(
                dates,
                format="%d/%m/%Y"
            )
        )
    
    @staticmethod
    def _handle_columns(titles, *names):

        first, second, third, fourth = names

        second_date = CleanSecondTitle.get_date(titles, second)
        third_date = CleanThirdTitle.get_date(titles, third)

        empty_string = ''

        dates: Series = (
            second_date
            .str.cat(third_date, na_rep=empty_string)
            .replace(empty_string, np.nan, regex=False)
        )

        dates = HandleTitles._change_to_date_format(dates)
        dates.name = "fecha"

        return dates
    
    @staticmethod
    def titles_to_columns(raw_titles):
        handle_titles = HandleRawTitles(raw_titles)
        unstacked_titles = handle_titles.generate_unstacked_titles()
        date_column = HandleTitles._handle_columns(
            unstacked_titles,
            'first',
            'second',
            'third',
            'fourth'
        )
        
        return date_column