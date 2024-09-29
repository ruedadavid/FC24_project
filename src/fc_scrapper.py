""" Scrapper for FC25
"""
from library import read_config_file
from pathlib import Path
import typer
#from requests import request



def main() -> None:
    """main _summary_
    """
    print('Test 1.')
    src_dir = '/home/davo/Projects/FC24_project/src'
    config_file = 'app.messages.conf'
    config_file = Path.joinpath(Path(src_dir), config_file)
    rut = read_config_file(filename=config_file, features='ROUTES')
    print(rut)


if __name__ == "__main__":
    typer.run(main)
