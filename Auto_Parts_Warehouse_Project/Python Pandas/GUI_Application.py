import oracledb
import pandas as pd
import customtkinter
import tkinter
from sqlalchemy import create_engine
from GUI_Picking_Parts import Picking_Parts_Window
from GUI_Staging_Parts import Staging_Parts_Window
from GUI_Gather_Parts import Gather_Parts_Window

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
            Gather_Window = Gather_Parts_Window("Name", self.connection, self.engine, self.root, self.frame2)
            Gather_Window.load_gather_parts_view(None)

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

        '''
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
        '''
        
        
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
