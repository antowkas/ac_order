from DBConnection import DBConnect
from json import load as json_load

if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json_load(config_file)
        db_structure = config["db_structure"]
    db = DBConnect(config["path_db"])

