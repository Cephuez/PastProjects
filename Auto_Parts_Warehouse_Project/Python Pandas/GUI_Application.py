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
        self.root = tkinter.Tk()
        #self.name = name
        #self.root = tkinter.Tk()
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.root = customtkinter.CTk()
        self.root.geometry("500x450")

        #self.root = customtkinter.CTk()
        #self.root.geometry("500x450")

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
        input_num = self.f2_command_entry.get()
        #print("Entry: " + input_num)
        size = len(input_num)
        self.f2_command_entry.delete(0,size)
        if(input_num == '1'):
            Picking_Window = Picking_Parts_Window("Name", self.connection, self.engine, self.root, self.command_list_frame)
            Picking_Window.load_picking_view(None)
            #self.load_picking_view(None)
        elif(input_num == '2'):
            Staging_Window = Staging_Parts_Window("Name", self.connection, self.engine, self.root, self.command_list_frame)
            Staging_Window.load_staging_view(None)
            #self.load_staging_view(None)
        elif(input_num == '3'):
            Gather_Window = Gather_Parts_Window("Name", self.connection, self.engine, self.root, self.command_list_frame)
            Gather_Window.load_gather_parts_view(None)

    def display_command_window(self):
        self.log_in_frame.pack_forget()
        
        self.command_list_frame = customtkinter.CTkFrame(self.root)
        self.command_list_frame.pack(pady=20, padx=10, fill="y", expand=True)
        self.frame_list.append(self.command_list_frame)
        self.f_i = self.f_i + 1

        self.f2_label_1 = customtkinter.CTkLabel(self.command_list_frame , text="Command List", font=("Roboto", 40))
        self.f2_label_1.pack(side='top', pady=10, padx = 1)

        self.command_input_frame = customtkinter.CTkFrame(self.command_list_frame)
        self.command_input_frame.pack(side='top', anchor = 'w', pady=10, padx=25)

        self.f2_command_entry = customtkinter.CTkEntry(self.command_input_frame, width = 30, font=("Roboto", 20))
        self.f2_command_entry.pack(side='left', anchor = 'w', pady=1, padx=1)
        self.f2_command_entry.bind('<Return>', self.check_input)

        customtkinter.CTkLabel(self.command_input_frame, text="- Command", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=10)

        customtkinter.CTkLabel(self.command_list_frame, text="1. Start Picking", font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30)

        customtkinter.CTkLabel(self.command_list_frame, text="2. Stage Items", font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30)

        customtkinter.CTkLabel(master=self.command_list_frame, text="3. Gather Order Parts", font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30)

        self.short_cut_frame = customtkinter.CTkFrame(master = self.command_list_frame)
        self.short_cut_frame.pack(side='bottom', pady=20, padx=20)

        customtkinter.CTkLabel(master=self.short_cut_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=30)

        self.bin = self.root.bind('<F3>', self.exit_window)
        raise_frame(self.command_list_frame)     

    def exit_window(self, event):
        self.root.unbind('<F3>', self.bin)
        self.frame_list[self.f_i].destroy()
        self.beginning_screen()
        self.connection.close()
        
    def beginning_screen(self):
        #self.display_command_window()

        command = ""

        self.frame_list = []
        self.f_i = 0;
        
        self.log_in_frame = customtkinter.CTkFrame(self.root)
        self.log_in_frame.pack(pady=1, padx=1, fill="both", expand=True)
        self.frame_list.append(self.log_in_frame)

        self.log_in_label = customtkinter.CTkLabel(master=self.log_in_frame, text="Login  System", font=("Roboto", 24))
        self.log_in_label.pack(pady=12, padx=10)

        self.username_entry = customtkinter.CTkEntry(master=self.log_in_frame, placeholder_text="Username")
        self.username_entry.pack(pady=12, padx=10)

        self.password_entry = customtkinter.CTkEntry(master=self.log_in_frame, placeholder_text="Password")
        self.password_entry.pack(pady=12, padx=10)

        self.f1_button = customtkinter.CTkButton(master=self.log_in_frame, text="Login", command = self.login)
        self.f1_button.pack(pady=12, padx=10)       

        raise_frame(self.log_in_frame)
        
        self.root.mainloop()

def raise_frame(frame):
    
    frame.tkraise()
