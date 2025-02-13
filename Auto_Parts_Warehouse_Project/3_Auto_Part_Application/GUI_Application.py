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
        self.root.geometry("400x450")

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
        self.display_command_window()
        self.log_in_frame.pack_forget()
        
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
    def display_command_window(self):
        self.command_list_frame = customtkinter.CTkFrame(self.root)
        self.command_list_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame_list.append(self.command_list_frame)
        self.f_i = self.f_i + 1

        self.f2_label_1 = customtkinter.CTkLabel(self.command_list_frame , text="Command List", font=("Roboto", 40))
        self.f2_label_1.pack(side='top', pady=20, padx = 20)

        customtkinter.CTkLabel(self.command_list_frame, text="1. Start Picking", font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30)

        customtkinter.CTkLabel(self.command_list_frame, text="2. Stage Items", font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30)

        customtkinter.CTkLabel(self.command_list_frame, text="3. Gather Order Parts", font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30)

        #short_cut_frame = customtkinter.CTkFrame(self.command_list_frame)\
        #short_cut_frame = customtkinter.CTkFrame(self.command_list_frame)
        #short_cut_frame.pack(side='bottom', pady=20, padx=20)

        customtkinter.CTkLabel(self.command_list_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='bottom', anchor = 'w', pady=10, padx=25)
        #tkinter.Label(short_cut_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'w')
        
        self.input_1 = self.root.bind('1', self.start_picking_window)
        self.input_2 = self.root.bind('2', self.start_staging_window)
        self.input_3 = self.root.bind('3', self.start_gather_window)

        self.bin = self.root.bind('<F3>', self.exit_window)
        raise_frame(self.command_list_frame)

    def start_picking_window(self, event):
        self.root.unbind('<F3>', self.bin)
        self.root.unbind('1', self.input_1)
        self.root.unbind('2', self.input_2)
        self.root.unbind('3', self.input_3)
        Picking_Window = Picking_Parts_Window(self, "Name", self.connection, self.engine, self.root, self.command_list_frame)
        Picking_Window.load_picking_view()

    def start_staging_window(self, event):
        self.root.unbind('<F3>', self.bin)
        self.root.unbind('1', self.input_1)
        self.root.unbind('2', self.input_2)
        self.root.unbind('3', self.input_3)
        Staging_Window = Staging_Parts_Window(self, "Name", self.connection, self.engine, self.root, self.command_list_frame)
        Staging_Window.load_staging_view()

    def start_gather_window(self, event):
        self.root.unbind('<F3>', self.bin)
        self.root.unbind('1', self.input_1)
        self.root.unbind('2', self.input_2)
        self.root.unbind('3', self.input_3)
        Gather_Window = Gather_Parts_Window(self, "Name", self.connection, self.engine, self.root, self.command_list_frame)
        Gather_Window.load_gather_parts_view()
        
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
        self.log_in_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame_list.append(self.log_in_frame)

        self.log_in_label = customtkinter.CTkLabel(master=self.log_in_frame, text="Login  System", font=("Roboto", 40))
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
