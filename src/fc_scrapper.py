""" Scrapper for FC25
"""
from pathlib import PosixPath
import re
import json
import typer
import requests
from bs4 import BeautifulSoup
from library import read_config_file


def get_limit(
    soup: BeautifulSoup,
    name:str,
    class_:str
) -> int:
    """fname _summary_

    Parameters
    ----------
    arg : datatype
        _description_

    Returns
    -------
    type
        _description_
    """
    finds = soup.find_all(
        name = name,
        class_ = class_
    )
    return int(finds[-1].text)

def main() -> None:
    """main _summary_
    """
    src_route = PosixPath(__file__).parent.resolve()
    print(src_route)
    url = 'web_url'
    config_file = 'app.messages.conf'
    config_file_route = src_route.joinpath(config_file)
    #
    rut = read_config_file(filename=config_file_route, features='DATA')
    routes = read_config_file(filename=config_file_route, features='ROUTES')
    routes = {key:src_route.joinpath(route) for key, route in routes.items()}
    scrappers = read_config_file(filename=config_file_route, features='SCRAPPER')
    #
    ea_page = 0
    ea_pages = 200
    while True:
        ea_page = ea_page + 1
        complete_route = f'{rut[url]}{ea_page}'
        req = requests.get(complete_route, timeout=30)
        soup = BeautifulSoup(
                markup = req.content,
                features = 'html.parser'
        )
        print(f'{ea_page}')
        if req.status_code == 200:
            if ea_page == 1:
                limit = get_limit(
                    soup,
                    scrappers['scrapper_max_type'],
                    scrappers['scrapper_max']
                )
                print(f'Páginas { limit }-{ ea_page }')
            if ea_page == limit:
                print(f'P+aginas { ea_page }')
                break
        if ea_page == ea_pages:
            break
    for ea_page in range(int(rut['max_pages'])):
        complete_route = f'{rut[url]}{ea_page + 1}'
        #
        if req.status_code == 200:
            output_file = PosixPath.joinpath(
                routes['output_dir'],
                f'file{ea_page + 1}.json'
            )
            soup = BeautifulSoup(
                markup = req.content,
                features = 'html.parser'
            )
            if ea_page == 0:
                limits = soup.find_all(
                    name = scrappers['scrapper_max_type'],
                    class_ = scrappers['scrapper_max'],
                )
                limit = int(limits[-1].text)
                print(f"\n{limit}\n")
            link_list = []
            #
            player_cards = soup.find_all(
                name = scrappers['player_class_type'],
                class_ = scrappers['player_link']
            )
            link_list = [link for link in player_cards]
            list02 = [link['href'] for link in link_list]
            #
            #
            with open(output_file.resolve(), 'w', encoding='utf-8') as f:
                json.dump(list02, f, indent=2)
            #
            #
        examples = [0, 10 , 20, 30, 60, 80 ,99]
        for ex in examples:
            tmp_text = link_list[ex].text
            tmp = re.split(r'\D+', tmp_text, maxsplit=0, flags=0)[0]
            print(f'<<{tmp}>>,<<{link_list[ex]["href"]}>>')


if __name__ == "__main__":
    typer.run(main)
