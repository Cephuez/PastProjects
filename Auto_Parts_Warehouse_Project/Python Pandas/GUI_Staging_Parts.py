import oracledb
import pandas as pd
import customtkinter
import tkinter
from sqlalchemy import create_engine

class Staging_Parts_Window:
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

    def stage_part(self, event):
        print("Check Part")
        quantity_scanned = self.product_info_enter_quantity.get()
        stage_scanned = self.product_info_enter_stage.get()
        
        check_stage_query = "SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('STAGE', '" +stage_scanned+"') FROM DUAL"
        stage_result = pd.read_sql(check_stage_query, self.engine).iat[0,0]

        #STAGE_001
        print(quantity_scanned)
        print(stage_result)

        print(self.quantity)

        if(int(quantity_scanned) <= int(self.quantity) and int(stage_result) == 1):
            # Move parts to Stage Area
            # Employee ID = 1
            query = "BEGIN PACKAGE_ORDER_LIST.MOVE_TOTE_TO_STAGE("+str(self.product_id)+", 1, "+str(quantity_scanned)+", 'PICK', " \
                    "'"+self.tote_zone+"' , 'STAGE' , '"+stage_scanned+"'); commit; END;"
            cursor = self.connection.cursor()
            result = cursor.execute(query)
    
            self.load_stage_product_view(self.product_info_frame)
            
        
        # Run and check if the input part is correct
        # If it's correct, then move the part to the staging area
            # Then run load_stage_product_view
            # Go back to product_view because maybe not all parts could fit in stage shelf
        # IMPORTANT: You will work on F3 shortcut to exit current windows.
        
    def load_product_info(self,other_frame):
        if(other_frame is None):
            self.stage_product_view_frame.destroy()
        else:
            other_frame.destroy()
            
        self.product_info_frame = customtkinter.CTkFrame(master = self.root)
        self.product_info_frame.pack(pady=2, padx=10)

        self.product_info_label = customtkinter.CTkLabel(master=self.product_info_frame, text="Display Product Info", font=("Roboto", 34))
        self.product_info_label.pack(pady=4, padx=10)

        query = "SELECT PRODUCT_ID, COUNT(UNITS) FROM ORDER_LIST WHERE ZONE = '"+self.tote_zone+"' AND PRODUCT_ID = "+self.product_id+" GROUP BY PRODUCT_ID"
        self.quantity = pd.read_sql(query, self.engine).iat[0,1]
        
        display_tote = "Tote: " + self.tote_zone
        self.product_info_show_tote = customtkinter.CTkLabel(master=self.product_info_frame, text=display_tote, font=("Roboto", 20))
        self.product_info_show_tote.pack(pady=4, padx=10)

        display_product = "Product: " + self.product_id
        self.product_info_show_product = customtkinter.CTkLabel(master=self.product_info_frame, text=display_product, font=("Roboto", 20))
        self.product_info_show_product.pack(pady=4, padx=10)

        display_quantity = "QTY: " + str(self.quantity)
        self.product_info_show_quantity = customtkinter.CTkLabel(master=self.product_info_frame, text=display_quantity, font=("Roboto", 20))
        self.product_info_show_quantity.pack(pady=4, padx=10)

        self.product_info_scan_stage = customtkinter.CTkLabel(master=self.product_info_frame, text="Scan Stage Area:", font=("Roboto", 20))
        self.product_info_scan_stage.pack(pady=4, padx=10)  

        self.product_info_enter_stage = customtkinter.CTkEntry(master=self.product_info_frame)
        self.product_info_enter_stage.pack(pady=4, padx=10)
        self.product_info_enter_stage.bind('<Return>', self.stage_part)

        self.product_info_display_quantity = customtkinter.CTkLabel(master=self.product_info_frame, text="Enter Quantity", font=("Roboto", 20))
        self.product_info_display_quantity.pack(pady=4, padx=10)  

        self.product_info_enter_quantity = customtkinter.CTkEntry(master=self.product_info_frame)
        self.product_info_enter_quantity.insert(0, '1')
        self.product_info_enter_quantity.pack(pady=4, padx=10)
        self.product_info_enter_quantity.bind('<Return>', self.stage_part)
        self.product_info_enter_quantity.configure(state='disabled')

        self.root.bind('<F5>', self.enable_qty_input)
        
        raise_frame(self.product_info_frame)

    def enable_qty_input(self, event):
        state_condition = self.product_info_enter_quantity.cget("state")
        if(state_condition == 'disabled'):
            self.product_info_enter_quantity.configure(state='normal')
        elif(state_condition == 'normal'):
            num = self.product_info_enter_quantity.get()
            if(len(num) == 0):
                self.product_info_enter_quantity.insert(0, '1')
            self.product_info_enter_quantity.configure(state='disabled')
        
    def check_product_scanned(self, event):
        self.product_id = self.stage_product_view_entry.get()

        query = "SELECT COUNT(UNITS) FROM ORDER_LIST WHERE ZONE = '"+self.tote_zone+"' AND PRODUCT_ID = "+self.product_id +" ORDER BY PRODUCT_ID"
        product_count = pd.read_sql(query, self.engine).iat[0,0]

        if(product_count > 0):
            print("Item in there")
            self.load_product_info(None)
        else:
            print("No item")

    def load_stage_product_view(self, other_frame):
        if(other_frame is None):
            self.staging_view_frame.destroy()
        else:
            other_frame.destroy()
            print("Remove Frame")

        self.stage_product_view_frame = customtkinter.CTkFrame(master = self.root)
        self.stage_product_view_frame.pack(pady=30, padx=10)

        self.stage_product_view_label = customtkinter.CTkLabel(master=self.stage_product_view_frame, text="Tote View", font=("Roboto", 34))
        self.stage_product_view_label.pack(pady=30, padx=10)

        self.stage_product_view_show_tote = customtkinter.CTkLabel(master=self.stage_product_view_frame, text="Tote: " + self.tote_zone, font=("Roboto", 20))
        self.stage_product_view_show_tote.pack(pady=5, padx=10)

        self.stage_product_view_label_2 = customtkinter.CTkLabel(master=self.stage_product_view_frame, text="Scan Product", font=("Roboto", 20))
        self.stage_product_view_label_2.pack(pady=5, padx=10)

        self.stage_product_view_entry = customtkinter.CTkEntry(master=self.stage_product_view_frame)
        self.stage_product_view_entry.pack(pady=5, padx=10)
        self.stage_product_view_entry.bind('<Return>', self.check_product_scanned)        

        raise_frame(self.stage_product_view_frame)

    def check_tote_item_list(self, event):
        print("Will check tote here")
        tote_zone = self.tote_name_entry.get()
        check_tote_query = "SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('PICK', '" +tote_zone+"') FROM DUAL"
        tote_result = pd.read_sql(check_tote_query, self.engine).iat[0,0]
        self.tote_zone = tote_zone

        if(tote_result == 1):
            check_tote_empty_query = "SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = '"+tote_zone+"'"
            tote_empty_result = pd.read_sql(check_tote_empty_query, self.engine).iat[0,0]

        if(tote_result == 1 and tote_empty_result > 0):
            # Continue rest of procedure here
            self.load_stage_product_view(None)
        else:
            print("Incorrrect Tote Or Is Empty")
        

    def load_staging_view(self, other_frame):
        if(other_frame is None):
            self.frame2.destroy()
        else:
            other_frame.destroy()
            print("Remove Frame")

        self.staging_view_frame = customtkinter.CTkFrame(master = self.root)
        self.staging_view_frame.pack(pady=30, padx=10)

        self.staging_view_label = customtkinter.CTkLabel(master=self.staging_view_frame, text="Staging View", font=("Roboto", 34))
        self.staging_view_label.pack(pady=30, padx=10)

        self.scan_tote_label = customtkinter.CTkLabel(master=self.staging_view_frame, text="Scan Tote: ", font=("Roboto", 34))
        self.scan_tote_label.pack(pady=30, padx=10)

        self.tote_name_entry = customtkinter.CTkEntry(master=self.staging_view_frame)
        self.tote_name_entry.pack(pady=12, padx=10)
        self.tote_name_entry.bind('<Return>', self.check_tote_item_list)

        raise_frame(self.staging_view_frame)

        
def raise_frame(frame):
    frame.tkraise()
