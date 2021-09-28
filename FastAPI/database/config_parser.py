import configparser
from pathlib import Path

parser = configparser.ConfigParser()
config_file = Path("database/config.ini")
parser.read(config_file)

user = parser.get("database", "user")
passwd = parser.get("database", "pass")
db_name = parser.get("database", "db")
host = parser.get("database", "host")
