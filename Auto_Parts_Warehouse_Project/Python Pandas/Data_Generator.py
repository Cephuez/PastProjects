import oracledb
import pandas as pd
import random
from sys import exit
from sqlalchemy import create_engine

class code_generator:
    engine = ""
    cs = ""
    connection = ""
    def __init__(self, name):
        self.name = name

    def log_in(self):
        #self.user_name = input("User Name: ")
        #self.password = input("Password: ")
        user_name = "Project"
        password = "password123"
        cs = "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1522)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = orclpdb)))"
        self.connection = oracledb.connect( user=user_name, password= password, dsn= cs)
        self.engine = create_engine('oracle+oracledb://', creator=lambda: self.connection)


    def genrate_order_dates(self):
        print("xd")


    def generate_orders(self):
        # 100 of each
        old_product_id = 0
        cursor = self.connection.cursor()
        print("Enter 'Y' for Yes")

        # Added a lot of check statements so I don't accidently add more code than usual
        input_command = input("You want to generate? ")
        if(input_command != 'Y'):
            exit(0)
        input_command = input("Are you sure? ")
        if(input_command != 'Y'):
            exit(0)
        input_command = input("Last check?: ")
        if(input_command != 'Y'):
            exit(0)

        # ------------------------Change order id------------------------------------
        for i in range(801, 901):
            #print("Loop:" + str(i))
            customer_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            customer_id = random.choice(customer_list)

            # -------------------Change this for later products-------------------------
            quantity_list = [1,2,3]
            
            query = "BEGIN PACKAGE_ORDERS.CREATE_NEW_ORDER("+str(customer_id)+"); COMMIT; END;"
            print("Create Order: "+query)
            result = cursor.execute(query)
            for x in range(2):

                # -------------------Change this for different products----------------------
                product_id_list_1 = [5, 20, 24, 2, 1]
                qty = random.choice(quantity_list)
                while(True):
                    product_id = random.choice(product_id_list_1)
                    if(product_id != old_product_id):
                        old_product_id = product_id
                        break
                
                #print("Customer: " + str(customer_id) + "         Product ID: " + str(product_id) + "               QTY: " + str(qty))
                query = "BEGIN PACKAGE_CUSTOMER_ORDERS.ADD_PRODUCT_TO_ORDER("+str(i)+","+str(product_id)+","+str(qty)+"); COMMIT; END;"
                #print("Add Product: " + query)
                result = cursor.execute(query)
            
            query = "BEGIN PACKAGE_CUSTOMER_ORDERS.CONFIRM_CUSTOMER_ORDER("+str(i)+"); COMMIT; END;"
            print("Confirm Order: "+query)
            result = cursor.execute(query)
        #product_id_list_2 = [33, 15, 13, 16, 12]
        #product_id_list_3 = [37, 26, 25, 22, 32]
        #product_id_list_4 = [38, 27, 23, 17, 6]
        #product_id_list_5 = [19, 43, 42, 40, 41]
        #product_id_list_6 = [4, 9, 28, 3, 39]
        #product_id_list_7 = [18, 30, 36, 44, 8]
        #product_id_list_8 = [7, 14, 21, 10, 11]
        #product_id_list_9 = [5, 20, 24, 2, 1]
        print("Hi")
