import pandas as pd
from pandas import Series, DataFrame
from names.definitions import ResultColumnNames, WPDataColumnNames
import re

def create_period_columns(periods_column: Series):
    # periods['year_period'] = periods['year_period'].astype('int64')
    periods = (
        periods_column
        .str.lower()
        .str.replace('ó', 'o', regex=False)
        .str.replace('-', ' ', regex=False)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
        .str.split(expand=True)
        .iloc[:, 1:]
        .rename(columns={1: ResultColumnNames.YEAR_PERIOD.value, 2: ResultColumnNames.PERIOD.value})
    )

    periods[ResultColumnNames.YEAR_PERIOD.value] = periods[ResultColumnNames.YEAR_PERIOD.value].astype('int64')
    return periods

def create_test_column(test_type_column: Series):
    return (
        test_type_column
        .str.strip()
        .str.lower()
    )

def create_details_column(details_column: Series):
    return (
        details_column
        .str.strip()
        .str.lower()
        .str.replace('á', 'a', regex=False)
        .str.replace('é', 'e', regex=False)
        .str.replace('í', 'i', regex=False)
        .str.replace('ó', 'o', regex=False)
        .str.replace('ú', 'u', regex=False)
        .str.replace(r'[:.,;-]', ' ', regex=True)
        .str.replace(r'\s+', ' ', regex=True)
    )

def remove_i_sumativos(details_column: Series):

    i_sumativos = details_column.str.contains('i sumativo')
    ii_sumativos = details_column.str.contains('ii sumativo')

    return (
        details_column[(~i_sumativos) | (ii_sumativos)]
    )

def create_place_column(details_column: Series):
    place_regex = re.compile(r'(trujillo|huamachuco|sa.tiago\sde\schuco|valle\sjequetepeque|valle)')
    return (
        details_column
        .str.extract(place_regex)
        .rename(columns={0: ResultColumnNames.PLACE.value})
        [ResultColumnNames.PLACE.value]
        .str.replace("samtiago", "santiago", regex=False)
    )

def create_mod_column(details_column: Series):
    mod_regex = re.compile(
        r'(5to\ssecundaria|deportistas\scalificados|personas?\scon\sdiscapacidad|v.ctimas\sde\sla\sviolencia\sexcelencia|v.ctimas\sde\sla\sviolencia|excelencia)'
    )

    return (
        details_column
        .str.extract(mod_regex)
        .rename(columns={0: ResultColumnNames.MOD.value})
        [ResultColumnNames.MOD.value]
        .str.replace("personas", "persona", regex=False)
        .str.replace("persona", "personas", regex=False)
        .str.replace('victimas de la violencia excelencia', 'victimas de la violencia', regex=False)
    )

def join_columns(initial_wp: DataFrame,
                 periods: DataFrame,
                 test_type: Series,
                 details: Series,
                 mod: Series,
                 place: Series):
    return (
        pd.merge(details, test_type, left_index=True, right_index=True, how='left')
        .merge(periods, left_index=True, right_index=True, how='left')
        .merge(mod, left_index=True, right_index=True, how='left')
        .merge(place, left_index=True, right_index=True, how='left')
        .merge(initial_wp[ResultColumnNames.LINK.value], left_index=True, right_index=True, how='left')
        .reset_index()
        .drop(['index', WPDataColumnNames.DETAILS.value], axis=1)
    )

def create_webpage_frame(result_webpage):
    
    # columns = ["resultado_id", "periodo", "tipo_exam", "detalles", "link"]
    # columns = ["id_result", "period", "test_type", "details", "link"]

    initial_wp_frame = pd.DataFrame(data=result_webpage)

    periods = create_period_columns(initial_wp_frame[WPDataColumnNames.PERIODS.value])
    test_type = create_test_column(initial_wp_frame[ResultColumnNames.TEST_TYPE.value])
    details = create_details_column(initial_wp_frame[WPDataColumnNames.DETAILS.value])
    details = remove_i_sumativos(details)
    mod = create_mod_column(details.copy())
    place = create_place_column(details.copy())

    t_wp_frame = join_columns(initial_wp_frame, periods, test_type, details, mod, place)

    return t_wp_frame, initial_wp_frame
