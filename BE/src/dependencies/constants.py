import configparser
import random
import os

configfile = configparser.ConfigParser()

# Check if the config file exists
if not os.path.isfile("config.ini"):
    # generate default config
    configfile["DEFAULT"] = {
        "dbfile": "database.db",
        "SECRET_KEY": str(random.getrandbits(256)),
        "ALGORITHM": "HS256",
    }
    with open("config.ini", "w") as new_cf:
        configfile.write(new_cf)

else:
    configfile.read("config.ini")

dbfile = configfile["DEFAULT"]["dbfile"]
SECRET_KEY = configfile["DEFAULT"]["SECRET_KEY"]
ALGORITHM = configfile["DEFAULT"]["ALGORITHM"]

if SECRET_KEY == "":
    SECRET_KEY = random.getrandbits(32)

if ALGORITHM == "":
    ALGORITHM = "HS256"

configfile["DEFAULT"]["SECRET_KEY"] = SECRET_KEY
configfile["DEFAULT"]["ALGORITHM"] = ALGORITHM

# Path: src/dependencies/constants.py
