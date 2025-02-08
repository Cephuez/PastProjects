import oracledb
import pandas as pd
import customtkinter
import tkinter
from sqlalchemy import create_engine

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

    def check_input():
        print("as")

    def load_bin_pick_view(self, bin_picked):
        self.pick_frame.destroy()
        self.zone_list_i = 0
        
        self.bin_pick_frame = customtkinter.CTkFrame(master = self.root)
        self.bin_pick_frame.pack(pady=30, padx=10)

        self.bin_pick_frame_label_1 = customtkinter.CTkLabel(master=self.bin_pick_frame, text="Picking List", font=("Roboto", 34)).pack(pady=30, padx=10)

        query = "SELECT DISTINCT ZONE_lOCATION FROM PICKS WHERE BIN_LOCATION = '"+bin_picked+"' AND PICK_STATUS = 'N' ORDER BY ZONE_LOCATION"
        self.zone_location_list = pd.read_sql(query, self.engine)

        zone_loc = self.zone_location_list.iat[self.zone_list_i,0]
        bin_loc = bin_picked
        
        query = "SELECT ORDER_ID, PRODUCT_ID, QUANTITY, ZONE_LOCATION FROM PICKS " \
                "WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' ORDER BY ZONE_LOCATION, ORDER_ID"
        self.product_zone_list = pd.read_sql(query, self.engine)
        
        order_id = self.product_zone_list.iat[self.zone_list_i,0]
        product_id = self.product_zone_list.iat[self.zone_list_i,1]
        quantity = self.product_zone_list.iat[self.zone_list_i,2]
        

        display_order_id = "Order ID: " + str(order_id)
        self.bin_pick_frame_label_2 = customtkinter.CTkLabel(master=self.bin_pick_frame, text=display_order_id, font=("Roboto", 20)).pack(pady=2, padx=10)

        display_product = "Product: " + str(product_id)
        self.bin_pick_frame_label_3 = customtkinter.CTkLabel(master=self.bin_pick_frame, text=display_product, font=("Roboto", 20)).pack(pady=2, padx=10)

        display_quantity = "QTY: " + str(quantity)
        self.bin_pick_frame_label_4 = customtkinter.CTkLabel(master=self.bin_pick_frame, text=display_quantity, font=("Roboto", 20)).pack(pady=2, padx=10)

        display_location = bin_loc + " " +zone_loc
        self.bin_pick_frame_label_5 = customtkinter.CTkLabel(master=self.bin_pick_frame, text=display_location, font=("Roboto", 20)).pack(pady=2, padx=10)

        self.bin_pick_frame_entry1 = customtkinter.CTkEntry(master=self.frame2)
        self.bin_pick_frame_entry1.pack(pady=12, padx=10)
        self.bin_pick_frame_entry1.bind('<Return>', self.check_input)
        
        raise_frame(self.bin_pick_frame)


    def input_pick_tote(self):
        self.pick_frame.destroy()

        self.tote_pick_frame = customtkinter.CTkFrame(master = self.root)
        self.tote_pick_frame.pack(pady=30, padx=10)

        self.tote_pick_frame_label_1 = customtkinter.CTkLabel(master=self.tote_pick_frame, text="Scan Tote", font=("Roboto", 34)).pack(pady=30, padx=10)

        self.tote_pick_entry_1 = customtkinter.CTkEntry(master=self.tote_pick_frame).pack(pady=12, padx=10)
        
        raise_frame(self.tote_pick_frame)
        

        
    def check_picking_view(self, event):
        bin_picked = self.pick_frame_entry_1.get().upper()
        #print("Entry: " + bin_picked)
        #print(self.pick_list)
        size = len(bin_picked)
        self.pick_frame_entry_1.delete(0,size)

        for i in range(0,int(self.pick_list.size/2)):
            if(str(self.pick_list.iat[i,0]) == bin_picked):
                #print("Correct Input")
                self.input_pick_tote()
                #self.load_bin_pick_view(bin_picked)

        
    def load_picking_view(self):
        self.frame2.destroy()

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
        
    def check_input(self, event):
        input_num = self.f2_entry1.get()
        print("Entry: " + input_num)
        size = len(input_num)
        self.f2_entry1.delete(0,size)
        if(input_num == '1'):
            self.load_picking_view()
        

            
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
