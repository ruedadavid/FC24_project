""" Scraper for FC25
"""
from pathlib import PosixPath
#import re
import json
import typer
from typing_extensions import Annotated
import requests
from bs4 import BeautifulSoup
from utils import read_config_file


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

def main(
    ea_last_page: Annotated[int, typer.Option("--pages", "-p")] = -1
) -> None:
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
        if req.status_code == 200:
            soup = BeautifulSoup(
                markup = req.content,
                features = 'html.parser'
            )
            if ea_page == 1 and ea_last_page == -1:
                ea_last_page = int(
                    get_data(
                        soup,
                        scrapers['scraper_max_type'],
                        scrapers['scraper_max'],
                        all_data=False
                    )[0]
                )
                print(f"Total Páginas>>{ea_last_page}:{type(ea_last_page)}>>")
            player_cards = get_data(
                soup = soup,
                name = scrapers['player_link_type'],
                class_ = scrapers['player_link']
            )
            player_links = [plr_link.get('href') for plr_link in player_cards]
            #
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(player_links, f, indent=2)
            #
            print(f"Página {output_file}, Links/página: {len(player_links)}:")
            if ea_page == ea_last_page:
                print(f'\nTotal de páginas visitadas/descargadas { ea_page }')
                break


if __name__ == "__main__":
    typer.run(main)
