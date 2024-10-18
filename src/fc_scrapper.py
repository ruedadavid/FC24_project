""" Scraper for FC25
"""
from pathlib import PosixPath
#import re
import json
import typer
import requests
from bs4 import BeautifulSoup
from library import read_config_file


def get_data(
    soup: BeautifulSoup,
    name:str,
    class_:str,
    all_data:bool = True
) -> list:
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
    if all_data:
        return finds
    return [finds[-1].text]

def main() -> None:
    """main _summary_
    """
    config_file = 'parameters.conf'
    src_route = PosixPath(__file__).parent.parent.resolve()
    config_file_route = src_route.joinpath('src', config_file)
    #
    routes = read_config_file(
        filename=config_file_route,
        features='ROUTES'
    )
    scrapers = read_config_file(
        filename=config_file_route,
        features='SCRAPER'
    )
    #
    routes = {key:src_route.joinpath(route) for key, route in routes.items()}
    print(routes)
    ea_page = 0
    ea_last_page = 2
    player_links = []
    while True:
        ea_page = ea_page + 1
        output_file = PosixPath.joinpath(
                routes['output_dir'],
                f'file{ea_page}.json'
            )
        complete_route = f"{scrapers['url']}{ea_page}"
        req = requests.get(
            url=complete_route,
            timeout=30
        )
        print(f'Páginas { ea_last_page }-{ ea_page }')
        if ea_page == ea_last_page:
            break
        if req.status_code == 200:
            soup = BeautifulSoup(
                markup = req.content,
                features = 'html.parser'
            )
            if ea_page == 1:
                ea_last_page = int(
                    get_data(
                        soup,
                        scrapers['scraper_max_type'],
                        scrapers['scraper_max'],
                        all_data=False
                    )[0]
                )
                print(f"last page: >> {ea_last_page}: {type(ea_last_page)}>>")
            if ea_page == ea_last_page:
                print(f'Páginas { ea_page }')
                break
            player_cards = get_data(
                soup = soup,
                name = scrapers['player_class_type'],
                class_ = scrapers['player_link']
            )
            link_list = [link for link in player_cards]
            player_links = [link['href'] for link in link_list]
            with open(output_file.resolve(), 'w', encoding='utf-8') as f:
                json.dump(player_links, f, indent=2)
            print(player_links)


if __name__ == "__main__":
    typer.run(main)
