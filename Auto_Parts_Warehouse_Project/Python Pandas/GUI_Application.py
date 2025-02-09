import oracledb
import pandas as pd
import customtkinter
import tkinter
from sqlalchemy import create_engine
from GUI_Picking_Parts import Picking_Parts_Window

class gui_application:
    engine = ""
    cs = ""
    connection = ""
    name = ""
    root = ""
    label = ""
    #entry1 = ""


    def __init__(self, name):
        self.name = name
        self.root = tkinter.Tk()
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.root = customtkinter.CTk()
        self.root.geometry("500x450")

    def print(self):
        print("GUI Application Started")

    def log_in(self):
        #self.user_name = input("User Name: ")
        #self.password = input("Password: ")
        user_name = "Project"
        password = "password123"
        cs = "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1522)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = orclpdb)))"
        self.connection = oracledb.connect( user=user_name, password= password, dsn= cs)
        self.engine = create_engine('oracle+oracledb://', creator=lambda: self.connection)

    def login(self):
        #user_name = self.f1_entry1.get()
        #password = self.f1_entry2.get()
        #print("Username: " + user_name)
        #print("Password: " + password)

        self.display_command_window()

        '''
        try:
            cs = "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1522)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = orclpdb)))"
            self.connection = oracledb.connect( user=user_name, password= password, dsn= cs)
            self.engine = create_engine('oracle+oracledb://', creator=lambda: self.connection)
            print("Connected")
            self.display_command_window()
            
        except:
            print("Log in incorrect")
        '''
        #print("Username: "+ entry1.get())
        #print("Password: "+ entry2.get())
        #print("Test")

    def stage_part(self, event):
        print("Check Part")
        # Run and check if the input part is correct
        # If it's correct, then move the part to the staging area
            # Then run load_stage_product_view
            # Go back to product_view because maybe not all parts could fit in stage shelf
        
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

        self.product_info_display_product = customtkinter.CTkLabel(master=self.product_info_frame, text="Scan Product", font=("Roboto", 20))
        self.product_info_display_product.pack(pady=4, padx=10)  

        self.product_info_enter_product = customtkinter.CTkEntry(master=self.product_info_frame)
        self.product_info_enter_product.pack(pady=4, padx=10)
        self.product_info_enter_product.bind('<Return>', self.stage_part)

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
        
    

    ## From here, you will launch seperate classes to handle each window
    def check_input(self, event):
        input_num = self.f2_entry1.get()
        #print("Entry: " + input_num)
        size = len(input_num)
        self.f2_entry1.delete(0,size)
        if(input_num == '1'):
            Picking_Window = Picking_Parts_Window("Name", self.connection, self.engine, self.root, self.frame2)
            Picking_Window.load_picking_view(None)
            #self.load_picking_view(None)
        elif(input_num == '2'):
            self.load_staging_view(None)
            
    def display_command_window(self):
        #print("1. Start Picking")
        #print("2. Stage Items")
        #print("3. Gather Order Parts")
        #print("4. Move Parts")
        #print("5. Process Receiving Items")
        #print("6. Process Order")
        #print("7. Look Product's Location")
        #print("0. Exit Program")
        self.frame1.destroy()
        self.frame2 = customtkinter.CTkFrame(master = self.root)
        self.frame2.pack(pady=20, padx=10, fill="y", expand=True)

        self.f2_label_1 = customtkinter.CTkLabel(master=self.frame2, text="Command List", font=("Roboto", 34))
        self.f2_label_1.pack(pady=30, padx=10)

        self.f2_entry1 = customtkinter.CTkEntry(master=self.frame2)
        self.f2_entry1.pack(pady=12, padx=10)
        self.f2_entry1.bind('<Return>', self.check_input)

        self.f2_label_2 = customtkinter.CTkLabel(master=self.frame2, text="1. Start Picking", font=("Roboto", 20), justify="left")
        self.f2_label_2.pack(pady=1, padx=10)

        self.f2_label_3 = customtkinter.CTkLabel(master=self.frame2, text="2. Stage Items", font=("Roboto", 20))
        self.f2_label_3.pack(pady=1, padx=10)

        self.f2_label_4 = customtkinter.CTkLabel(master=self.frame2, text="3. Gather Order Parts", font=("Roboto", 20))
        self.f2_label_4.pack(pady=1, padx=10)

        self.f2_label_5 = customtkinter.CTkLabel(master=self.frame2, text="4. Move Parts", font=("Roboto", 20))
        self.f2_label_5.pack(pady=1, padx=10)

        self.f2_label_6 = customtkinter.CTkLabel(master=self.frame2, text="5. Process Receiving Items", font=("Roboto", 20))
        self.f2_label_6.pack(pady=1, padx=10)

        self.f2_label_7 = customtkinter.CTkLabel(master=self.frame2, text="6. Process Order", font=("Roboto", 20))
        self.f2_label_7.pack(pady=1, padx=10)

        self.f2_label_8 = customtkinter.CTkLabel(master=self.frame2, text="7. Search Product's Location", font=("Roboto", 20))
        self.f2_label_8.pack(pady=1, padx=1)

        self.f2_label_9 = customtkinter.CTkLabel(master=self.frame2, text="8. Log Out", font=("Roboto", 20))
        self.f2_label_9.pack(pady=1, padx=1)
        
        
        raise_frame(self.frame2)
        
    def beginning_screen(self):
        command = ""
        self.frame1 = customtkinter.CTkFrame(master = self.root)
        self.frame1.pack(pady=20, padx=60, fill="both", expand=True)

        self.f1_label = customtkinter.CTkLabel(master=self.frame1, text="Login  System", font=("Roboto", 24))
        self.f1_label.pack(pady=12, padx=10)

        self.f1_entry1 = customtkinter.CTkEntry(master=self.frame1, placeholder_text="Username")
        self.f1_entry1.pack(pady=12, padx=10)

        self.f1_entry2 = customtkinter.CTkEntry(master=self.frame1, placeholder_text="Password")
        self.f1_entry2.pack(pady=12, padx=10)

        self.f1_button = customtkinter.CTkButton(master=self.frame1, text="Login", command = self.login)
        self.f1_button.pack(pady=12, padx=10)

        #checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
        #checkbox.pack(pady=12, padx=10)

        raise_frame(self.frame1)
        self.root.mainloop()

def raise_frame(frame):
    frame.tkraise()
