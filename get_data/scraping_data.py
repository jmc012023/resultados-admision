import requests
from requests import Response
from selectolax.parser import HTMLParser

def get_response(url: str) -> Response | None:
    try:
        r = requests.get(url)
        return r
    except requests.ConnectionError:
        print("Error un error durante la consulta a la pagina web")
        return None
    except requests.HTTPError as exc:
        print("Error con el status code")
        return None
   
def scraping(r: Response, css_selector: str) -> dict[str, str]:
    values_to_exclude = 'i sumativo'
    values_to_keep = 'ii sumativo'

    tree = HTMLParser(r.text)
    
    if tree.any_css_matches((css_selector, )):
        a_tags = tree.css(css_selector)

        sumativos = filter(lambda a_tag: a_tag.text().lower().find(values_to_exclude) != -1, a_tags)
        only_sumativos_2 = list(filter(lambda a_tag: a_tag.text().lower().find(values_to_keep) != -1, sumativos))

        all_exec_sumativos = list(filter(lambda a_tag: a_tag.text().lower().find(values_to_exclude) == -1, a_tags))
        valid_a_tags = all_exec_sumativos + only_sumativos_2

        urls = list(map(lambda a_tag: a_tag.attributes['href'], valid_a_tags))

        return urls
    else:
        return {"error": f"No existe ni un elemento html con ese CSS Selector {css_selector}" }

def get_urls(url, css_selector):

    r = get_response(url)

    urls = scraping(r, css_selector)

    # print(urls)
    # print(len(urls))

    return urls

# quering_web_page()
    


# df = pd.read_csv("http://admisionunt.info/docs/padrones/20191/20191_ordinario/20191_ordinario5to_B.txt",
#                  encoding='ISO-8859-1',
#                  names={"main": 0}
#                  )
# df['main']

# many_white_spaces = re.compile(r'\s+')
# one_white_space = ' '

# df['main'].str.replace(many_white_spaces, one_white_space, regex=True)