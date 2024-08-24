import pandas as pd
from names.definitions import LinksDataColumnNames, ResultColumnNames, GradesColumnNames
from pandas import DataFrame
from enum import Enum

class TestTypes(Enum):
    ORDINARIO = 'ordinario'
    EXTRAORDINARIO = 'extraordinario'
    CEPUNT = 'cepunt'

def create_filter_fourth_grades(results):
    years = [2019, 2020]

    cepunt_data = results[ResultColumnNames.TEST_TYPE.value] == TestTypes.CEPUNT.value
    year_data = results[ResultColumnNames.YEAR_PERIOD.value].isin(years)

    filter_fourth_grades = (cepunt_data) & (year_data)

    return filter_fourth_grades

def create_filter_first_grades(results):
    types = [TestTypes.EXTRAORDINARIO.value, TestTypes.ORDINARIO.value]
    # You should add 2025 and period i
    year = 2024
    period = "ii"

    type_data = results[ResultColumnNames.TEST_TYPE.value].isin(types)
    year_data = results[ResultColumnNames.YEAR_PERIOD.value] == year
    period_data = results[ResultColumnNames.PERIOD.value] == period

    filter_first_grades = (type_data) & (year_data) & (period_data)

    return filter_first_grades

def create_filter_third_grades(results):
    filter_first_grades = create_filter_first_grades(
        results
    )

    filter_fourth_grades = create_filter_fourth_grades(
        results
    )

    filter_third_grades = ~((filter_first_grades) | (filter_fourth_grades))

    return filter_third_grades

def filter_fourth_grades(results):
    filter_fourth_grades = create_filter_fourth_grades(
        results
    )

    fourth_grades = results[filter_fourth_grades]

    fourth_grades = fourth_grades.drop([
        GradesColumnNames.ONE.value,
        GradesColumnNames.TWO.value,
        GradesColumnNames.THREE.value,
        GradesColumnNames.FIVE.value],
        axis=1
    )

    fourth_grades = fourth_grades.rename(
        columns={
            GradesColumnNames.FOUR.value: ResultColumnNames.GRADE.value
        }
    )

    return fourth_grades

def filter_first_grades(results):
    filter_first_grades = create_filter_first_grades(
        results
    )

    first_grades = results[filter_first_grades]

    first_grades = first_grades.drop([
        GradesColumnNames.TWO.value,
        GradesColumnNames.THREE.value,
        GradesColumnNames.FOUR.value,
        GradesColumnNames.FIVE.value],
        axis=1
    )

    first_grades = first_grades.rename(
        columns={
            GradesColumnNames.ONE.value: ResultColumnNames.GRADE.value
        }
    )

    return first_grades

def filter_third_grades(results):
    filter_third_grades = create_filter_third_grades(
        results
    )

    third_grades = results[filter_third_grades]

    third_grades = third_grades.drop([
        GradesColumnNames.ONE.value,
        GradesColumnNames.TWO.value,
        GradesColumnNames.FOUR.value,
        GradesColumnNames.FIVE.value],
        axis=1
    )

    third_grades = third_grades.rename(
        columns={
            GradesColumnNames.THREE.value: ResultColumnNames.GRADE.value
        }
    )

    return third_grades

def combine_grades(grades1, grades3, grades4):

    results = pd.concat(
        [
            grades1,
            grades3,
            grades4
        ]
    )

    results = results.reset_index()
    results = results.drop(['index', LinksDataColumnNames.N_DF.value], axis=1)
    
    return results

def filling_data(results: DataFrame):
    filter_extraor_lugar_nan = (
        (results[ResultColumnNames.TEST_TYPE.value] == TestTypes.EXTRAORDINARIO.value) & 
        (results[ResultColumnNames.PLACE.value].isna())
        )
    
    filter_extraor_mod_nan = (
        (results[ResultColumnNames.TEST_TYPE.value] == TestTypes.EXTRAORDINARIO.value) & 
        (results[ResultColumnNames.MOD.value].isna())
        )
    
    filter_ordi_mod_nan = (
        (results[ResultColumnNames.TEST_TYPE.value] == TestTypes.ORDINARIO.value) & 
        (results[ResultColumnNames.MOD.value].isna())
        )
    
    filter_cepu_mod_nan = (
        (results[ResultColumnNames.TEST_TYPE.value] == TestTypes.CEPUNT.value) & 
        (results[ResultColumnNames.MOD.value].isna())
        )
    
    results.loc[filter_extraor_lugar_nan, ResultColumnNames.PLACE.value] = "trujillo"
    results.loc[filter_extraor_mod_nan, ResultColumnNames.MOD.value] = "excelencia"
    results.loc[filter_ordi_mod_nan, ResultColumnNames.MOD.value] = "estandar"
    results.loc[filter_cepu_mod_nan, ResultColumnNames.MOD.value] = "estandar"

    return results