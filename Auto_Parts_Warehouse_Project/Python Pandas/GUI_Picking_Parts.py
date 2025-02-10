import oracledb
import pandas as pd
import customtkinter
import tkinter
from sqlalchemy import create_engine


'''
    TODO:
    1. Make sure you can return back to the previous class. You will need to return the current frame when exiting windows
    2. Allow the user to change totes. There's a chance it can be filled all the way to the top
    3. Add the shortcuts onto the screen. 'F5' to allow quantity. 'F3' to exit from the window, etc
    4. Check for 'self.root.bind('<F5>', self.enable_qty_input)'. There's a chance this will carry over for other windows
'''

class Picking_Parts_Window:
    engine = ""
    cs = ""
    connection = ""
    name = ""
    root = ""
    label = ""
    #entry1 = ""


    def __init__(self, name, connection, engine, root, frame2):
        self.name = name
        self.connection = connection
        self.engine = engine
        self.root = root
        self.frame2 = frame2


    def update_product_view(self):
        zone_loc = self.zone_loc
        #query = "SELECT ORDER_ID, PRODUCT_ID, SUM(QUANTITY), ZONE_LOCATION FROM PICKS " \
        #"WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' GROUP BY ORDER_ID, PRODUCT_ID, ZONE_LOCATION ORDER BY ZONE_LOCATION, ORDER_ID"

        query = "SELECT PRODUCT_ID, SUM(QUANTITY), ZONE_LOCATION FROM PICKS " \
        "WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' GROUP BY PRODUCT_ID, ZONE_LOCATION ORDER BY ZONE_LOCATION"
        self.product_zone_list = pd.read_sql(query, self.engine)

        #order_id = self.product_zone_list.iat[0,0]
        #print(self.product_zone_list)
        #print(self.product_zone_list.size)
        if(self.product_zone_list.size == 0):
            #return back to
            self.go_to_zone_location(self.bin_pick_frame)
            print("Go back")
        else:
            product_id = self.product_zone_list.iat[0,0]
            qty = self.product_zone_list.iat[0,1]
            zone_loc = self.product_zone_list.iat[0,2]
            bin_loc = self.bin_picked
            self.loc = zone_loc

            #print("Order ID: " + str(order_id))
            #print("Product ID: " + str(product_id))
            #print("Quantity: " + str(qty))
            #print("Zone: " + zone_loc)
            #print(bin_loc)

            #print(self.bin_pick_frame_order_id.get())
            #self.bin_pick_frame_order_id.configure(text = "Order ID: " + str(order_id))
            self.bin_pick_frame_product.configure(text = "Product: " + str(product_id))
            self.bin_pick_frame_quantity.configure(text = "QTY: " + str(qty))
            self.bin_pick_frame_zone.configure(text = bin_loc + " " + zone_loc)
        
        
    def check_product(self,event):
        input_product_id = self.bin_pick_frame_entry1.get()
        input_qty = self.bin_pick_frame_qty_entry.get()

        product_id = self.product_zone_list.iat[self.zone_list_i,0]
        zone_loc = self.zone_loc
        bin_loc = self.bin_picked
        tote_zone = self.tote_zone
        print(input_product_id)
        print(product_id)
        if(str(input_product_id) == str(product_id)):
            query = "SELECT PACKAGE_PICKS.CHECK_QUANTITY_INPUT("+str(product_id)+", "+str(input_qty)+", '"+bin_loc+"', '"+zone_loc+"') FROM DUAL"
            print(query)
            qty_result = pd.read_sql(query, self.engine).iat[0,0]
            if(qty_result == 1):
                size = len(input_product_id)
                self.bin_pick_frame_entry1.delete(0,size)
                size = len(input_qty)
                self.bin_pick_frame_qty_entry.delete(0,size)
                self.bin_pick_frame_qty_entry.insert(0, '1')
                cursor = self.connection.cursor()
                query = "BEGIN PACKAGE_PICKS.PROCESS_PICKS(" + str(product_id) + ", 1, "+str(input_qty)+", '" + bin_loc + "', '" + zone_loc + \
                    "', 'PICK', '" + tote_zone +"'); commit; END;"
                result = cursor.execute(query)
                self.update_product_view()
        else:
            #print("------------------------- Check Here -----------------------------")
            #print(self.bin_pick_frame_entry1)
            #print(self.bin_pick_frame_entry1.size)
            #print("------------------------ End Check Here ---------------------------")
            size = len(input_product_id)
            self.bin_pick_frame_entry1.delete(0,size)
            size = len(input_qty)
            self.bin_pick_frame_qty_entry.delete(0,size)
            self.bin_pick_frame_qty_entry.insert(0, '1')
        
        
    # bin_name = self.bin_picked
    # zone_name = zone_loc
    
    def load_bin_pick_view(self, zone_loc):
        self.go_to_frame.destroy()
        
        #bin_picked = self.bin_picked
        bin_loc = self.bin_picked
        #self.pick_frame.destroy()
        self.zone_list_i = 0
        
        self.bin_pick_frame = customtkinter.CTkFrame(master = self.root)
        self.bin_pick_frame.pack(pady=30, padx=10)

        self.bin_pick_frame_label_1 = customtkinter.CTkLabel(master=self.bin_pick_frame, text="Picking List", font=("Roboto", 34)).pack(pady=30, padx=10)

        #bin_loc = bin_picked
        
        #query = "SELECT ORDER_ID, PRODUCT_ID, SUM(QUANTITY), ZONE_LOCATION FROM PICKS " \
        #        "WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' GROUP BY ORDER_ID, PRODUCT_ID, ZONE_LOCATION ORDER BY ZONE_LOCATION, ORDER_ID"
        query = "SELECT PRODUCT_ID, SUM(QUANTITY), ZONE_LOCATION FROM PICKS " \
                "WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' GROUP BY PRODUCT_ID, ZONE_LOCATION ORDER BY ZONE_LOCATION"
        self.product_zone_list = pd.read_sql(query, self.engine)
        
        #order_id = self.product_zone_list.iat[self.zone_list_i,0]
        product_id = self.product_zone_list.iat[self.zone_list_i,0]
        quantity = self.product_zone_list.iat[self.zone_list_i,1]
        

        #display_order_id = "Order ID: " + str(order_id)
        #self.bin_pick_frame_order_id = customtkinter.CTkLabel(master=self.bin_pick_frame, text=display_order_id, font=("Roboto", 20))
        #self.bin_pick_frame_order_id.pack(pady=2, padx=10)
        #print(self.bin_pick_frame_order_id)

        display_product = "Product: " + str(product_id)
        self.bin_pick_frame_product = customtkinter.CTkLabel(master=self.bin_pick_frame, text=display_product, font=("Roboto", 20))
        self.bin_pick_frame_product.pack(pady=2, padx=10)

        display_quantity = "QTY: " + str(quantity)
        self.bin_pick_frame_quantity = customtkinter.CTkLabel(master=self.bin_pick_frame, text=display_quantity, font=("Roboto", 20))
        self.bin_pick_frame_quantity.pack(pady=2, padx=10)

        display_location = bin_loc + " " +zone_loc
        self.bin_pick_frame_zone = customtkinter.CTkLabel(master=self.bin_pick_frame, text=display_location, font=("Roboto", 20))
        self.bin_pick_frame_zone.pack(pady=2, padx=10)

        self.bin_pick_frame_scan_product = customtkinter.CTkLabel(master=self.bin_pick_frame, text="Scan Product", font=("Roboto", 20))
        self.bin_pick_frame_scan_product.pack(pady=4, padx=10)

        self.bin_pick_frame_entry1 = customtkinter.CTkEntry(master=self.bin_pick_frame, justify='center')
        self.bin_pick_frame_entry1.pack(pady=4, padx=10)
        self.bin_pick_frame_entry1.bind('<Return>', self.check_product)

        self.bin_pick_frame_qty_input = customtkinter.CTkLabel(master=self.bin_pick_frame, text="Enter Quantity", font=("Roboto", 20))
        self.bin_pick_frame_qty_input.pack(pady=4, padx=10)

        self.bin_pick_frame_qty_entry = customtkinter.CTkEntry(master=self.bin_pick_frame, justify='center')
        self.bin_pick_frame_qty_entry.insert(0, '1')
        self.bin_pick_frame_qty_entry.pack(pady=4, padx=10)
        self.bin_pick_frame_qty_entry.bind('<Return>', self.check_product)
        self.bin_pick_frame_qty_entry.configure(state='disabled')

        self.root.bind('<F5>', self.enable_qty_input)
        #self.bin_pick_frame_qty_entry.bind('<Return>', self.check_product)
        
        raise_frame(self.bin_pick_frame)

    def enable_qty_input(self, event):
        state_condition = self.bin_pick_frame_qty_entry.cget("state")
        if(state_condition == 'disabled'):
            self.bin_pick_frame_qty_entry.configure(state='normal')
        elif(state_condition == 'normal'):
            num = self.bin_pick_frame_qty_entry.get()
            if(len(num) == 0):
                self.bin_pick_frame_qty_entry.insert(0, '1')
            self.bin_pick_frame_qty_entry.configure(state='disabled')
        #self.bin_pick_frame_qty_entry.configure(state='disabled')

    def check_zone_location(self, event):
        input_zone = self.go_to_frame_entry_1.get().upper()

        if(self.zone_loc == input_zone):
            self.load_bin_pick_view(input_zone)
        else:
            size = len(input_zone)
            self.go_to_frame_entry_1.delete(0,size)
            

    def go_to_zone_location(self, other_frame):
        if(other_frame is None):
            self.tote_pick_frame.destroy()
        else:
            print(other_frame)
            other_frame.destroy()
            print("Remove Frame")

        self.go_to_frame = customtkinter.CTkFrame(master = self.root)
        self.go_to_frame.pack(pady=30, padx=10)
        
        bin_picked = self.bin_picked
        #print(bin_picked)
        query = "SELECT DISTINCT ZONE_lOCATION FROM PICKS WHERE BIN_LOCATION = '"+bin_picked+"' AND PICK_STATUS = 'N' ORDER BY ZONE_LOCATION"
        print("------------------")
        print("Query: " + query)
        zone_location_list = pd.read_sql(query, self.engine)
        print(zone_location_list)
        print(zone_location_list.size)
        if(zone_location_list.size == 0):
            print("Going back to load_picking_view")
            self.load_picking_view(self.go_to_frame)
        else:
            self.zone_loc = zone_location_list.iat[0,0]
            zone_loc = zone_location_list.iat[0,0]
            
            query = "SELECT ORDER_ID, PRODUCT_ID, QUANTITY, ZONE_LOCATION FROM PICKS " \
                        "WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' ORDER BY ZONE_LOCATION, ORDER_ID"

            self.zone_list = pd.read_sql(query, self.engine)
            #print(self.zone_list)

            self.go_to_frame_label_1 = customtkinter.CTkLabel(master=self.go_to_frame, text="Go to location: "+zone_loc, font=("Roboto", 34)).pack(pady=30, padx=10)

            self.go_to_frame_entry_1 = customtkinter.CTkEntry(master=self.go_to_frame)
            self.go_to_frame_entry_1.pack(pady=12, padx=10)
            self.go_to_frame_entry_1.bind('<Return>', self.check_zone_location)
            
            raise_frame(self.go_to_frame)
            print("-------------")


    def check_tote(self, event):
        tote_bin = 'PICK'
        tote_zone = self.tote_pick_frame_tote_entry_1.get()
        self.tote_zone = tote_zone

        check_tote_query = "SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('PICK', '" +tote_zone+"') FROM DUAL"
        tote_result = pd.read_sql(check_tote_query, self.engine).iat[0,0]

        if(tote_result == 1):
            self.go_to_zone_location(None)
            #check_tote_empty_query = "SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = '"+tote_zone+"'"
            #tote_empty_result = pd.read_sql(check_tote_empty_query, self.engine).iat[0,0]
        else:
            size = len(tote_zone)
            self.tote_pick_frame_tote_entry_1.delete(0,size)
        #if(tote_result == 1 and tote_empty_result > 0):
        #    self.go_to_zone_location(None)
        #else:
        #    size = len(tote_zone)
        #    self.tote_pick_frame_tote_entry_1.delete(0,size)
        #print("ASD")
        

    def input_pick_tote(self):
        self.pick_frame.destroy()

        self.tote_pick_frame = customtkinter.CTkFrame(master = self.root)
        self.tote_pick_frame.pack(pady=30, padx=10)

        self.tote_pick_frame_label_1 = customtkinter.CTkLabel(master=self.tote_pick_frame, text="Scan Tote", font=("Roboto", 34)).pack(pady=30, padx=10)

        # Work on the tote name
        self.tote_pick_frame_tote_entry_1 = customtkinter.CTkEntry(master=self.tote_pick_frame)
        self.tote_pick_frame_tote_entry_1.pack(pady=12, padx=10)
        self.tote_pick_frame_tote_entry_1.bind('<Return>', self.check_tote)
        
        raise_frame(self.tote_pick_frame)
        

        
    def check_picking_view(self, event):
        self.bin_picked = self.pick_frame_entry_1.get().upper()
        #print("Entry: " + bin_picked)
        #print(self.pick_list)
        size = len(self.bin_picked)
        self.pick_frame_entry_1.delete(0,size)

        for i in range(0,int(self.pick_list.size/2)):
            if(str(self.pick_list.iat[i,0]) == self.bin_picked):
                #print("Correct Input")
                self.input_pick_tote()
                #self.load_bin_pick_view(bin_picked)

        
    def load_picking_view(self, other_frame):
        if(other_frame is None):
            self.frame2.destroy()
        else:
            other_frame.destroy()
            print("Remove Frame")

        self.pick_frame = customtkinter.CTkFrame(master = self.root)
        self.pick_frame.pack(pady=30, padx=10)

        self.pick_frame_label_1 = customtkinter.CTkLabel(master=self.pick_frame, text="Picking View", font=("Roboto", 34))
        self.pick_frame_label_1.pack(pady=30, padx=10)

        self.pick_frame_entry_1 = customtkinter.CTkEntry(master=self.pick_frame)
        self.pick_frame_entry_1.pack(pady=12, padx=10)

        query = "SELECT BIN_LOCATION, SUM(QUANTITY) QUANTITY " + \
                    "FROM PICKS WHERE TIME_PICKED IS NULL " + \
                    "GROUP BY BIN_LOCATION ORDER BY BIN_LOCATION"

        self.pick_list = pd.read_sql(query, self.engine)
        
        for i in range(int(self.pick_list.size/2)):
            bin_name = self.pick_list.iat[i,0]
            qty = self.pick_list.iat[i,1]
            pick_word = bin_name + ":\tPicks: " + str(qty)
            customtkinter.CTkLabel(master=self.pick_frame, text=pick_word, font=("Roboto", 20)).pack(pady=2, padx=10)

        self.pick_frame_entry_1.bind('<Return>', self.check_picking_view)        
        
        raise_frame(self.pick_frame)
     
def raise_frame(frame):
    frame.tkraise()
            
