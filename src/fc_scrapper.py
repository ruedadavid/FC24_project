""" Scrapper for FC25
"""
from pathlib import PosixPath
import typer
from library import read_config_file

#from requests import request



def main() -> None:
    """main _summary_
    """
    print('Test 1.')
    src_dir = '/home/davo/Projects/FC24_project/src'
    src_route = PosixPath(src_dir)
    config_file = 'app.messages.conf'
    config_file_route = PosixPath.joinpath(src_route, config_file)
    rut = read_config_file(filename=config_file_route, features='ROUTES')
    print(rut)


if __name__ == "__main__":
    typer.run(main)
