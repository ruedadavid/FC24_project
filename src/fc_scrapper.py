""" Scrapper for FC25
"""
from pathlib import PosixPath
import re
import json
import typer
import requests
from bs4 import BeautifulSoup
from library import read_config_file


def main() -> None:
    """main _summary_
    """
    src_dir = '/home/davo/Projects/FC24_project/src'
    src_route = PosixPath(src_dir)
    config_file = 'app.messages.conf'
    config_file_route = PosixPath.joinpath(src_route, config_file)
    #
    rut = read_config_file(filename=config_file_route, features='DATA')
    url = 'web_url'
    #
    #
    for page in range(int(rut['max_pages'])):
        count = page + 1
        complete_route = f'{rut[url]}{count}'
        page = requests.get(complete_route, timeout=30)
        routes = read_config_file(filename=config_file_route, features='ROUTES')
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            link_list = []
            for link in soup.find_all("a", class_="Table_profileCellAnchor__L23hq"):
                link_list.append(link)
            list02 = [link['href']for link in link_list]
            out_dir = PosixPath(routes['output_dir'])
            output_file = PosixPath.joinpath(out_dir, f'file{count}.json').resolve()
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(list02, f, indent=2)
            #
            #
        examples = [0, 10 , 20, 30, 60, 80 ,99]
        for ex in examples:
            tmp_text = link_list[ex].text
            tmp = re.split(r'#\d+', tmp_text, maxsplit=0, flags=0)[1]
            print(f'<<{tmp}>>,<<{link_list[ex]["href"]}>>')


if __name__ == "__main__":
    typer.run(main)
