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


    def generate_order_dates(self):
        cursor = self.connection.cursor()
        # Jan 24 - 28 Day
        # 'DD-01-2025 10:10:45'
        # 06:00:00 - 20:00:00

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
            
        jan_day_list = [24,25,26,27,28]
        feb_day_list = [3,4,5,6,7]
        cursor = self.connection.cursor()

        # 002-100 - Jan 24 2025
        #   - 002-010 : 08:00:00 - 08:59:59
        #   - 011-020 : 09:00:00 - 09:59:59
        #   - 021-030 : 10:00:00 - 10:59:59
        # 101-200 - Jan 25 2025
        # 201-300 - Jan 26 2025
        # etc
        # Generate 10 orders for every hour
        for x in range(17,23):
            day = str(x)
            # 933 
            hundredth = 9 + x - 17
            for y in range(9,19):
                old_minute = -1
                old_second = -1
                hour = str(y)
                tenth = 3 + y - 9
                for i in range(2,12):
                    order_id = i + (10 * tenth) + (100 * hundredth)

                    if(order_id > 1):
                        while(True):
                            if(old_minute == 59):
                                break
                            generate_minute = random.randint((i-2)*5,(i-2)*5+10)
                            if(old_minute <= generate_minute):
                                break
                        while(True):
                            if(old_second == 59):
                                break
                            generate_second = random.randint((i-2)*5,(i-2)*5+10)
                            if(old_second <= generate_second):
                                break
                        date = ""+day+"-02-2025 "+ ""+hour+":"+str(generate_minute)+":"+str(generate_second)+""

                        query = "UPDATE ORDERS SET ORDER_DATE = TO_DATE('"+date+"', 'DD-MM-YYYY HH24:MI:SS') WHERE ORDER_ID = " +str(order_id)

                        print(query)
                        old_minute = generate_minute
                        old_second = generate_second

                        #print(query)
                        result = cursor.execute(query)
                        #result = pd.read_sql(query, self.engine)
                        self.connection.commit()
                        #print(query)

    def get_current_order_id(self):
        query = "SELECT MAX(ORDER_ID) FROM ORDERS"
        return pd.read_sql(query, self.engine).iat[0,0]

    def generate_orders(self):
        # 100 of each
        query = "SELECT MAX(ORDER_ID) FROM ORDERS"
        order_id = (pd.read_sql(query, self.engine).iat[0,0] + 1)
        print(order_id)
        old_product_id = 0
        cursor = self.connection.cursor()
        print("Enter 'Y' for Yes")

        # Added a lot of check statements so I don't accidently add more code than usual
        #input_command = input("You want to generate? ")
        if(input_command != 'Y'):
            exit(0)
        input_command = input("Are you sure? ")
        if(input_command != 'Y'):
            exit(0)
        input_command = input("Last check?: ")
        if(input_command != 'Y'):
            exit(0)

        # ------------------------Change order id------------------------------------
        for i in range(order_id, order_id + 500):
            #print("Loop:" + str(i))
            customer_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            customer_id = random.choice(customer_list)

            # -------------------Change this for later products-------------------------
            quantity_list = [1,2]
            
            query = "BEGIN PACKAGE_ORDERS.CREATE_NEW_ORDER("+str(customer_id)+"); COMMIT; END;"
            #print("Create Order: "+query)
            result = cursor.execute(query)
            for x in range(3):

                # -------------------Change this for different products----------------------
                product_id_list_1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,
                                     20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
                qty = random.choice(quantity_list)
                while(True):
                    product_id = random.choice(product_id_list_1)
                    if(product_id != old_product_id):
                        old_product_id = product_id
                        break
                
                query = "BEGIN PACKAGE_CUSTOMER_ORDERS.ADD_PRODUCT_TO_ORDER("+str(i)+","+str(product_id)+","+str(qty)+"); COMMIT; END;"
                #print(query)
                result = cursor.execute(query)
            
            query = "BEGIN PACKAGE_CUSTOMER_ORDERS.CONFIRM_CUSTOMER_ORDER("+str(i)+"); COMMIT; END;"
            #print("Confirm Order: "+query)
            result = cursor.execute(query)

        for i in range(order_id + 500, order_id + 500 + 100):
            #print("Loop:" + str(i))
            customer_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            customer_id = random.choice(customer_list)

            # -------------------Change this for later products-------------------------
            quantity_list = [1,2]
            
            query = "BEGIN PACKAGE_ORDERS.CREATE_NEW_ORDER("+str(customer_id)+"); COMMIT; END;"
            #print("Create Order: "+query)
            result = cursor.execute(query)
            for x in range(3):

                # -------------------Change this for different products----------------------
                product_id_list_1 = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,
                                     20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]
                qty = random.choice(quantity_list)
                while(True):
                    product_id = random.choice(product_id_list_1)
                    if(product_id != old_product_id):
                        old_product_id = product_id
                        break
                
                query = "BEGIN PACKAGE_CUSTOMER_ORDERS.ADD_PRODUCT_TO_ORDER("+str(i)+","+str(product_id)+","+str(qty)+"); COMMIT; END;"
                #print(query)
                result = cursor.execute(query)
            
            query = "BEGIN PACKAGE_CUSTOMER_ORDERS.CONFIRM_CUSTOMER_ORDER("+str(i)+"); COMMIT; END;"
            #print("Confirm Order: "+query)
            result = cursor.execute(query)
        
        #product_id_list_2 = [33, 15, 13, 16, 12]
        #product_id_list_3 = [37, 26, 25, 22, 32]
        #product_id_list_4 = [38, 27, 23, 17, 6]
        #product_id_list_5 = [19, 43, 42, 40, 41]
        #product_id_list_6 = [4, 9, 28, 3, 39]
        #product_id_list_7 = [18, 30, 36, 44, 8]
        #product_id_list_8 = [7, 14, 21, 10, 11]
        #product_id_list_9 = [5, 20, 24, 2, 1]

