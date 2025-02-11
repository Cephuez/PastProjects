import oracledb
import pandas as pd
import customtkinter
import tkinter
from sqlalchemy import create_engine

class Gather_Parts_Window:
    engine = ""
    cs = ""
    connection = ""
    name = ""
    root = ""
    label = ""
    #entry1 = ""


    def __init__(self, gui_application, name, connection, engine, root, frame2):
        self.gui_application = gui_application
        self.name = name
        self.connection = connection
        self.engine = engine
        self.root = root
        self.curr_frame = frame2

    def update_product_view(self):
        print("Update Frame")
        query = "SELECT PRODUCT_ID, COUNT(QUANTITY) FROM ORDERS_READY " \
                "WHERE ORDER_ID = "+self.order_id+" AND ZONE = '"+self.curr_stage+"' GROUP BY PRODUCT_ID ORDER BY PRODUCT_ID"

        shelf_list = pd.read_sql(query, self.engine)

        if(shelf_list.size == 0):
            self.load_staging_view(self.shelf_view_frame)
        else:
            product_id = shelf_list.iat[0,0]
            qty = shelf_list.iat[0,1]
            
            self.shelf_view_product_display.configure(text = "Scan Product: " + str(product_id))
            self.shelf_view_quantity_display.configure(text = "QTY: " + str(qty))


    # ORDER_TOTE_00013
    def check_product(self,event):
        input_product_id = self.shelf_view_product_entry.get()
        input_qty = self.shelf_view_quantity_entry.get()

        if(str(input_product_id) == str(self.product_id)):
            query = "SELECT SUM(QUANTITY) FROM ORDERS_READY WHERE product_id = "+str(input_product_id)+" AND ZONE = '"+self.curr_stage+"'"
            print(query)
            qty_result = pd.read_sql(query, self.engine).iat[0,0]
            print(qty_result)

            if(int(input_qty) <= int(qty_result)):
                # Employee ID: 4
                cursor = self.connection.cursor()
                query = "BEGIN PACKAGE_ORDERS.MOVE_STAGE_TO_BOX("+self.order_id+", "+input_product_id+", 4, "+input_qty+\
                        ", 'STAGE', '"+self.curr_stage+"', 'COMP', '"+self.box_tote+"');"\
                        " commit; END;"
                result = cursor.execute(query)
                self.update_product_view()
                print(query)

    def display_product_in_shelf_view(self, other_frame):
        if(other_frame is None):
            self.staging_view_frame.destroy()
        else:
            other_frame.destroy()

        self.shelf_view_frame = customtkinter.CTkFrame(master = self.root)
        self.shelf_view_frame.pack(pady=30, padx=10)

        self.shelf_view_label = customtkinter.CTkLabel(master=self.shelf_view_frame, text="Pick Part From Shelf", font=("Roboto", 34))
        self.shelf_view_label.pack(pady=2, padx=10)

        query = "SELECT PRODUCT_ID, COUNT(QUANTITY) FROM ORDERS_READY " \
                "WHERE ORDER_ID = "+self.order_id+" AND ZONE = '"+self.curr_stage+"' GROUP BY PRODUCT_ID ORDER BY PRODUCT_ID"

        shelf_list = pd.read_sql(query, self.engine)

        self.product_id = shelf_list.iat[0,0]
        self.quantity = shelf_list.iat[0,1]        

        self.shelf_view_stage_display = customtkinter.CTkLabel(master=self.shelf_view_frame, text=self.curr_stage, font=("Roboto", 20))
        self.shelf_view_stage_display.pack(pady=2, padx=10)    
        
        self.shelf_view_product_display = customtkinter.CTkLabel(master=self.shelf_view_frame, text="Scan Product: " + str(self.product_id), font=("Roboto", 20))
        self.shelf_view_product_display.pack(pady=2, padx=10)

        self.shelf_view_product_entry = customtkinter.CTkEntry(master=self.shelf_view_frame)
        self.shelf_view_product_entry.pack(pady=2, padx=10)
        self.shelf_view_product_entry.bind('<Return>', self.check_product)

        self.shelf_view_quantity_display = customtkinter.CTkLabel(master=self.shelf_view_frame, text="QTY: " + str(self.quantity), font=("Roboto", 20))
        self.shelf_view_quantity_display.pack(pady=2, padx=10)

        self.shelf_view_quantity_entry = customtkinter.CTkEntry(master=self.shelf_view_frame, justify='center')
        self.shelf_view_quantity_entry.insert(0, '1')
        self.shelf_view_quantity_entry.pack(pady=12, padx=10)
        self.shelf_view_quantity_entry.bind('<Return>', self.check_product)
        self.shelf_view_quantity_entry.configure(state='disabled')

        self.root.bind('<F5>', self.enable_qty_input)

        raise_frame(self.shelf_view_frame)

    def enable_qty_input(self, event):
        state_condition = self.shelf_view_quantity_entry.cget("state")
        if(state_condition == 'disabled'):
            self.shelf_view_quantity_entry.configure(state='normal')
        elif(state_condition == 'normal'):
            num = self.shelf_view_quantity_entry.get()
            if(len(num) == 0):
                self.shelf_view_quantity_entry.insert(0, '1')
            self.shelf_view_quantity_entry.configure(state='disabled')
        #self.bin_pick_frame_qty_entry.configure(state='disabled')
            
    def check_stage_input(self,event):
        stage_input = self.staging_view_entry.get()
        if(stage_input == self.curr_stage):
            self.display_product_in_shelf_view(None)

    def load_staging_view(self, other_frame):
        if(other_frame is None):
            self.scan_box_frame.destroy()
        else:
            other_frame.destroy()

        self.staging_view_frame = customtkinter.CTkFrame(master = self.root)
        self.staging_view_frame.pack(pady=30, padx=10)

        query = "SELECT DISTINCT(ZONE) FROM ORDERS_READY WHERE ORDER_ID = "+self.order_id+" ORDER BY ZONE"
        get_stage_list = pd.read_sql(query, self.engine)

        if(get_stage_list.size == 0):
            self.load_gather_parts_view(self.staging_view_frame)
        else:
            self.curr_stage = pd.read_sql(query, self.engine).iat[0,0]

            stage_display = "Scan Stage: " + self.curr_stage
            self.staging_view_display_stage = customtkinter.CTkLabel(master=self.staging_view_frame, text=stage_display, font=("Roboto", 34))
            self.staging_view_display_stage.pack(pady=30, padx=10)

            self.staging_view_entry = customtkinter.CTkEntry(master=self.staging_view_frame)
            self.staging_view_entry.pack(pady=12, padx=10)
            self.staging_view_entry.bind('<Return>', self.check_stage_input)  

            raise_frame(self.staging_view_frame)
        

    def check_input_box(self, event):
        self.box_tote = self.scan_box_entry.get()

        print(self.box_tote)
        query = "SELECT COUNT(*) FROM APPROVED_ZONE WHERE ZONE = '"+self.box_tote+"'"
        tote_exists = pd.read_sql(query, self.engine).iat[0,0]

        query = "SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = '"+self.box_tote+"' AND ORDER_ID != " + str(self.order_id)
        empty_tote = pd.read_sql(query, self.engine).iat[0,0]

        print(tote_exists)
        print(empty_tote)
        if(int(tote_exists) == 1 and int(empty_tote) == 0):
            print("Change")
            self.load_staging_view(None)
            
        
    def load_input_box_view(self, other_frame):
        if(other_frame is None):
            self.gather_parts_frame.destroy()
        else:
            other_frame.destory()

        self.scan_box_frame = customtkinter.CTkFrame(master = self.root)
        self.scan_box_frame.pack(pady=30, padx=10)

        self.scan_box_display = customtkinter.CTkLabel(master=self.scan_box_frame, text="Scan Box: ", font=("Roboto", 34))
        self.scan_box_display.pack(pady=30, padx=10)

        self.scan_box_entry = customtkinter.CTkEntry(master=self.scan_box_frame)
        self.scan_box_entry.pack(pady=12, padx=10)
        self.scan_box_entry.bind('<Return>', self.check_input_box)          
        
        #SELECT COUNT(*) FROM APPROVED_ZONE WHERE ZONE = 'ORDER_TOTE_00011'; -- If 1, then approved box
        #SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = 'ORDER_TOTE_00001' -- If 0, then box can be used

        raise_frame(self.scan_box_frame)

    def check_order_id(self, event):
        self.order_id = self.gather_parts_enter_product.get()
        if(int(self.order_id) in self.order_list):
            self.load_input_box_view(None)
            print("Correct Order ID")
        else:
            print("Wrong Order ID")

    def load_gather_parts_view(self):
        self.curr_frame.destroy()

        self.order_list = []
        self.gather_parts_frame = customtkinter.CTkFrame(master = self.root)
        self.gather_parts_frame.pack(pady=30, padx=10)
        self.curr_frame = self.gather_parts_frame

        self.gather_parts_label = customtkinter.CTkLabel(master=self.gather_parts_frame, text="Orders Ready List", font=("Roboto", 34))
        self.gather_parts_label.pack(pady=30, padx=10)

        self.gather_parts_enter_product = customtkinter.CTkEntry(master=self.gather_parts_frame)
        self.gather_parts_enter_product.pack(pady=12, padx=10)
        self.gather_parts_enter_product.bind('<Return>', self.check_order_id)   

        get_orders_query = "SELECT DISTINCT(ORDER_ID) FROM ORDERS_READY ORDER BY ORDER_ID"
        all_order_list = pd.read_sql(get_orders_query, self.engine)
        list_length = all_order_list.size

        for i in range(list_length):
            if(i == 7):
                break
            order_id = all_order_list.iat[i,0]
            self.order_list.append(int(order_id))
            self.gather_parts_label = customtkinter.CTkLabel(master=self.gather_parts_frame, text="Order: " + str(order_id), font=("Roboto", 20))
            self.gather_parts_label.pack(pady=2, padx=10)            

        raise_frame(self.gather_parts_frame)
        
    def exit_window(self, event):
        self.root.unbind('<F3>', self.bind)
        self.curr_frame.destroy()
        self.gui_application.display_command_window()
        

def raise_frame(frame):
    frame.tkraise()
