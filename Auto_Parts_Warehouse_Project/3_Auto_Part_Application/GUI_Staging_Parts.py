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
    
    def __init__(self, gui_applicaiton, name, connection, engine, root, frame2):
        self.gui_application = gui_applicaiton
        self.name = name
        self.connection = connection
        self.engine = engine
        self.root = root
        self.curr_frame = frame2

    def update_view(self):
        query = "SELECT OL.PRODUCT_ID, COUNT(OL.UNITS), P.PRODUCT_NAME "\
        "FROM ORDER_LIST OL " \
        "JOIN PRODUCT P " \
        "   ON OL.PRODUCT_ID = P.PRODUCT_ID " \
        "WHERE OL.ZONE = '"+self.tote_zone+"' AND OL.PRODUCT_ID = "+self.product_id+" " \
        "GROUP BY OL.PRODUCT_ID, P.PRODUCT_NAME "

        update_list = pd.read_sql(query, self.engine)

        if(update_list.size == 0):
            check_tote_empty_query = "SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = '"+self.tote_zone+"'"
            tote_result = pd.read_sql(check_tote_empty_query, self.engine).iat[0,0]
            self.root.unbind('<F3>', self.bind_exit)
            self.root.unbind('<F5>', self.bind_qty)

            if(int(tote_result) == 0):
                self.load_staging_view()
            else:
                self.load_stage_product_view()
        else:
            quantity = update_list.iat[0,1]
            product_name = update_list.iat[0,2]
            self.product_info_show_quantity.configure(text = "QTY: " + str(quantity))
            self.quantity = quantity
            
            size = len(self.product_info_enter_stage.get())
            self.product_info_enter_stage.delete(0,size)
            
            size = len(self.product_info_enter_quantity.get())
            self.product_info_enter_quantity.delete(0,size)
            self.product_info_enter_quantity.insert(0, '1')
            self.product_info_enter_quantity.configure(state='disabled')
            self.bin_pick_part_name.configure(text = "Part Name: " + str(product_name))

            
    def stage_part(self, event):
        self.product_info_enter_quantity.configure(state='normal')
        quantity_scanned = self.product_info_enter_quantity.get()
        stage_scanned = self.product_info_enter_stage.get()

        # Query 6
        check_stage_query = "SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('STAGE', '" +stage_scanned+"') FROM DUAL"
        stage_result = pd.read_sql(check_stage_query, self.engine).iat[0,0]
        print(stage_result)

        if(stage_result != 0 and (int(quantity_scanned) <= int(self.quantity) and int(stage_result) == 1)):
                # Move parts to Stage Area
                # Employee ID = 1
                # Query 7
                query = "BEGIN PACKAGE_ORDER_LIST.MOVE_TOTE_TO_STAGE("+str(self.product_id)+", 1, "+str(quantity_scanned)+", 'PICK', " \
                        "'"+self.tote_zone+"' , 'STAGE' , '"+stage_scanned+"'); commit; END;"
                cursor = self.connection.cursor()
                result = cursor.execute(query)
                self.update_view()
        elif(stage_result == 0):
            self.root.bell()
            size = len(stage_scanned)
            self.product_info_enter_stage.delete(0,size)
        else:
            self.root.bell()
            size = len(quantity_scanned)
            self.product_info_enter_quantity.delete(0,size)
            self.product_info_enter_quantity.insert(0, '1')
        
    def load_product_info(self):
        self.curr_frame.destroy()
           
        product_info_frame = customtkinter.CTkFrame(master = self.root)
        product_info_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = product_info_frame

        self.product_info_label = customtkinter.CTkLabel(product_info_frame, text="Display Product Info", font=("Roboto", 40))
        self.product_info_label.pack(pady=12, padx=10)

        # Query 5
        query = "SELECT OL.PRODUCT_ID, COUNT(OL.UNITS), P.PRODUCT_NAME "\
                "FROM ORDER_LIST OL "\
                "JOIN PRODUCT P " \
                "   ON OL.PRODUCT_ID = P.PRODUCT_ID " \
                "WHERE OL.ZONE = '"+self.tote_zone+"' AND OL.PRODUCT_ID = "+self.product_id+" " \
                "GROUP BY OL.PRODUCT_ID, P.PRODUCT_NAME "

        query_result = pd.read_sql(query, self.engine)
        self.quantity = query_result.iat[0,1]
        product_name =  query_result.iat[0,2]
        
        display_tote = "Tote: " + self.tote_zone
        product_info_show_tote = customtkinter.CTkLabel(product_info_frame, text=display_tote, font=("Roboto", 20)).pack(pady=4, padx=10)

        display_info_frame = customtkinter.CTkFrame(product_info_frame)
        display_info_frame.pack(side='top', pady=10, padx=30)

        display_product = "Product: " + self.product_id
        self.product_info_show_product = customtkinter.CTkLabel(display_info_frame, text=display_product, font=("Roboto", 20))
        self.product_info_show_product.pack(side='left', anchor='w',pady=4, padx=10)

        display_quantity = "QTY: " + str(self.quantity)
        self.product_info_show_quantity = customtkinter.CTkLabel(display_info_frame, text=display_quantity, font=("Roboto", 20))
        self.product_info_show_quantity.pack(side='left', anchor='w',pady=4, padx=10)

        d_part_name = "Part Name: " + str(product_name)
        self.bin_pick_part_name = customtkinter.CTkLabel(product_info_frame, text=d_part_name, font=("Roboto", 20))
        self.bin_pick_part_name.pack(pady=2, padx=10)

        scan_frame = customtkinter.CTkFrame(product_info_frame)
        scan_frame.pack(side='top', anchor='w', pady=10, padx=10)

        product_info_scan_stage = customtkinter.CTkLabel(scan_frame, text="Scan Stage:", font=("Roboto", 20)).pack(side='left', anchor='w',pady=4, padx=10)  

        self.product_info_enter_stage = customtkinter.CTkEntry(scan_frame, width = 110, font=("Roboto", 16))
        self.product_info_enter_stage.pack(side='left', anchor='w',pady=2, padx=2)
        self.product_info_enter_stage.bind('<Return>', self.stage_part)
        self.product_info_enter_stage.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.product_info_enter_stage))
        self.product_info_enter_stage.focus_set()

        self.product_info_display_quantity = customtkinter.CTkLabel(scan_frame,text="QTY: ",font=("Roboto",20), width=60)
        self.product_info_display_quantity.pack(side='left', anchor='w', pady=2, padx=2)  

        validation = self.root.register(self.validate_entry)
        self.product_info_enter_quantity = customtkinter.CTkEntry(scan_frame, width = 55, font=("Roboto", 16), validate="key",validatecommand=(validation,"%P"))
        self.product_info_enter_quantity.insert(0, '1')
        self.product_info_enter_quantity.pack(side='left', anchor='w',pady=2, padx=2)
        self.product_info_enter_quantity.bind('<Return>', self.stage_part)
        self.product_info_enter_quantity.configure(state='disabled')
        
        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind_exit = self.root.bind('<F3>', self.exit_go_to_view)

        customtkinter.CTkLabel(self.curr_frame, text="F5. QTY", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25) 
        self.bind_qty = self.root.bind('<F5>', self.enable_qty_input)
        
        raise_frame(self.curr_frame)

    def exit_go_to_view(self, event):
        self.root.unbind('<F3>', self.bind_exit)
        self.root.unbind('<F5>', self.bind_qty)
        self.load_stage_product_view()   

    def enable_qty_input(self, event):
        state_condition = self.product_info_enter_quantity.cget("state")
        if(state_condition == 'disabled'):
            self.product_info_enter_quantity.configure(state='normal')
            self.product_info_enter_quantity.focus_set()
        elif(state_condition == 'normal'):
            num = self.product_info_enter_quantity.get()
            if(len(num) == 0):
                self.product_info_enter_quantity.insert(0, '1')
            self.product_info_enter_quantity.configure(state='disabled')
            self.product_info_enter_stage.focus_set()
        
    def check_product_scanned(self, event):
        self.product_id = self.stage_product_view_entry.get()

        # Query 3
        query_check_valid_product = "SELECT COUNT(*) FROM PRODUCT WHERE TO_CHAR(PRODUCT_ID) = '" + str(self.product_id) +"'"
        product_check = pd.read_sql(query_check_valid_product, self.engine).iat[0,0]
        if(product_check == 1):
            #Query 4
            query = "SELECT COUNT(UNITS) FROM ORDER_LIST WHERE ZONE = '"+self.tote_zone+"' AND PRODUCT_ID = "+self.product_id +" ORDER BY PRODUCT_ID"
            product_count = pd.read_sql(query, self.engine).iat[0,0]

            if(product_count > 0):
                self.load_product_info()
            else:
                size = len(self.product_id)
                self.stage_product_view_entry.delete(0,size)
                self.root.bell()             
        else:
            size = len(self.product_id)
            self.stage_product_view_entry.delete(0,size)
            self.root.bell()

    def load_stage_product_view(self):
        self.curr_frame.destroy()

        stage_product_view_frame = customtkinter.CTkFrame(master = self.root)
        stage_product_view_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = stage_product_view_frame

        stage_product_view_label = customtkinter.CTkLabel(stage_product_view_frame, text="Tote View", font=("Roboto", 40))
        stage_product_view_label.pack(pady=12, padx=10)

        self.stage_product_view_show_tote = customtkinter.CTkLabel(stage_product_view_frame, text="Tote: " + self.tote_zone, font=("Roboto", 20))
        self.stage_product_view_show_tote.pack(pady=5, padx=10)

        scan_product_frame = customtkinter.CTkFrame(stage_product_view_frame)
        scan_product_frame.pack(side='top', anchor = 'w', pady=10, padx=30)
        
        stage_product_view_label_2 = customtkinter.CTkLabel(scan_product_frame, text="Scan Product: ", font=("Roboto", 20))
        stage_product_view_label_2.pack(side='left', anchor='w', pady=5, padx=10)

        self.stage_product_view_entry = customtkinter.CTkEntry(scan_product_frame, font=("Roboto", 16))
        self.stage_product_view_entry.pack(side='left', anchor='w', pady=5, padx=10)
        self.stage_product_view_entry.bind('<Return>', self.check_product_scanned)
        self.stage_product_view_entry.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.stage_product_view_entry))
        self.stage_product_view_entry.focus_set()

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind_exit = self.root.bind('<F3>', self.exit_stage_product_view)

        raise_frame(self.curr_frame)

    def exit_stage_product_view(self, event):
        self.root.unbind('<F3>', self.bind_exit)
        self.load_staging_view()

    def check_tote_item_list(self, event):
        tote_zone = self.tote_name_entry.get()

        # Query 1
        check_tote_query = "SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('PICK', '" +tote_zone+"') FROM DUAL"
        tote_result = pd.read_sql(check_tote_query, self.engine).iat[0,0]
        self.tote_zone = tote_zone

        if(tote_result == 1):
            # Query 2
            check_tote_empty_query = "SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = '"+tote_zone+"'"
            tote_empty_result = pd.read_sql(check_tote_empty_query, self.engine).iat[0,0]

        if(tote_result == 1 and tote_empty_result > 0):
            # Continue rest of procedure here
            self.load_stage_product_view()
        else:
            self.tote_indicator.configure(text="Empty Or Incorrect Tote")
            size = len(tote_zone)
            self.tote_name_entry.delete(0,size)
            self.root.bell()
        

    def load_staging_view(self):
        self.curr_frame.destroy()

        staging_view_frame = customtkinter.CTkFrame(self.root)
        staging_view_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = staging_view_frame

        customtkinter.CTkLabel(staging_view_frame, text="Staging View", font=("Roboto", 40)).pack(side = 'top', pady=12, padx=10)

        scan_tote_frame = customtkinter.CTkFrame(staging_view_frame)
        scan_tote_frame.pack(side='top', anchor = 'w', pady=10, padx=30)

        scan_tote_label = customtkinter.CTkLabel(scan_tote_frame, text="Scan Tote: ", font=("Roboto", 20)).pack(side='left', anchor='w',pady=2, padx=10)

        self.tote_name_entry = customtkinter.CTkEntry(scan_tote_frame, font=("Roboto", 16), width = 200)
        self.tote_name_entry.pack(side ='left', anchor='w', pady=2, padx=2)
        self.tote_name_entry.bind('<Return>', self.check_tote_item_list)
        self.tote_name_entry.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.tote_name_entry))
        self.tote_name_entry.focus_set()

        self.tote_indicator = customtkinter.CTkLabel(staging_view_frame, text="", font=("Roboto", 20))
        self.tote_indicator.pack(side = 'top', pady=10, padx=10)

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='bottom', anchor = 'w', pady=10, padx=25)
        self.bind = self.root.bind('<F3>', self.exit_window)
        
        raise_frame(self.curr_frame)

    def exit_window(self, event):
        self.root.unbind('<F3>', self.bind)
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
