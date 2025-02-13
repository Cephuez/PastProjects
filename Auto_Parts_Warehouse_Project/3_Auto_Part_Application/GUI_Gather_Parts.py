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
            self.load_staging_view()
        else:
            product_id = shelf_list.iat[0,0]
            qty = shelf_list.iat[0,1]
            self.product_id = product_id
            
            self.shelf_view_product_display.configure(text = "Scan Product: " + str(product_id))
            self.shelf_view_quantity_display.configure(text = "QTY: " + str(qty))


    # ORDER_TOTE_00013
    def check_product(self,event):
        input_product_id = self.shelf_view_product_entry.get()
        input_qty = self.shelf_view_quantity_entry.get()

        if(str(input_product_id) == str(self.product_id)):
            query = "SELECT SUM(QUANTITY) FROM ORDERS_READY WHERE ORDER_ID = "+self.order_id+\
                    " AND PRODUCT_ID = "+str(input_product_id)+" AND ZONE = '"+self.curr_stage+"'"
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

    def display_product_in_shelf_view(self):
        self.curr_frame.destroy()

        shelf_view_frame = customtkinter.CTkFrame(master = self.root)
        shelf_view_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = shelf_view_frame

        shelf_view_label = customtkinter.CTkLabel(shelf_view_frame, text="Pick Part From Shelf", font=("Roboto", 40))
        shelf_view_label.pack(pady=12, padx=10)

        query = "SELECT PRODUCT_ID, COUNT(QUANTITY) FROM ORDERS_READY " \
                "WHERE ORDER_ID = "+self.order_id+" AND ZONE = '"+self.curr_stage+"' GROUP BY PRODUCT_ID ORDER BY PRODUCT_ID"

        shelf_list = pd.read_sql(query, self.engine)

        self.product_id = shelf_list.iat[0,0]
        self.quantity = shelf_list.iat[0,1]        

        customtkinter.CTkLabel(shelf_view_frame, text=self.box_tote, font=("Roboto", 28)).pack(pady=10, padx=10)
        
        customtkinter.CTkLabel(shelf_view_frame, text=self.curr_stage, font=("Roboto", 28)).pack(pady=10, padx=10)

        test_frame = customtkinter.CTkFrame(shelf_view_frame)
        test_frame.pack(side='top', padx=5)

        product_frame = customtkinter.CTkFrame(test_frame)
        product_frame.pack(side='left', anchor='w')
        
        self.shelf_view_product_display = customtkinter.CTkLabel(product_frame, text="Scan Product: " + str(self.product_id), font=("Roboto", 20))
        self.shelf_view_product_display.pack(side='top',pady=5, padx=10)

        self.shelf_view_product_entry = customtkinter.CTkEntry(product_frame, font=("Roboto", 16))
        self.shelf_view_product_entry.pack(pady=5, padx=10)
        self.shelf_view_product_entry.bind('<Return>', self.check_product)
        self.shelf_view_product_entry.focus_set()
        
        quantity_frame = customtkinter.CTkFrame(test_frame)
        quantity_frame.pack(side='right', anchor='e')
        
        self.shelf_view_quantity_display = customtkinter.CTkLabel(quantity_frame, text="QTY: " + str(self.quantity), font=("Roboto", 20))
        self.shelf_view_quantity_display.pack(pady=5, padx=10)

        self.shelf_view_quantity_entry = customtkinter.CTkEntry(quantity_frame, justify='center', width = 40, font=("Roboto", 16))
        self.shelf_view_quantity_entry.insert(0, '1')
        self.shelf_view_quantity_entry.pack(pady=5, padx=10)
        self.shelf_view_quantity_entry.bind('<Return>', self.check_product)
        self.shelf_view_quantity_entry.configure(state='disabled')

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind_exit = self.root.bind('<F3>', self.exit_display_product_view)

        customtkinter.CTkLabel(self.curr_frame, text="F5. QTY", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25) 
        self.bind_qty = self.root.bind('<F5>', self.enable_qty_input)
        

        raise_frame(self.curr_frame)

    def exit_display_product_view(self, event):
        self.root.unbind('<F3>', self.bind_exit)
        self.root.unbind('<F5>', self.bind_qty)
        self.curr_frame.destroy()
        self.load_staging_view()        

    def enable_qty_input(self, event):
        state_condition = self.shelf_view_quantity_entry.cget("state")
        if(state_condition == 'disabled'):
            self.shelf_view_quantity_entry.configure(state='normal')
        elif(state_condition == 'normal'):
            num = self.shelf_view_quantity_entry.get()
            if(len(num) == 0):
                self.shelf_view_quantity_entry.insert(0, '1')
            self.shelf_view_quantity_entry.configure(state='disabled')
            
    def check_stage_input(self,event):
        stage_input = self.staging_view_entry.get()
        if(stage_input == self.curr_stage):
            self.display_product_in_shelf_view()

    def load_staging_view(self):
        self.curr_frame.destroy()

        staging_view_frame = customtkinter.CTkFrame(master = self.root)
        staging_view_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = staging_view_frame

        query = "SELECT DISTINCT(ZONE) FROM ORDERS_READY WHERE ORDER_ID = "+self.order_id+" ORDER BY ZONE"
        get_stage_list = pd.read_sql(query, self.engine)

        if(get_stage_list.size == 0):
            self.root.unbind('<F3>', self.bind)
            self.load_gather_parts_view()
        else:
            self.curr_stage = pd.read_sql(query, self.engine).iat[0,0]

            customtkinter.CTkLabel(staging_view_frame, text="Order ID: " + str(self.order_id), font=("Roboto", 40)).pack(side='top', pady=12, padx=10)

            #scan_stage_frame = customtkinter.CTkFrame(staging_view_frame)
            #scan_stage_frame.pack(side='top', pady=5, padx=10)
            
            stage_display = "Scan Stage: " + self.curr_stage
            customtkinter.CTkLabel(staging_view_frame, text=stage_display, font=("Roboto", 20)).pack(side='top', pady=10, padx=2)

            self.staging_view_entry = customtkinter.CTkEntry(staging_view_frame, font=("Roboto", 16))
            self.staging_view_entry.pack(side='top', pady=12, padx=10)
            self.staging_view_entry.bind('<Return>', self.check_stage_input)
            self.staging_view_entry.focus_set()

            #short_cut_frame = customtkinter.CTkFrame(staging_view_frame)
            #short_cut_frame.pack(side='bottom', pady=20, padx=20)

            #customtkinter.CTkLabel(short_cut_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=30)
            customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
            self.bind = self.root.bind('<F3>', self.exit_load_staging_view)

            raise_frame(self.curr_frame)

    def exit_load_staging_view(self, event):
        self.root.unbind('<F3>', self.bind)
        self.curr_frame.destroy()
        self.load_input_box_view()
        

    def check_input_box(self, event):
        self.box_tote = self.scan_box_entry.get()

        query = "SELECT COUNT(*) FROM APPROVED_ZONE WHERE ZONE = '"+self.box_tote+"'"
        tote_exists = pd.read_sql(query, self.engine).iat[0,0]

        query = "SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = '"+self.box_tote+"' AND ORDER_ID != " + str(self.order_id)
        empty_tote = pd.read_sql(query, self.engine).iat[0,0]

        if(int(tote_exists) == 1 and int(empty_tote) == 0):
            self.load_staging_view()
            
        
    def load_input_box_view(self):
        self.curr_frame.destroy()

        box_display_frame = customtkinter.CTkFrame(master = self.root)
        box_display_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = box_display_frame

        customtkinter.CTkLabel(box_display_frame, text="Order ID: " + str(self.order_id), font=("Roboto", 40)).pack(side='top', pady=12, padx=10)

        scan_box_frame = customtkinter.CTkFrame(box_display_frame)
        scan_box_frame.pack(side='top', anchor = 'w', pady=10, padx=30)

        customtkinter.CTkLabel(scan_box_frame, text="Scan Box: ", font=("Roboto", 20)).pack(side='left', anchor='w', pady=10, padx=10)

        self.scan_box_entry = customtkinter.CTkEntry(scan_box_frame, font=("Roboto", 16), width = 220)
        self.scan_box_entry.pack(side='left', anchor='w', pady=12, padx=10)
        self.scan_box_entry.bind('<Return>', self.check_input_box)
        self.scan_box_entry.focus_set()

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind = self.root.bind('<F3>', self.exit_load_input_box_view)

        raise_frame(self.curr_frame)

    def exit_load_input_box_view(self, event):
        self.root.unbind('<F3>', self.bind)
        self.curr_frame.destroy()
        self.load_gather_parts_view()

    def check_order_id(self, event):
        self.order_id = self.gather_parts_enter_product.get()
        if(int(self.order_id) in self.order_list):
            self.load_input_box_view()
            print("Correct Order ID")
        else:
            print("Wrong Order ID")

    def load_gather_parts_view(self):
        self.curr_frame.destroy()

        self.order_list = []
        self.i = 0
        self.box_tote = ""
        gather_parts_frame = customtkinter.CTkFrame(master = self.root)
        gather_parts_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = gather_parts_frame

        customtkinter.CTkLabel(gather_parts_frame, text="Orders Ready List", font=("Roboto", 40)).pack(side='top', pady=12, padx=10)

        enter_order_id_frame = customtkinter.CTkFrame(gather_parts_frame)
        enter_order_id_frame.pack(side='top', anchor = 'w', pady=5, padx=30)

        customtkinter.CTkLabel(enter_order_id_frame, text="Order: ", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=10)

        self.gather_parts_enter_product = customtkinter.CTkEntry(enter_order_id_frame, font=("Roboto", 16), width = 80)
        self.gather_parts_enter_product.pack(pady=1, padx=1)
        self.gather_parts_enter_product.bind('<Return>', self.check_order_id)
        self.gather_parts_enter_product.focus_set()

        get_orders_query = "SELECT DISTINCT(ORDER_ID) FROM ORDERS_READY ORDER BY ORDER_ID"
        all_order_list = pd.read_sql(get_orders_query, self.engine)
        list_length = all_order_list.size

        self.order_id_list_frame = customtkinter.CTkFrame(gather_parts_frame)
        self.order_id_list_frame.pack(side='top', anchor = 'w', pady=10, padx=30)
        
        for i in range(list_length):
            order_id = all_order_list.iat[i,0]
            self.order_list.append(int(order_id))

        self.temp_label = []
        self.display_order_list()
        self.display_extra_order()

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind_exit = self.root.bind('<F3>', self.exit_window)

        customtkinter.CTkLabel(self.curr_frame, text="F5. Prev", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25) 
        self.bind_exit = self.root.bind('<F5>', self.prev_page)

        customtkinter.CTkLabel(self.curr_frame, text="F7. Next", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind_exit = self.root.bind('<F7>', self.next_page)
        
        raise_frame(self.curr_frame)

    def display_order_list(self):
        if(len(self.temp_label) > 0 ):
            for label in self.temp_label:
                label.destroy()
            self.temp_label = []
        min_i = self.i
        for i in range(min_i, len(self.order_list)):
            if(i == min_i+6):
                break
            order_id = self.order_list[i]
            id_text = "Order: " + str(order_id)
            id_extra_order =  "     \t" + "Order: " + str(order_id)
            order_label = customtkinter.CTkLabel(self.order_id_list_frame, text=id_text, font=("Roboto", 20))
            order_label.pack(side='top', anchor = 'w', pady=2, padx=10)
            self.temp_label.append(order_label)

    def display_extra_order(self):
        min_i = self.i + 6
        for i in range(min_i, len(self.order_list)):
            if(i == min_i+6):
                break
            x = i % 6

            label_text = self.temp_label[x]
            order_text = label_text.cget('text')
            next_order = "Order: " + str(self.order_list[i])
            o_text = order_text + "     \t" + next_order

            
            label_text.configure(text=o_text)

    def prev_page(self, event):
        self.i = self.i - 12
        if(self.i < 0):
            self.i = 0
        self.display_order_list()
        self.display_extra_order()

    def next_page(self, event):
        if(self.i + 12 < len(self.order_list)):
            self.i = self.i + 12
        self.display_order_list()
        self.display_extra_order()

        
    def exit_window(self, event):
        self.root.unbind('<F3>', self.bind_exit)
        self.curr_frame.destroy()
        self.gui_application.display_command_window()
        

def raise_frame(frame):
    frame.tkraise()
