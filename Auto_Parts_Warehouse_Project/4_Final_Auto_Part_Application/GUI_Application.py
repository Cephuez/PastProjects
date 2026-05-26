import customtkinter
import tkinter
import requests

from GUI_Picking_Parts import Picking_Parts_Window
from GUI_Staging_Parts import Staging_Parts_Window
from GUI_Gather_Parts import Gather_Parts_Window

'''
    It sets up the GUI which will allow the user to interact with the application
    and eventually make API calls
'''
class gui_application:
    engine = ""
    cs = ""
    connection = ""
    name = ""
    root = ""
    label = ""
    #entry1 = ""

    # Set up canvas
    def __init__(self, name):
        self.root = tkinter.Tk()
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("dark-blue")

        self.root = customtkinter.CTk()
        self.root.geometry("425x450")

    def print(self):
        print("GUI Application Started")

    # Set up display        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.error_label.configure(text="Connecting to server...")
        self.root.update()

        try:
            # Get token if the user logs in correctly. Allows them access to the API
            auth = requests.get(
                'https://warehouse-api-wnnm.onrender.com/check-login',
                params={'user_name': username, 'password': password},
                timeout=5
            ).json()
            print(auth)
            if auth is None:
                self.root.bell()
                self.password_entry.delete(0, "end")
                self.error_label.configure(text="Wrong Username or Password")
                return
            
            self.dev_token = auth["token"]
            self.display_command_window()
            self.log_in_frame.pack_forget()
            
        except requests.exceptions.ConnectionError:
            self.error_label_configure(text="Server waking up. Please wait...")
        except requests.exceptions.ConnectionError:
            self.error_label.configure(text="Unable to connect to server")
        self.root.update()

    '''
        This will display the views by calling separate classes
    
    '''    
    def display_command_window(self):
        self.command_list_frame = customtkinter.CTkFrame(self.root)
        self.command_list_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.frame_list.append(self.command_list_frame)
        self.f_i += 1

        self.f2_label_1 = customtkinter.CTkLabel(self.command_list_frame , text="Command List", font=("Roboto", 40))
        self.f2_label_1.pack(side='top', pady=12, padx=10)

        customtkinter.CTkLabel(self.command_list_frame, text="1. Start Picking", font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30)

        customtkinter.CTkLabel(self.command_list_frame, text="2. Stage Items", font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30)

        customtkinter.CTkLabel(self.command_list_frame, text="3. Gather Order Parts", font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30)

        customtkinter.CTkLabel(self.command_list_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='bottom', anchor = 'w', pady=10, padx=25)
        
        self.input_1 = self.root.bind('1', self.start_picking_window)
        self.input_2 = self.root.bind('2', self.start_staging_window)
        self.input_3 = self.root.bind('3', self.start_gather_window)

        self.bin = self.root.bind('<F3>', self.exit_window)
        raise_frame(self.command_list_frame)

    def start_picking_window(self, event):
        self.unbind_commands()
        Picking_Window = Picking_Parts_Window(self, "Name", self.connection, self.engine, self.root, self.command_list_frame, self.dev_token)
        Picking_Window.load_picking_view()

    def start_staging_window(self, event):
        self.unbind_commands()
        Staging_Window = Staging_Parts_Window(self, "Name", self.connection, self.engine, self.root, self.command_list_frame, self.dev_token)
        Staging_Window.load_staging_view()

    def start_gather_window(self, event):
        self.unbind_commands()
        Gather_Window = Gather_Parts_Window(self, "Name", self.connection, self.engine, self.root, self.command_list_frame, self.dev_token)
        Gather_Window.load_gather_parts_view()        

    def unbind_commands(self):
        self.root.unbind('<F3>', self.bin)
        self.root.unbind('1', self.input_1)
        self.root.unbind('2', self.input_2)
        self.root.unbind('3', self.input_3)
        
    def exit_window(self, event):
        self.root.unbind('<F3>', self.bin)
        self.frame_list[self.f_i].destroy()
        self.beginning_screen()
        self.connection.close()
        
    def beginning_screen(self):
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

        self.password_entry = customtkinter.CTkEntry(master=self.log_in_frame,placeholder_text="Password",show="•")
        self.password_entry.pack(pady=12, padx=10)

        self.f1_button = customtkinter.CTkButton(master=self.log_in_frame, text="Login", command = self.login)
        self.f1_button.pack(pady=12, padx=10)       

        self.error_label = customtkinter.CTkLabel(master=self.log_in_frame,text="",font=("Roboto", 14),text_color="red")
        self.error_label.pack(pady=(5, 10))
        
        raise_frame(self.log_in_frame)
        
        self.root.mainloop()

def raise_frame(frame):
    frame.tkraise()
