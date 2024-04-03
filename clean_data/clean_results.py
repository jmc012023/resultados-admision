import pandas as pd
import re

class HandleRawResults:
    empty_string = ''

    @staticmethod
    def _get_names(raw_results):
        valid_name = re.compile(r'\s(\D+[0]?\D+[0]?)\s-?\d')

        return (
            raw_results
            ['main']
            .str.extract(valid_name)
            [0]
            .str.strip()
        )       

    @staticmethod
    def _get_grades(raw_results):
        valid_grades = re.compile(r'(-?\d+\.\d+)')

        return (
            raw_results
            ['main']
            .str.extractall(valid_grades)
            .unstack()
            .droplevel(level=0, axis=1)
        )
    
    @staticmethod
    def _get_school_and_details(raw_results):
        after_grades = re.compile(r'(\.\d+\s[A-Z].*)')
        digits = re.compile(r'\.\d+\s')

        return (
            raw_results
            ['main']
            .str.extract(after_grades)
            [0]
            .str.replace(
                digits,
                HandleRawResults.empty_string,
                regex=True
            )
        )
    
    @staticmethod
    def _get_details(raw_results):

        school_and_details = HandleRawResults._get_school_and_details(
            raw_results
        )

        valid_result = re.compile(r'(INGRESA.*|NO\sINGRESA.*|ING\.\s?2.*|AUSENTE.*|ANULADO.*|^SI\s|^NO\s|\sSI$|\sNO$)')
        possitive_pattern = re.compile(r'INGRESA([\w\s-]+)?')
        negative_pattern = re.compile(r'NO\D+')
        positive_result = 'SI'
        negative_result = 'NO'

        return (
            school_and_details
            .str.extract(valid_result)
            [0]
            .str.strip()
            .str.replace(negative_pattern, negative_result, regex=True)
            .str.replace(possitive_pattern, positive_result, regex=True)
        )
    
    @staticmethod
    def _get_school(raw_results):

        school_and_details = HandleRawResults._get_school_and_details(
            raw_results
        )

        valid_result2 = re.compile(r'INGRESA.*|NO\sINGRESA.*|ING\.\s?2.*|AUSENTE.*|ANULADO.*|^SI\s|^NO\s|\sSI$|\sNO$')

        return (
            school_and_details
            .str.replace(
                valid_result2,
                HandleRawResults.empty_string,
                regex=True
            )
            .str.upper()
            .str.strip()
        )
    
    @staticmethod
    def _join_results(
        names,
        grades,
        school,
        details,
        raw_results
    ):
        joined_results = pd.concat(
            [
                names,
                grades,
                school,
                details,
                raw_results['n_df']
            ],
            axis=1  
        )

        column_names = ['names','r1', 'r2', 'r3', 'r4', 'r5', 'escuela', 'resultado', 'n_df']

        joined_results.columns = column_names

        return joined_results
    
    @staticmethod
    def generated_results(raw_results):
        names = HandleRawResults._get_names(raw_results)
        grades = HandleRawResults._get_grades(raw_results)
        school = HandleRawResults._get_school(raw_results)
        details = HandleRawResults._get_details(raw_results)

        results = HandleRawResults._join_results(
            names,
            grades,
            school,
            details,
            raw_results
        )

        return results