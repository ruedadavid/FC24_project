from pathlib import PosixPath 
import configparser

def read_config_file(filename: PosixPath, features: str = 'DEFAULT') -> dict:
    """read_config_file Function reads configuration files and return a
    dictionary with the found keys
    Parameters
    ----------
    filename : PosixPath
        file path to be read
    features : str
        Name of the set of features to be read
    Returns
    -------
    dict
        Dictionary with all entities in the feature of interest
    """
    config = configparser.ConfigParser()
    config.read(filenames=filename)
    details_dict = dict(config[features])
    return details_dict