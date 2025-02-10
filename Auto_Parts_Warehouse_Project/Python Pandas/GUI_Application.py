import oracledb
import pandas as pd
import customtkinter
import tkinter
from sqlalchemy import create_engine
from GUI_Picking_Parts import Picking_Parts_Window
from GUI_Staging_Parts import Staging_Parts_Window

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

    def load_staging_view(self, other_frame):
        if(other_frame is None):
            self.scan_box_frame.destroy()
        else:
            self.other_frame.destroy()

        self.staging_view_frame = customtkinter.CTkFrame(master = self.root)
        self.staging_view_frame.pack(pady=30, padx=10)

        stage_display = "Scan Stage: "
        self.staging_view_display_stage = customtkinter.CTkLabel(master=self.staging_view_frame, text=stage_display, font=("Roboto", 34))
        self.staging_view_display_stage.pack(pady=30, padx=10)

        raise_frame(self.staging_view_frame)
        

    def check_input_box(self, event):
        self.box_tote = self.scan_box_entry.get()

        print(self.box_tote)
        query = "SELECT COUNT(*) FROM APPROVED_ZONE WHERE ZONE = '"+self.box_tote+"'"
        tote_exists = pd.read_sql(query, self.engine).iat[0,0]

        query = "SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = '"+self.box_tote+"'"
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
        
        #SELECT COUNT(*) FROM APPROVED_ZONE WHERE ZONE = 'ORDER_TOTE_00001'; -- If 1, then approved box
        #SELECT COUNT(*) FROM ORDER_LIST WHERE ZONE = 'ORDER_TOTE_00001' -- If 0, then box can be used

        raise_frame(self.scan_box_frame)

    def check_order_id(self, event):
        self.order_id = self.gather_parts_enter_product.get()

        if(int(self.order_id) in self.order_list):
            self.load_input_box_view(None)
            print("Correct Order ID")
        else:
            print("Wrong Order ID")

    def load_gather_parts_view(self, other_frame):
        print("XD")
        if(other_frame is None):
            self.frame2.destroy()
        else:
            other_frame.destory()

        self.order_list = []
        self.gather_parts_frame = customtkinter.CTkFrame(master = self.root)
        self.gather_parts_frame.pack(pady=30, padx=10)

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

    '''
        This will display the views by calling separate classes
    
    '''    

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
            Staging_Window = Staging_Parts_Window("Name", self.connection, self.engine, self.root, self.frame2)
            Staging_Window.load_staging_view(None)
            #self.load_staging_view(None)
        elif(input_num == '3'):
            self.load_gather_parts_view(None)

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
