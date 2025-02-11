import oracledb
import pandas as pd
import customtkinter
import tkinter
#from GUI_Application import gui_application
from sqlalchemy import create_engine


'''
    TODO:
    1. Make sure you can return back to the previous class. You will need to return the current frame when exiting windows
    2. Allow the user to change totes. There's a chance it can be filled all the way to the top
    3. Add the shortcuts onto the screen. 'F5' to allow quantity. 'F3' to exit from the window, etc
    4. Check for 'self.root.bind('<F5>', self.enable_qty_input)'. There's a chance this will carry over for other windows
'''

class Picking_Parts_Window:
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
        self.tote_zone = ""


    def update_product_view(self):
        zone_loc = self.zone_loc

        query = "SELECT PRODUCT_ID, SUM(QUANTITY), ZONE_LOCATION FROM PICKS " \
        "WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' GROUP BY PRODUCT_ID, ZONE_LOCATION ORDER BY ZONE_LOCATION"
        self.product_zone_list = pd.read_sql(query, self.engine)

        if(self.product_zone_list.size == 0):
            #self.go_to_zone_location(self.bin_pick_frame)
            self.tote_zone = ""
            self.root.unbind('<F3>', self.bind)
            self.go_to_zone_location()
            print("Go back")
        else:
            product_id = self.product_zone_list.iat[0,0]
            qty = self.product_zone_list.iat[0,1]
            zone_loc = self.product_zone_list.iat[0,2]
            bin_loc = self.bin_picked
            self.loc = zone_loc

            self.bin_pick_frame_product.configure(text = "Product: " + str(product_id))
            self.bin_pick_frame_quantity.configure(text = "QTY: " + str(qty))
            self.bin_pick_frame_zone.configure(text = "Zone: " + bin_loc + " " + zone_loc)
        
        
    def check_product(self,event):
        if(self.tote_zone != ""):
            input_product_id = self.bin_pick_frame_entry1.get()
            input_qty = self.bin_pick_frame_qty_entry.get()

            product_id = self.product_zone_list.iat[0,0]
            zone_loc = self.zone_loc
            bin_loc = self.bin_picked
            tote_zone = self.tote_zone
            if(str(input_product_id) == str(product_id)):
                query = "SELECT PACKAGE_PICKS.CHECK_QUANTITY_INPUT("+str(product_id)+", "+str(input_qty)+", '"+bin_loc+"', '"+zone_loc+"') FROM DUAL"
                qty_result = pd.read_sql(query, self.engine).iat[0,0]
                if(qty_result == 1):
                    size = len(input_product_id)
                    self.bin_pick_frame_entry1.delete(0,size)
                    size = len(input_qty)
                    self.bin_pick_frame_qty_entry.delete(0,size)
                    self.bin_pick_frame_qty_entry.insert(0, '1')
                    cursor = self.connection.cursor()
                    query = "BEGIN PACKAGE_PICKS.PROCESS_PICKS(" + str(product_id) + ", 1, "+str(input_qty)+", '" + bin_loc + "', '" + zone_loc + \
                        "', 'PICK', '" + tote_zone +"'); commit; END;"
                    result = cursor.execute(query)
                    self.update_product_view()
            else:
                size = len(input_product_id)
                self.bin_pick_frame_entry1.delete(0,size)
                size = len(input_qty)
                self.bin_pick_frame_qty_entry.delete(0,size)
                self.bin_pick_frame_qty_entry.insert(0, '1')
    
    def load_bin_pick_view(self):
        zone_loc = self.input_zone
        self.curr_frame.destroy()
        
        bin_loc = self.bin_picked
        
        bin_pick_frame = customtkinter.CTkFrame(master = self.root)
        bin_pick_frame.pack(pady=30, padx=10, side='top')

        self.curr_frame = bin_pick_frame

        customtkinter.CTkLabel(bin_pick_frame, text="Picking List", font=("Roboto", 34)).pack(pady=30, padx=10)
        
        query = "SELECT PRODUCT_ID, SUM(QUANTITY), ZONE_LOCATION FROM PICKS " \
                "WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' GROUP BY PRODUCT_ID, ZONE_LOCATION ORDER BY ZONE_LOCATION"
        self.product_zone_list = pd.read_sql(query, self.engine)

        product_id = self.product_zone_list.iat[0,0]
        quantity = self.product_zone_list.iat[0,1]        

        pd_frame = customtkinter.CTkFrame(bin_pick_frame)
        pd_frame.pack(side='top', pady=10, padx=10)

        d_product = "Product: " + str(product_id)
        self.bin_pick_frame_product = customtkinter.CTkLabel(pd_frame, text=d_product, font=("Roboto", 20))
        self.bin_pick_frame_product.pack(side='left', anchor='w', pady=2, padx=10)

        d_quantity = "QTY: " + str(quantity)
        self.bin_pick_frame_quantity = customtkinter.CTkLabel(pd_frame, text=d_quantity, font=("Roboto", 20))
        self.bin_pick_frame_quantity.pack(side='left', anchor='w',pady=2, padx=10)

        d_location = "Zone: " + bin_loc + " " +zone_loc
        self.bin_pick_frame_zone = customtkinter.CTkLabel(pd_frame, text=d_location, font=("Roboto", 20))
        self.bin_pick_frame_zone.pack(side='left', anchor='w',pady=2, padx=10)

        s_frame = customtkinter.CTkFrame(bin_pick_frame)
        s_frame.pack(side='top', pady=10, padx=10)

        customtkinter.CTkLabel(s_frame, text="Scan: ", font=("Roboto", 20)).pack(side='left', anchor='w', pady=4, padx=5)
        self.bin_pick_frame_entry1 = customtkinter.CTkEntry(s_frame, justify='center')
        self.bin_pick_frame_entry1.pack(side='left', anchor='w', pady=4, padx=5)
        self.bin_pick_frame_entry1.bind('<Return>', self.check_product)

        self.bin_pick_frame_qty_input = customtkinter.CTkLabel(s_frame, text="QTY: ", font=("Roboto", 20))
        self.bin_pick_frame_qty_input.pack(side='left', anchor='w', pady=4, padx=5)

        self.bin_pick_frame_qty_entry = customtkinter.CTkEntry(s_frame, justify='center', width = 50, font=("Roboto", 20))
        self.bin_pick_frame_qty_entry.insert(0, '1')
        self.bin_pick_frame_qty_entry.pack(side='left', anchor='w', pady=4, padx=5)
        self.bin_pick_frame_qty_entry.bind('<Return>', self.check_product)
        self.bin_pick_frame_qty_entry.configure(state='disabled')

        tote_name = "" + self.tote_zone
        self.tote_display = customtkinter.CTkLabel(bin_pick_frame, text="Tote: " + tote_name, font=("Roboto", 20)).pack(side='top', anchor = 'w', pady=1, padx=30) 

        self.short_cut_frame = customtkinter.CTkFrame(bin_pick_frame)
        self.short_cut_frame.pack(side='bottom', pady=20, padx=20)

        customtkinter.CTkLabel(master=self.short_cut_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=10)        
        self.bind = self.root.bind('<F3>', self.exit_bin_pick_view)

        customtkinter.CTkLabel(master=self.short_cut_frame, text="F5. Quantity", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=10)        
        self.bind = self.root.bind('<F5>', self.enable_qty_input)

        customtkinter.CTkLabel(master=self.short_cut_frame, text="F7. Enter Tote", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=10)        
        self.bind = self.root.bind('<F7>', self.input_pick_tote)

        self.tote_bind = self.root.bind('<F5>', self.enable_qty_input)

        raise_frame(self.curr_frame)

    def exit_bin_pick_view(self, event):
        self.tote_zone = ""
        self.root.unbind('<F3>', self.bind)
        self.go_to_zone_location()
        
    def enable_qty_input(self, event):
        state_condition = self.bin_pick_frame_qty_entry.cget("state")
        if(state_condition == 'disabled'):
            self.bin_pick_frame_qty_entry.configure(state='normal')
        elif(state_condition == 'normal'):
            num = self.bin_pick_frame_qty_entry.get()
            if(len(num) == 0):
                self.bin_pick_frame_qty_entry.insert(0, '1')
            self.bin_pick_frame_qty_entry.configure(state='disabled')

    def check_tote(self, event):
        tote_bin = 'PICK'
        tote_zone = self.tote_pick_frame_tote_entry_1.get()
        self.tote_zone = tote_zone

        check_tote_query = "SELECT PACKAGE_APPROVED_ZONE.BIN_AND_ZONE_EXISTS('PICK', '" +tote_zone+"') FROM DUAL"
        tote_result = pd.read_sql(check_tote_query, self.engine).iat[0,0]

        if(tote_result == 1):
            self.load_bin_pick_view()
        else:
            size = len(tote_zone)
            self.tote_pick_frame_tote_entry_1.delete(0,size)
        

    def input_pick_tote(self, event):
        self.curr_frame.destroy()
       
        self.tote_pick_frame = customtkinter.CTkFrame(master = self.root)
        self.tote_pick_frame.pack(pady=30, padx=10)
        self.curr_frame = self.tote_pick_frame

        self.tote_pick_frame_label_1 = customtkinter.CTkLabel(master=self.tote_pick_frame, text="Scan Tote", font=("Roboto", 34)).pack(pady=30, padx=10)

        # Work on the tote name
        self.tote_pick_frame_tote_entry_1 = customtkinter.CTkEntry(master=self.tote_pick_frame)
        self.tote_pick_frame_tote_entry_1.pack(pady=12, padx=10)
        self.tote_pick_frame_tote_entry_1.bind('<Return>', self.check_tote)

        self.short_cut_frame = customtkinter.CTkFrame(master = self.tote_pick_frame)
        self.short_cut_frame.pack(side='bottom', pady=20, padx=20)

        customtkinter.CTkLabel(master=self.short_cut_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=30)        
        self.bind = self.root.bind('<F3>', self.exit_tote_window)
        
        raise_frame(self.curr_frame)

    def exit_tote_window(self, event):
        self.root.unbind('<F3>', self.bind)
        self.load_bin_pick_view()
        
    def check_zone_location(self, event):
        input_zone = self.go_to_frame_entry_1.get().upper()

        if(self.zone_loc == input_zone):
            self.input_zone = input_zone
            self.load_bin_pick_view()
        else:
            size = len(input_zone)
            self.go_to_frame_entry_1.delete(0,size)
            

    def go_to_zone_location(self):
        self.curr_frame.destroy()
        
        go_to_frame = customtkinter.CTkFrame(master = self.root)
        go_to_frame.pack(pady=30, padx=10)
        self.curr_frame = go_to_frame
        
        bin_picked = self.bin_picked
        query = "SELECT DISTINCT ZONE_lOCATION FROM PICKS WHERE BIN_LOCATION = '"+bin_picked+"' AND PICK_STATUS = 'N' ORDER BY ZONE_LOCATION"
        zone_location_list = pd.read_sql(query, self.engine)
        
        if(zone_location_list.size == 0):
            self.load_picking_view()
        else:
            self.zone_loc = zone_location_list.iat[0,0]
            zone_loc = zone_location_list.iat[0,0]
            
            query = "SELECT ORDER_ID, PRODUCT_ID, QUANTITY, ZONE_LOCATION FROM PICKS " \
                        "WHERE ZONE_LOCATION = '" + zone_loc +"' AND PICK_STATUS = 'N' ORDER BY ZONE_LOCATION, ORDER_ID"
            self.zone_list = pd.read_sql(query, self.engine)

            customtkinter.CTkLabel(go_to_frame, text="Go to location: "+zone_loc, font=("Roboto", 34)).pack(pady=30, padx=10)

            self.go_to_frame_entry_1 = customtkinter.CTkEntry(go_to_frame)
            self.go_to_frame_entry_1.pack(pady=12, padx=10)
            self.go_to_frame_entry_1.bind('<Return>', self.check_zone_location)

            short_cut_frame = customtkinter.CTkFrame(go_to_frame)
            short_cut_frame.pack(side='bottom', pady=20, padx=20)

            customtkinter.CTkLabel(short_cut_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=30)        
            self.bind = self.root.bind('<F3>', self.exit_go_to_view)
        
            raise_frame(self.curr_frame)

    def exit_go_to_view(self, event):
        self.root.unbind('<F3>', self.bind)
        self.load_picking_view()        
        
    def check_picking_view(self, event):
        self.bin_picked = self.pick_frame_entry_1.get().upper()
        size = len(self.bin_picked)
        self.pick_frame_entry_1.delete(0,size)

        for i in range(0,int(self.pick_list.size/2)):
            if(str(self.pick_list.iat[i,0]) == self.bin_picked):
                self.go_to_zone_location()
        
    def load_picking_view(self):
        self.curr_frame.destroy()

        pick_frame = customtkinter.CTkFrame(master = self.root)
        pick_frame.pack(pady=30, padx=10)
        self.curr_frame = pick_frame                                           

        customtkinter.CTkLabel(pick_frame, text="Picking View", font=("Roboto", 40)).pack(side='top', pady=30, padx=10)      

        enter_bin_frame = customtkinter.CTkFrame(pick_frame)
        enter_bin_frame.pack(side='top', anchor = 'w', pady=10, padx=30)
        
        self.pick_frame_entry_1 = customtkinter.CTkEntry(enter_bin_frame, width = 30, font=("Roboto", 20))
        self.pick_frame_entry_1.pack(side='left', anchor = 'w', pady=1, padx=1)
        self.pick_frame_entry_1.bind('<Return>', self.check_picking_view)

        customtkinter.CTkLabel(enter_bin_frame, text="- Enter Bin", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=10)

        query = "SELECT BIN_LOCATION, SUM(QUANTITY) QUANTITY FROM PICKS WHERE TIME_PICKED IS NULL GROUP BY BIN_LOCATION ORDER BY BIN_LOCATION"

        self.pick_list = pd.read_sql(query, self.engine)       
        for i in range(int(self.pick_list.size/2)):
            bin_name = self.pick_list.iat[i,0]
            qty = self.pick_list.iat[i,1]
            pick_word = bin_name + ":\tPicks: " + str(qty)
            customtkinter.CTkLabel(pick_frame, text=pick_word, font=("Roboto", 20)).pack(side='top', pady=2, padx=30)

        short_cut_frame = customtkinter.CTkFrame(pick_frame)
        short_cut_frame.pack(side='bottom', pady=20, padx=20)

        customtkinter.CTkLabel(short_cut_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=30)        
        self.bind = self.root.bind('<F3>', self.exit_window)
        
        raise_frame(self.curr_frame)

    def exit_window(self, event):
        self.root.unbind('<F3>', self.bind)
        self.curr_frame.destroy()
        self.gui_application.display_command_window()
     
def raise_frame(frame):
    frame.tkraise()
            
