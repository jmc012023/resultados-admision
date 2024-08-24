import requests
from requests import Response
from bs4 import BeautifulSoup
from bs4 import Tag, ResultSet
from enum import Enum
from names.definitions import WebPageContent

URL = "https://www.admisionunt.info/padron"
SUCCESSFUL_STATUS_CODE = 200

class DivTagContainerOfAllResults(Enum):
    ID = "container-main"

class DivTagContainerOfAllAnchors(Enum):
    TAG_SELECTOR = "div"
    CLASS_SELECTOR = "accordion-content"

class TableTagContainerOfLinks(Enum):
    TAG_SELECTOR = "table"
    CLASS_SELECTOR = "table table-sm table-responsive"

class AnchorTag(Enum):
    TAG_SELECTOR = "a"
    HREF_ATTRIBUTE = "href"

def get_HTML_cotent(url: str) -> Response:
    response = requests.get(url)
    if (response.status_code == SUCCESSFUL_STATUS_CODE):
        return response
    else:
        raise requests.HTTPError
    
def get_table_tags(r: Response):
    soup = BeautifulSoup(r.text, 'html.parser')
    main_container = soup.find(id=DivTagContainerOfAllResults.ID.value)

    table_tags = main_container.find_all(
        TableTagContainerOfLinks.TAG_SELECTOR.value,
        class_=TableTagContainerOfLinks.CLASS_SELECTOR.value
    )

    return table_tags

def get_a_tag_description(a_tag: Tag):
    div_container = a_tag.find_parent(
        DivTagContainerOfAllAnchors.TAG_SELECTOR.value,
        class_=DivTagContainerOfAllAnchors.CLASS_SELECTOR.value
    )
    a_tag_description = div_container.previous_sibling.previous_sibling
    return a_tag_description

def get_link_result(a_tag: Tag):
    return a_tag[AnchorTag.HREF_ATTRIBUTE.value]

def get_result_detail(a_tag: Tag):
    return next(a_tag.stripped_strings)

def get_test_and_period(a_tag: Tag):
    a_test_tag = get_a_tag_description(a_tag=a_tag)
    test_description = next(a_test_tag.stripped_strings)

    a_period_tag = get_a_tag_description(a_tag=a_test_tag)
    period_description = next(a_period_tag.stripped_strings)

    return period_description, test_description

def generate_test_information(a_tag: Tag):
    period_description, test_description = get_test_and_period(a_tag)
    detail = get_result_detail(a_tag)
    link = get_link_result(a_tag)

    return (period_description, test_description, detail, link)

def create_type_test(id, info_result):
    test_web_page = WebPageContent(
        id_result=id,
        periods=info_result[0],
        test_type=info_result[1],
        details=info_result[2],
        link=info_result[3]
    )
    return test_web_page

def create_webpage_data():
    response = get_HTML_cotent(url=URL)
    table_tags = get_table_tags(r=response)
    a_link_tags = [table_tag.find_all(AnchorTag.TAG_SELECTOR.value) for table_tag in table_tags]
    valid_a_tags = sum(a_link_tags, [])
    info_results = map(lambda a_tag: generate_test_information(a_tag), valid_a_tags)
    webpage_data = [create_type_test(id, info_result) for id, info_result in enumerate(info_results)]

    return webpage_data
