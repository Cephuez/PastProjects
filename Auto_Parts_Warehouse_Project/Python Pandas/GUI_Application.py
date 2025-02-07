import oracledb
import pandas as pd
from sqlalchemy import create_engine

class gui_application:
    engine = ""
    cs = ""
    connection = ""
    name = ""

    def __init__(self, name):
        self.name = name

    def print(self):
        print("GUI Application Started")

    def log_in(self):
        #self.user_name = input("User Name: ")
        #self.password = input("Password: ")
        user_name = "Project"
        password = "password123"
        cs = "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1522)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = orclpdb)))"
        self.connection = oracledb.connect( user=user_name, password= password, dsn= cs)
        self.engine = create_engine('oracle+oracledb://', creator=lambda: self.connection)

    def read_commands(self):
        command = ""
        print("1. Start Picking")
        print("2. Stage Items")
        print("3. Gather Order Parts")
        print("4. Move Parts")
        print("5. Process Receiving Items")
        print("6. Process Order")
        print("7. Look Product's Location")
        print("0. Exit Program")
        while(command != "0"):
            command = input("Enter your Command: ")
            #command = "3"
            if(command == "1"):
                print("Picking List")
                self.picking_command()
            elif(command == "2"):
                print("Stage Items")
                self.staging_parts()
            elif(command == "3"):
                print("Gather Order Parts")
                self.gather_parts()
            elif(command == "4"):
                print("Move Parts")
            elif(command == "5"):
                print("Process Receiving Items")
            elif(command == "6"):
                print("Complete Order")
            elif(command == "0"):
                print("Closing Program")
                break
            else:
                print("Wrong Input")
            command = "0"
    
