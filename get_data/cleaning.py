import re
import pandas as pd
from pandas import DataFrame, Series

def get_sumativos(raw_description: DataFrame):

    sumativos_filter =  (
        raw_description
        ['descripcion']
        .str.contains("Sumativo")
        )
    
    return (
        raw_description
        ['descripcion']
        .loc[sumativos_filter]
    )

def get_sumativos_i_index(sumativos: Series):
    sumativos_ii_filter = (
        sumativos
        .str.contains("II Sumativo")
        )
    
    return (
        sumativos
        .loc[~sumativos_ii_filter]
        .index
        )

def replace_values(raw_description: DataFrame):
    many_white_spaces = re.compile(r'\s+')
    area = re.compile(r'Áreas?-?')

    return (
        raw_description['descripcion']
        .str.replace("Cepunt", "", regex=False)
        .str.replace("CEPUNT", "", regex=False)
        .str.replace("Ordinario", "", regex=False)
        .str.replace("Resultados", "", regex=False)
        .str.replace("2024-II", "", regex=False)
        .str.replace("II Sumativo", "", regex=False)
        .str.replace(":", "", regex=False)
        .str.replace("-", "", regex=False)
        .str.replace(" y ", "-", regex=False)
        .str.replace(" Y ", "-", regex=False)
        .str.replace(area, "", regex=True)
        .str.replace(many_white_spaces, " ", regex=True)
        .str.strip()
        )

def create_column_place(description_values: Series):
    places = re.compile(r'(Trujillo|Huamachuco|Sa.tiago\sde\sChuco|Valle\sJequetepeque|Valle)')

    column_place = (
        description_values
        .str.extract(places)
        [0]
        .str.replace("Samtiago", "Santiago", regex=False)
        )
    column_place.name = "lugar"

    return column_place
    
def create_column_mod(description_values: Series):
    mods = re.compile(
    r'(5to\sSecundaria|Deportistas\sCalificados|Personas?\scon\sDiscapacidad|V.ctimas\sde\sla\sViolencia\sExcelencia|V.ctimas\sde\sla\sViolencia|Excelencia)'
    )
    
    column_mod = (
        description_values
        .str.extract(mods)
        [0]
        .str.replace("Víctimas", "Victimas", regex=False)
        .str.replace("Personas", "Persona", regex=False)
        .str.replace("Persona", "Personas", regex=False)
        # .value_counts()
        )
    
    column_mod.name = "modalidad"
    
    return column_mod

def delete_sumativos_i(raw_description: DataFrame):
    sumativos = get_sumativos(raw_description)
    sumativos_i_index = get_sumativos_i_index(sumativos)

    raw_description = (
        raw_description
        .drop(sumativos_i_index)
        .reset_index()
        .drop(['index'], axis=1)
        )
    
    return raw_description   

def create_df_periods(raw_description: DataFrame):

    periods = (
        raw_description
        ['periodo']
        .str.split(" ", expand=True)
        .drop(0, axis=1)
        [1]
        .str.split("-", expand=True)
        )
    
    periods.columns = ['fecha_periodo', 'numero_periodo']
    
    periods['fecha_periodo'] = periods['fecha_periodo'].astype('int64')

    return periods

def generate_columns(raw_description: DataFrame):
    description_values = replace_values(raw_description)
    periods = create_df_periods(raw_description)
    column_place = create_column_place(description_values)
    column_mod = create_column_mod(description_values)

    joined_columns = pd.concat(
        [
            raw_description,
            periods,
            column_mod,
            column_place
            ],
            axis=1
            )
    
    return (
        joined_columns
        .drop(['periodo', 'descripcion'], axis=1)
        .reindex(columns=
                 ['link',
                  'fecha_periodo',
                  'numero_periodo',
                  'tipo_exam',
                  'modalidad',
                  'lugar']
                  )
        )

def filling_data(raw_description: DataFrame):
    filter_extraor_lugar_nan = (
        (raw_description['tipo_exam'] == "EXTRAORDINARIO") & (raw_description['lugar'].isna())
        )
    
    filter_extraor_mod_nan = (
        (raw_description['tipo_exam'] == "EXTRAORDINARIO") & (raw_description['modalidad'].isna())
        )
    
    filter_ordi_mod_nan = (
        (raw_description['tipo_exam'] == "ORDINARIO") & (raw_description['modalidad'].isna())
        )
    
    filter_cepu_mod_nan = (
        (raw_description['tipo_exam'] == "CEPUNT") & (raw_description['modalidad'].isna())
        )
    
    raw_description.loc[filter_extraor_lugar_nan, 'lugar'] = "Trujillo"
    raw_description.loc[filter_extraor_mod_nan, 'modalidad'] = "Excelencia"
    raw_description.loc[filter_ordi_mod_nan, 'modalidad'] = "Normal"
    raw_description.loc[filter_cepu_mod_nan, 'modalidad'] = "Normal"

    return raw_description

def clean_data(raw_description: DataFrame):
    raw_description = delete_sumativos_i(raw_description)
    raw_description = generate_columns(raw_description)
    description = filling_data(raw_description)

    return description
