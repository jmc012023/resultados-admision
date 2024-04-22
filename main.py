import asyncio
from clean_data.cleaning_data import generate_cleaned_data
from get_data.getting_data import generate_raw_data

async def main():

    url = 'https://www.admisionunt.info/padron'
    id_selector = "container-main"
    class_selector = "accordion-container"
    encoding = 'ISO-8859-1'
    name_column = 'main'

    (description, raw_data) = await generate_raw_data(
        url,
        id_selector,
        class_selector,
        encoding,
        name_column
        )

    results = generate_cleaned_data(raw_data, description)

    # print(results)

    results.to_csv('unt_results.csv', index=False)

if __name__ == '__main__':
    asyncio.run(main())