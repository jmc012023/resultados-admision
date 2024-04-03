from get_data.appending_data import join_all_data
import sys

async def generate_raw_data(url, css_selector, encoding, name_column):
    
    try:
        await join_all_data(url, css_selector, encoding, name_column)

    except:
        print("Error al obtener la data de la pagina web")
        sys.exit(1)