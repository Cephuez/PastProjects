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
        
        tote_text = "Tote: " + self.box_tote
        customtkinter.CTkLabel(shelf_view_frame, text=tote_text, font=("Roboto", 20)).pack(pady=10, padx=10)

        display_info_frame = customtkinter.CTkFrame(shelf_view_frame)
        display_info_frame.pack(side='top', pady=10, padx=30)

        display_product = "Product: " + str(self.product_id)
        self.product_info_show_product = customtkinter.CTkLabel(display_info_frame, text=display_product, font=("Roboto", 20))
        self.product_info_show_product.pack(side='left', anchor='w',pady=4, padx=10)

        display_quantity = "QTY: " + str(self.quantity)
        self.product_info_show_quantity = customtkinter.CTkLabel(display_info_frame, text=display_quantity, font=("Roboto", 20))
        self.product_info_show_quantity.pack(side='left', anchor='w',pady=4, padx=10)

        scan_frame = customtkinter.CTkFrame(shelf_view_frame)
        scan_frame.pack(side='top', anchor='w', pady=10, padx=10)
        
        customtkinter.CTkLabel(scan_frame, text="Scan Product:", font=("Roboto", 20)).pack(side='left', anchor='w',pady=4, padx=10)  

        self.shelf_view_product_entry = customtkinter.CTkEntry(scan_frame, width = 110, font=("Roboto", 16))
        self.shelf_view_product_entry.pack(side='left', anchor='w',pady=2, padx=2)
        self.shelf_view_product_entry.bind('<Return>', self.check_product)
        self.shelf_view_product_entry.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.shelf_view_product_entry))
        self.shelf_view_product_entry.focus_set()

        self.quantity_frame = customtkinter.CTkLabel(scan_frame,text="QTY: ",font=("Roboto",20), width=60)
        self.quantity_frame.pack(side='left', anchor='w', pady=2, padx=2)  

        validation = self.root.register(self.validate_entry)
        self.shelf_view_quantity_entry = customtkinter.CTkEntry(scan_frame, width = 55, font=("Roboto", 16), validate="key",validatecommand=(validation,"%P"))
        self.shelf_view_quantity_entry.insert(0, '1')
        self.shelf_view_quantity_entry.pack(side='left', anchor='w',pady=2, padx=2)
        self.shelf_view_quantity_entry.bind('<Return>', self.check_product)
        self.shelf_view_quantity_entry.configure(state='disabled')

        #d_part_name = "Part Name: " + str(product_name)
        d_part_name = "Part Name: "
        self.bin_pick_part_name = customtkinter.CTkLabel(shelf_view_frame, text=d_part_name, font=("Roboto", 20))
        self.bin_pick_part_name.pack(pady=2, padx=10)

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
            
            stage_display = "Scan Stage: " + self.curr_stage
            customtkinter.CTkLabel(staging_view_frame, text=stage_display, font=("Roboto", 20)).pack(side='top', pady=10, padx=2)

            self.staging_view_entry = customtkinter.CTkEntry(staging_view_frame, font=("Roboto", 16))
            self.staging_view_entry.pack(side='top', pady=12, padx=10)
            self.staging_view_entry.bind('<Return>', self.check_stage_input)
            self.staging_view_entry.focus_set()

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
        else:
            self.root.bell()
            self.tote_indicator.configure(text="Empty Or Incorrect Tote")
            size = len(tote_zone)
            self.tote_name_entry.delete(0,size)
        
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

        self.tote_indicator = customtkinter.CTkLabel(box_display_frame, text="", font=("Roboto", 20))
        self.tote_indicator.pack(side = 'top', pady=10, padx=10)

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
            
        else:
            self.root.bell()
            size = len(self.order_id)
            self.gather_parts_enter_product.delete(0,size)

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

        validation = self.root.register(self.validate_entry)
        self.gather_parts_enter_product = customtkinter.CTkEntry(enter_order_id_frame, font=("Roboto", 16), width = 80, validate="key", validatecommand=(validation, "%P"))
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
        
    def to_uppercase(self, frame):
        input_text = frame.get()
        length = len(input_text)
        frame.delete(0,length)
        frame.insert(0,input_text.upper())

    def validate_entry(self, new_text):
        if not new_text:
            return True
        try:
            int(new_text)
            return True
        except ValueError:
            return False

def raise_frame(frame):
    frame.tkraise()
