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
            #df = pd.read_sql(query, self.engine)
            #df_test = df.copy()
            #df_test.to_sql('test', con = self.engine, if_exists='replace', index=False)
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
        print("1. Start Picking")
        print("2. Stage Items")
        print("3. Process Orders")
        print("4. Move Parts")
        print("5. Process Receiving Items")
        print("0. Exit Program")
        while(command != "0"):
            command = input("Enter your Command: ")
            #command = "1"
            if(command == "1"):
                print("Picking List")
                self.picking_command()
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
            else:
                print("Wrong Input")
            command = "0"

    def picking_command(self):
        command = ""
        query = "SELECT ORDER_ID FROM ORDERS WHERE ORDER_DATE IS NOT NULL AND SHIP_DATE IS NULL ORDER BY ORDER_DATE"
        df = pd.read_sql(query, self.engine)
        df_test = df.copy()
        df_test.to_sql('test', con = self.engine, if_exists='replace', index=False)

        # Prompt user what order_id to pick
        bin_picked = self.pick_bin_from_list()
        self.pick_parts(bin_picked)

    def pick_bin_from_list(self):
        command = ""
        bin_picked = ""
        while(command != '0'):
            #order_id = input("Enter Order ID to Pick: ")
            query = "SELECT BIN_LOCATION, SUM(QUANTITY) QUANTITY " + \
                    "FROM PICKS WHERE TIME_PICKED IS NULL " + \
                    "GROUP BY BIN_LOCATION ORDER BY BIN_LOCATION"

            df = pd.read_sql(query, self.engine)
            print("Zone to Pick")
            for x in range(int(df.size/2)):
                print(df.iat[x,0] + "\tPicks: " + str(df.iat[x,1]))
            bin_picked = input("Pick Bin: ")
            command = "0"
        return bin_picked.upper()

    def pick_parts(self, bin_picked):
        # When you choose location, you will be prompted to enter a valid tote location
        # This will be the location that the item will be placed at
        tote_name = input("Enter Tote Location: ")
        #tote_name = "PICK GREY_TOTE_100"
        tote_bin, tote_zone = tote_name.split(' ', 1)

        query = "SELECT DISTINCT ZONE_lOCATION FROM PICKS WHERE BIN_LOCATION = '"+bin_picked+"' AND PICK_STATUS = 'N' ORDER BY ZONE_LOCATION"
        zone_location_list_df = pd.read_sql(query, self.engine)

        list_loop = 0
        zone_loop = 0
        while list_loop != zone_location_list_df.size:
            zone_loc = zone_location_list_df.iat[list_loop,0]
            query = "SELECT ORDER_ID, PRODUCT_ID, QUANTITY, ZONE_LOCATION FROM PICKS " \
                    "WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' ORDER BY ZONE_LOCATION, ORDER_ID"
            zone_list_df = pd.read_sql(query, self.engine)
            #print(zone_list_df)
            #print(zone_list_df.size)
            print("Go to Area: " + zone_loc)
            input_loc = input("Scan Location: ")

            if(zone_loc == input_loc):
                print("Correct Location")
                while zone_loop != (int(zone_list_df.size / 4)):
                    order_id = zone_list_df.iat[zone_loop,0]
                    product_id = zone_list_df.iat[zone_loop,1]
                    quantity = zone_list_df.iat[zone_loop,2]
                    zone_loc = zone_list_df.iat[zone_loop,3]
                    bin_loc = zone_loc[0]
                    self.scan_parts(product_id, bin_loc, zone_loc, tote_bin, tote_zone)
                    zone_loop += 1
            else:
                print("Wrong Location")

            zone_loop = 0                       
            list_loop += 1
        
    def scan_parts(self, product_id, bin_loc, zone_loc, tote_bin, tote_zone):
        print("Product ID: " + str(product_id))
        product_scan = input("Scan Item: ")
        if(str(product_id) == product_scan):
            ''' Procedure will execute and pick the part for the worker'''
            print("Correct Part Scanned")
            cursor = self.connection.cursor()
            query = "BEGIN PACKAGE_PICKS.PROCESS_PICKS(" + str(product_id) + ", 1, '" + bin_loc + "', '" + zone_loc + \
                "', '" + tote_bin + "', '" + tote_zone +"'); commit; END;"
            result = cursor.execute(query)
            #print(query)
        else:
            print("Part Not Correct")
        
    def staging_parts(self):
        command = ""
        query = ""
        print("Scan Tote")
        while(command != '0'):
            print("asd")
            command = "0"

    def process_order(self):
        command = ""
        query = "SELECT ORDER_ID FROM ORDERS WHERE ORDER_DATE IS NOT NULL AND SHIP_DATE IS NULL ORDER BY ORDER_DATE"
            
            














