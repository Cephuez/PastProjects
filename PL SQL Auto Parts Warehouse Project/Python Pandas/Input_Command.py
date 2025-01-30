import oracledb
import pandas as pd
from sqlalchemy import create_engine

class command:
    cs = "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1522)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = orclpdb)))"

    #connection=oracledb.connect( user="project", password= "password123", dsn= cs)
    # create engine
    engine = create_engine('oracle+oracledb://', creator=lambda: connection)

    user_name = ""
    password = ""

    def __init__(self, name):
        self.name = name

    def print(self):
        print("Yo What's up")

    def log_in(self)
        user_name = input("User Name: ")
        password = input("Password: ")
        connection=oracledb.connect( user="project", password= "", dsn= cs)
