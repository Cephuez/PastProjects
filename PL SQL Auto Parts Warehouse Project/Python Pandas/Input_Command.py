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
        print("Application Started")

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
        command = ""
        #query = input("Do Something")
        #query = "SELECT EMPLOYEE_ID, FIRST_NAME, LAST_NAME FROM EMPLOYEES ORDER BY 1"
        #df = pd.read_sql(query, self.engine)
        # test data prep
        #df_test = df.copy()
        # export test DataFrame with pandas to_sql
        #df_test.to_sql('test', con = self.engine, if_exists='replace', index=False)
        #print(df)
        print("1. Start Picking")
        print("2. Stage Items")
        print("3. Process Orders")
        print("4. Move Parts")
        print("5. Process Receiving Items")
        print("0. Exit Program")
        while(command != "0"):
            command = input("Enter your Command")
            if(command == "1"):
                self.picking_command()
                print("Now Picking")
            elif(command == "2"):
                print("Stage Items")
            elif(command == "3"):
                print("Process Orders")
            elif(command == "4"):
                print("Move Parts")
            elif(command == "5"):
                print("Process Receiving Items")
            elif(command == "0"):
                print("Closing Program")

    def picking_command(self):
        command = ""
        query = "SELECT ORDER_ID FROM ORDERS WHERE ORDER_DATE IS NOT NULL AND SHIP_DATE IS NULL ORDER BY ORDER_DATE"
        df = pd.read_sql(query, self.engine)
        df_test = df.copy()
        df_test.to_sql('test', con = self.engine, if_exists='replace', index=False)
        print(df)
        while(command != '0'):
            command = input("Enter Order ID to Pick: ")
            # Redirect user to the the next window where they will now pick the parts
            














