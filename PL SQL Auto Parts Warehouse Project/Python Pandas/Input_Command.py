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
            #command = input("Enter your Command: ")
            command = "3"
            if(command == "1"):
                print("Picking List")
                self.picking_command()
            elif(command == "2"):
                print("Stage Items")
                self.staging_parts()
            elif(command == "3"):
                print("Process Orders")
                self.process_orders()
            elif(command == "4"):
                print("Move Parts")
            elif(command == "5"):
                print("Process Receiving Items")
            elif(command == "0"):
                print("Closing Program")
            else:
                print("Wrong Input")
            command = "0"


    def process_orders(self): 
        print("XD")
        while(True):
            get_orders_query = "SELECT DISTINCT(ORDER_ID) FROM ORDERS_READY ORDER BY ORDER_ID"
            all_order_list = pd.read_sql(get_orders_query, self.engine)
            print("Orders Ready To Be Processed")
            for i in range(all_order_list.size):
                print("Order ID: " + str(all_order_list.iat[i,0]))

            #order_id = input("Pick Order ID: ")
            order_id = 15
            print("Pick Order ID: "+ str(order_id))

            #comp_box = input("Scan Order Box: ")
            comp_box = "ORDER_TOTE_00005"
            print("Scan Order Box: " + comp_box)
            get_order_list_query = "SELECT DISTINCT ZONE FROM ORDERS_READY WHERE ORDER_ID = "+str(order_id)+" ORDER BY ZONE"
            order_list = pd.read_sql(get_order_list_query, self.engine)
            print(order_list)

            
            for i in range(order_list.size):
                while(True):
                    zone_loc = order_list.iat[i,0]
                    print("Go to Zone: " + zone_loc)
                    zone_scanned = input("Scan Zone: ").upper()
                    if(zone_loc == zone_scanned):
                        print("Correct Zone")
                        self.move_to_process(order_id, zone_loc, comp_box)
                        break
                    else:
                        print("Incorrect Zone")
                

    def move_to_process(self, order_id, zone_loc, comp_box):
        #print("Move the parts to process")
        query = "SELECT PRODUCT_ID, QUANTITY FROM ORDERS_READY WHERE ZONE = '"+ zone_loc +"'"
        stage_list = pd.read_sql(query, self.engine)
        for i in range(int(stage_list.size / 2)):
            while(True):
                print("Scan Product: " + str(stage_list.iat[i,0]))
                part_scanned = input("Part: ")
                if(part_scanned == str(stage_list.iat[i,0])):
                    print("Correct Part Scanned")
                    break
                else:
                    print("Wrong part Scanned")
            
            #print("Scan Part: " + str(stage_list.iat[i,0]))
        print(stage_list)
    '''
        The user will scan the tote which will allow the worker to move the parts from the
        box to the shelfs(Stage)
    '''
    def staging_parts(self):
        command = ""
        query = ""
        #tote_name = input("Scan Tote: ")
        tote_bin = 'PICK'
        #tote_zone = 'GREY_TOTE_101'

        while(True):
            tote_zone = input("Scan Tote: ")

            check_tote_query = "SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('PICK', '" +tote_zone+"') FROM DUAL"
            tote_result = pd.read_sql(check_tote_query, self.engine).iat[0,0]

            if(tote_result == 1):
                check_tote_empty_query = "SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = '"+tote_zone+"'"
                tote_empty_result = pd.read_sql(check_tote_empty_query, self.engine).iat[0,0]

            if(tote_result == 1 and tote_empty_result > 0):
                # Continue rest of procedure here
                print("Stuff in tote")
                self.move_to_staging(tote_zone)
                print(tote_zone + " now empty")
            else:
                print("Incorrrect Tote Or Is Empty")

            
            
            query = "SELECT PRODUCT_ID FROM ORDER_LIST " +\
                    "WHERE BIN = 'PICK' AND ZONE = '"+tote_zone+"' ORDER BY PRODUCT_ID"

    '''
        The code will run procedure PACKAGE_ORDER_LIST.MOVE_TOTE_TO_STAGE, to move the parts from their box
        to the staging shelfs.
    '''
    def move_to_staging(self, tote_zone):
        query = "SELECT PRODUCT_ID FROM ORDER_LIST " +\
                "WHERE BIN = 'PICK' AND ZONE = '"+tote_zone+"' ORDER BY PRODUCT_ID"
        product_list = pd.read_sql(query, self.engine)
        for x in range(product_list.size):
            print("Need Product: " + str(product_list.iat[x,0]))
            while(True):
                part_scanned = input("Scan Part: ")
                if(part_scanned == str(product_list.iat[x,0])):
                    while(True):
                        stage_scanned = input("Scan Stage Area: ").upper()
                        check_stage_query = "SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('STAGE', '" +stage_scanned+"') FROM DUAL"
                        stage_result = pd.read_sql(check_stage_query, self.engine).iat[0,0]

                        # If staging area is correct, then move the part to its new location
                        if(stage_result == 1):
                            #print("Valid Stage Area")
                            # Employee id will remain 1 for now
                            query = "BEGIN " + \
                                    "PACKAGE_ORDER_LIST.MOVE_TOTE_TO_STAGE("+str(part_scanned)+", 1, 'PICK', '"+tote_zone+"', 'STAGE', '"+stage_scanned+"'); " + \
                                    "commit; END;"
                            cursor = self.connection.cursor()
                            result = cursor.execute(query)
                            break
                        else:
                            print("Incorrect Stage")
                    break
                else:
                    print("Incorrect Part Scanned")

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


    def process_order(self):
        command = ""
        query = "SELECT ORDER_ID FROM ORDERS WHERE ORDER_DATE IS NOT NULL AND SHIP_DATE IS NULL ORDER BY ORDER_DATE"
            
            














