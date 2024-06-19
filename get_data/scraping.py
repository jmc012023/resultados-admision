import requests
from requests import Response
from bs4 import BeautifulSoup
from bs4 import Tag, ResultSet
from get_data.handle_error import isElementNone, isListEmpty, HTMLElementExecption
import sys

def get_response(url: str) -> Response:
    response = requests.get(url)
    if (response.status_code == 200):
        return response
    else:
        raise requests.HTTPError
   
def scraping_web(response: Response, id_selector: str, class_selector: str):
    """
    id_selector: It is the main css selector that contains
    all information about results
    class_selector: They are the css selector that refers
    all periods and all type of tests
    """

    soup = BeautifulSoup(response.text, 'html.parser')

    main_container = soup.find(id=id_selector)

    isElementNone(main_container)

    period_accordions: ResultSet[Tag] = main_container.find_all(
        class_=class_selector,
        recursive=False
        )

    isListEmpty(period_accordions)

    period_contents: ResultSet[Tag] = map(
        lambda period_accordion: period_accordion.find("div"),
        period_accordions[:-1]
        )

    results: list[tuple[str, str, str, str]] = []

    for content in period_contents:
        isElementNone(content)
        tag_period = content.find_previous_sibling("a")

        isElementNone(tag_period)

        tag_period_text = tag_period.get_text().strip()

        div_type_tests: ResultSet[Tag] = content.find_all(
            class_=class_selector,
            recursive=False
        )

        isListEmpty(div_type_tests)

        for accordion in div_type_tests:
            
            tag_type_test = accordion.find("a").get_text().strip()
            container_results = accordion.find("div")

            tag_a_results: ResultSet[Tag] = container_results.find_all("a")

            isElementNone(tag_type_test)
            isElementNone(container_results)
            isListEmpty(tag_a_results)

            for result in tag_a_results:
                link = result['href']
                description = result.get_text().strip()

                information_test = (
                    tag_period_text,
                    tag_type_test,
                    description,
                    link
                    )
                
                results.append(information_test)

    return results

def get_urls(url, id_selector, css_selector):

    try:
        r = get_response(url)
        scraping_data = scraping_web(r, id_selector, css_selector)
    except Exception as e:
        if(isinstance(e, requests.ConnectionError)):
            print(e)
            sys.exit(1)
        if (isinstance(e, requests.HTTPError)):
            print(e)
            sys.exit(1)
        if (isinstance(e, HTMLElementExecption)):
            print(e)
            sys.exit(1)
        else:
            print("Error ->", e)
            sys.exit(1)
    else:
        return scraping_data