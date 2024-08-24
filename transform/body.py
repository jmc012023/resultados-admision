import pandas as pd
import re
from names.definitions import LinksDataColumnNames, ResultColumnNames, GradesColumnNames

def get_names(raw_results):
    valid_name = re.compile(r'\s(\D+[0]?\D+[0]?)\s-?\d')

    return (
        raw_results
        [LinksDataColumnNames.ALL_RESULT.value]
        .str.extract(valid_name)
        [0]
        .str.strip()
        .str.replace('0 0', '', regex=False)
        .str.rstrip()
        .str.replace('0', 'O', regex=False)
        .str.lower()
    )       

def get_grades(raw_results):
    valid_grades = re.compile(r'(-?\d+\.\d+)')

    return (
        raw_results
        [LinksDataColumnNames.ALL_RESULT.value]
        .str.extractall(valid_grades)
        .unstack()
        .droplevel(level=0, axis=1)
    )

def get_career_and_status(raw_results):
    after_grades = re.compile(r'(\.\d+\s[A-Z].*)')
    digits = re.compile(r'\.\d+\s')

    return (
        raw_results
        [LinksDataColumnNames.ALL_RESULT.value]
        .str.extract(after_grades)
        [0]
        .str.replace(
            digits,
            '',
            regex=True
        )
    )

def get_status(raw_results):

    school_and_details = get_career_and_status(
        raw_results
    )

    valid_result = re.compile(r'(INGRESA.*|NO\sINGRESA.*|ING\.\s?2.*|AUSENTE.*|ANULADO.*|^SI\s|^NO\s|\sSI$|\sNO$)')
    possitive_pattern = re.compile(r'INGRESA([\w\s-]+)?')
    negative_pattern = re.compile(r'NO\D+')
    positive_result = 'SI'
    negative_result = 'NO'
    ingresa = 'INGRESA'
    no_ingresa = 'NO INGRESA'

    return (
        school_and_details
        .str.extract(valid_result)
        [0]
        .str.strip()
        .str.replace(negative_pattern, negative_result, regex=True)
        .str.replace(possitive_pattern, positive_result, regex=True)
        .str.replace(positive_result, ingresa, regex=False)
        .str.replace(negative_result, no_ingresa, regex=False)
        .str.replace('.', '', regex=False)
        .str.replace('ING 2-OPC', 'SEGUNDA OPC', regex=False)
        .str.lower()
        .str.strip()
    )

def get_career(raw_results):

    school_and_details = get_career_and_status(
        raw_results
    )

    valid_result2 = re.compile(r'INGRESA.*|NO\sINGRESA.*|ING\.\s?2.*|AUSENTE.*|ANULADO.*|^SI\s|^NO\s|\sSI$|\sNO$')

    return (
        school_and_details
        .str.replace(
            valid_result2,
            '',
            regex=True
        )
        .str.upper()
        .str.strip()
        .str.replace(".", " ", regex=False)
        .str.replace(":", " ", regex=False)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.lower()
    )

def join_results(
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

    column_names = [ResultColumnNames.NAMES.value, GradesColumnNames.ONE.value, GradesColumnNames.TWO.value, GradesColumnNames.THREE.value, GradesColumnNames.FOUR.value, GradesColumnNames.FIVE.value, ResultColumnNames.CAREER.value, ResultColumnNames.STATUS.value, LinksDataColumnNames.N_DF.value]

    joined_results.columns = column_names

    return joined_results

def create_body_results(raw_results):
    names = get_names(raw_results)
    grades = get_grades(raw_results)
    school = get_career(raw_results)
    details = get_status(raw_results)

    results = join_results(
        names,
        grades,
        school,
        details,
        raw_results
    )

    return results