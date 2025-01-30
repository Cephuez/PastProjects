import oracledb
import pandas as pd
from sqlalchemy import create_engine

class command:
    #connection=oracledb.connect( user="project", password= "password123", dsn= cs)
    # create engine
    engine = ""
    cs = ""
    connection = ""

    def __init__(self, name):
        self.name = name

    def print(self):
        print("Yo What's up")

    '''
    For the sake of debugging, I will have the username and password already put in correctly
    '''
    def log_in(self):
        #self.user_name = input("User Name: ")
        #self.password = input("Password: ")
        user_name = "Project"
        password = "password123"
        cs = "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1522)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = orclpdb)))"
        self.connection = oracledb.connect( user=user_name, password= password, dsn= cs)
        self.engine = create_engine('oracle+oracledb://', creator=lambda: self.connection)

    def read_command(self):
        #query = input("Do Something")
        query = "SELECT EMPLOYEE_ID, FIRST_NAME, LAST_NAME FROM EMPLOYEES ORDER BY 1"
        df = pd.read_sql(query, self.engine)
        # test data prep
        df_test = df.copy()
        # export test DataFrame with pandas to_sql
        df_test.to_sql('test', con = self.engine, if_exists='replace', index=False)
        print(df)
