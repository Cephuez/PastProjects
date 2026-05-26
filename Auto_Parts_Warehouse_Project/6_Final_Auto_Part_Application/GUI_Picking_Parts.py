import customtkinter
import tkinter
import requests
#from GUI_Application import gui_application


'''
    User will go to Zones (A-F), where they will pick items for a customer order
    They will go to each Zone and make sure they pick an exact amount of QTY from each product
'''

class Picking_Parts_Window:
    engine = ""
    cs = ""
    connection = ""
    name = ""
    root = ""
    label = ""
    #entry1 = ""


    def __init__(self, gui_application, name, connection, engine, root, frame2, token):
        self.gui_application = gui_application
        self.name = name
        self.connection = connection
        self.engine = engine
        self.root = root
        self.curr_frame = frame2
        self.tote_zone = ""
        self.token = token


    def update_product_view(self):
        zone_loc = self.zone_loc

        # Returns an updated list after the parts have been picked
        product_zone_list = requests.get(
            'https://warehouse-api-wnnm.onrender.com/return-updated-view',
            params={'zone_loc': zone_loc},
            headers={"Auth": self.token}
        ).json()
        
        self.product_zone_list = product_zone_list

        if(len(self.product_zone_list) == 0):
            self.tote_zone = ""
            self.root.unbind('<F3>', self.bind)
            self.go_to_zone_location()
        else:
            product_id = self.product_zone_list[0][0]
            qty = self.product_zone_list[0][1]
            zone_loc = self.product_zone_list[0][2]
            product_name = self.product_zone_list[0][3]
            
            bin_loc = self.bin_picked
            self.loc = zone_loc

            self.bin_pick_frame_product.configure(text = "Product: " + str(product_id))
            self.bin_pick_frame_quantity.configure(text = "QTY: " + str(qty))
            self.bin_pick_frame_zone.configure(text = "Zone: " + bin_loc + " " + zone_loc)
            self.bin_pick_part_name.configure(text = "Part Name: " + str(product_name))
        
        
    def check_product(self,event):
        if(len(self.tote_zone) > 0):
            self.bin_pick_frame_qty_entry.configure(state='normal')
            input_product_id = self.bin_pick_frame_entry1.get()
            input_qty = self.bin_pick_frame_qty_entry.get()

            product_id = self.product_zone_list[0][0]
            
            zone_loc = self.zone_loc
            bin_loc = self.bin_picked
            tote_zone = self.tote_zone
            if(str(input_product_id) == str(product_id)):
                # Check if the inputted qty is not more than the number required to be moved
                qty_result_dic = requests.get(
                    'https://warehouse-api-wnnm.onrender.com/check-quantity-input',
                    params={'product_id': product_id, 'input_qty': input_qty, 'bin_loc': bin_loc, 'zone_loc': zone_loc},
                    headers={"Auth": self.token}
                ).json()
                
                qty_result = qty_result_dic[0][0]
                if(qty_result == 1):
                    size = len(input_product_id)
                    self.bin_pick_frame_entry1.delete(0,size)
                    size = len(input_qty)
                    self.bin_pick_frame_qty_entry.delete(0,size)
                    self.bin_pick_frame_qty_entry.insert(0, '1')
                    self.qty_input_state_change()                   

                    # Move the parts from their storage area to a bin for processing later
                    qty_result_dic = requests.get(
                        'https://warehouse-api-wnnm.onrender.com/process-pick',
                        params={'product_id': product_id, 'input_qty': input_qty, 'bin_loc': bin_loc, 'zone_loc': zone_loc, 'tote_zone': tote_zone},
                        headers={"Auth": self.token}
                    ).json()
                    
                    self.update_product_view()
                else:
                    self.root.bell()
            else:
                size = len(input_product_id)
                self.bin_pick_frame_entry1.delete(0,size)
                self.root.bell()
        else:
            self.root.bell()
            self.tote_display.configure(text="Tote: Enter Valid Tote")

    def validate_entry(self, new_text):
        if not new_text:
            return True
        try:
            int(new_text)
            return True
        except ValueError:
            return False
    
    def load_bin_pick_view(self):
        zone_loc = self.input_zone
        self.curr_frame.destroy()
        
        bin_loc = self.bin_picked
        
        bin_pick_frame = customtkinter.CTkFrame(master = self.root)
        bin_pick_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.curr_frame = bin_pick_frame

        customtkinter.CTkLabel(bin_pick_frame, text="Picking List", font=("Roboto", 40)).pack(pady=12, padx=10)

        # Returns a list of products that must be picked from a Zone location
        self.product_zone_list = requests.get(
            'https://warehouse-api-wnnm.onrender.com/load-bin-info',
            params={'zone_loc': zone_loc},
            headers={"Auth": self.token}
        ).json()

        product_id = self.product_zone_list[0][0]
        quantity = self.product_zone_list[0][1]
        product_name = self.product_zone_list[0][3]
        

        pd_frame = customtkinter.CTkFrame(bin_pick_frame)
        pd_frame.pack(side='top', pady=10, padx=10)

        d_product = "Product: " + str(product_id)
        self.bin_pick_frame_product = customtkinter.CTkLabel(pd_frame, text=d_product, font=("Roboto", 20))
        self.bin_pick_frame_product.pack(side='left',pady=2, padx=10)

        d_quantity = "QTY: " + str(quantity)
        self.bin_pick_frame_quantity = customtkinter.CTkLabel(pd_frame, text=d_quantity, font=("Roboto", 20))
        self.bin_pick_frame_quantity.pack(side='left', pady=2, padx=10)

        d_location = "Zone: " + bin_loc + " " +zone_loc
        self.bin_pick_frame_zone = customtkinter.CTkLabel(pd_frame, text=d_location, font=("Roboto", 20))
        self.bin_pick_frame_zone.pack(side='left',pady=2, padx=10)

        d_part_name = "Part Name: " + str(product_name)
        self.bin_pick_part_name = customtkinter.CTkLabel(bin_pick_frame, text=d_part_name, font=("Roboto", 20))
        self.bin_pick_part_name.pack(pady=2, padx=10)
        

        s_frame = customtkinter.CTkFrame(bin_pick_frame)
        s_frame.pack(side='top', pady=10, padx=10)

        customtkinter.CTkLabel(s_frame, text="Scan: ", font=("Roboto", 20)).pack(side='left', anchor='w', pady=4, padx=5)
        
        self.bin_pick_frame_entry1 = customtkinter.CTkEntry(s_frame, justify='center', font=("Roboto", 16))
        self.bin_pick_frame_entry1.pack(side='left', anchor='w', pady=4, padx=5)
        self.bin_pick_frame_entry1.bind('<Return>', self.check_product)
        self.bin_pick_frame_entry1.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.bin_pick_frame_entry1))
        self.bin_pick_frame_entry1.focus_set()

        self.bin_pick_frame_qty_input = customtkinter.CTkLabel(s_frame, text="QTY: ", font=("Roboto", 20))
        self.bin_pick_frame_qty_input.pack(side='left', anchor='w', pady=4, padx=5)

        validation = self.root.register(self.validate_entry)
        self.bin_pick_frame_qty_entry = customtkinter.CTkEntry(s_frame, justify='center', width = 50, font=("Roboto", 16), validate="key", validatecommand=(validation, "%P"))
        self.bin_pick_frame_qty_entry.insert(0, '1')
        self.bin_pick_frame_qty_entry.pack(side='left', anchor='w', pady=4, padx=5)
        self.bin_pick_frame_qty_entry.bind('<Return>', self.check_product)
        self.bin_pick_frame_qty_entry.configure(state='disabled')

        tote_name = "" + self.tote_zone
        self.tote_display = customtkinter.CTkLabel(bin_pick_frame, text="Tote: " + tote_name, font=("Roboto", 20))
        self.tote_display.pack(side='top', anchor = 'w', pady=1, padx=30)

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind = self.root.bind('<F3>', self.exit_bin_pick_view)

        customtkinter.CTkLabel(self.curr_frame, text="F5. QTY", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25) 
        self.bind = self.root.bind('<F5>', self.enable_qty_input)

        customtkinter.CTkLabel(self.curr_frame, text="F7. Tote", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)        
        self.bind = self.root.bind('<F7>', self.input_pick_tote)

        self.tote_bind = self.root.bind('<F5>', self.enable_qty_input)

        raise_frame(self.curr_frame)

    def exit_bin_pick_view(self, event):
        self.tote_zone = ""
        self.root.unbind('<F3>', self.bind)
        self.go_to_zone_location()

    def qty_input_state_change(self):
        state_condition = self.bin_pick_frame_qty_entry.cget("state")
        if(state_condition == 'disabled'):
            self.bin_pick_frame_qty_entry.configure(state='normal')
            self.bin_pick_frame_qty_entry.focus_set()
        elif(state_condition == 'normal'):
            num = self.bin_pick_frame_qty_entry.get()
            if(len(num) == 0):
                self.bin_pick_frame_qty_entry.insert(0, '1')
            self.bin_pick_frame_qty_entry.configure(state='disabled')
            self.bin_pick_frame_entry1.focus_set()

    def enable_qty_input(self, event):
        self.qty_input_state_change()

    def check_tote(self, event):
        tote_bin = 'PICK'
        tote_zone = self.tote_pick_frame_tote_entry_1.get()

        # Check if inputted tote name is correct
        check_tote_query = requests.get(
            'https://warehouse-api-wnnm.onrender.com/check-tote',
            params={'tote_zone': tote_zone},
            headers={"Auth": self.token}
        ).json()
        
        tote_result = check_tote_query[0][0]

        if(tote_result == 1):
            self.tote_zone = tote_zone
            self.load_bin_pick_view()
        else:
            self.root.bell()
            size = len(tote_zone)
            self.tote_pick_frame_tote_entry_1.delete(0,size)
        

    def input_pick_tote(self, event):
        self.curr_frame.destroy()
       
        self.tote_pick_frame = customtkinter.CTkFrame(master = self.root)
        self.tote_pick_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = self.tote_pick_frame

        self.tote_pick_frame_label_1 = customtkinter.CTkLabel(master=self.tote_pick_frame, text="Scan Tote", font=("Roboto", 40)).pack(pady=12, padx=10)

        self.tote_pick_frame_tote_entry_1 = customtkinter.CTkEntry(master=self.tote_pick_frame, font=("Roboto", 16), width = 220)
        self.tote_pick_frame_tote_entry_1.pack(pady=12, padx=10)
        self.tote_pick_frame_tote_entry_1.bind('<Return>', self.check_tote)
        self.tote_pick_frame_tote_entry_1.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.tote_pick_frame_tote_entry_1))
        self.tote_pick_frame_tote_entry_1.focus_set()

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='bottom', anchor = 'w', pady=10, padx=25)
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
            self.root.bell()
            size = len(input_zone)
            self.go_to_frame_entry_1.delete(0,size)
            

    def go_to_zone_location(self):
        self.curr_frame.destroy()
        
        go_to_frame = customtkinter.CTkFrame(master = self.root)
        go_to_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = go_to_frame
        
        bin_picked = self.bin_picked

        # Give a list to display what zones need picking
        zone_location_list = requests.get(
            'https://warehouse-api-wnnm.onrender.com/bin-display',
            params={'bin_picked': bin_picked},
            headers={"Auth": self.token}
        ).json()
        print(zone_location_list)
        
        if(len(zone_location_list) == 0):
            self.load_picking_view()
        else:
            self.zone_loc = zone_location_list[0][0]
            zone_loc = zone_location_list[0][0]

            customtkinter.CTkLabel(go_to_frame, text="Go to location: "+zone_loc, font=("Roboto", 40)).pack(pady=12, padx=10)

            self.go_to_frame_entry_1 = customtkinter.CTkEntry(go_to_frame, font=("Roboto", 16))
            self.go_to_frame_entry_1.pack(pady=12, padx=10)
            self.go_to_frame_entry_1.bind('<Return>', self.check_zone_location)
            self.go_to_frame_entry_1.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.go_to_frame_entry_1))
            self.go_to_frame_entry_1.focus_set()

            customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='bottom', anchor = 'w', pady=10, padx=25)
            self.bind = self.root.bind('<F3>', self.exit_go_to_view)
        
            raise_frame(self.curr_frame)

    def exit_go_to_view(self, event):
        self.root.unbind('<F3>', self.bind)
        self.load_picking_view()        
        
    def check_picking_view(self, event):
        self.bin_picked = self.pick_frame_entry_1.get().upper()
        size = len(self.bin_picked)
        self.pick_frame_entry_1.delete(0,size)
        print(self.pick_list)
        for i in range(0, int(len(self.pick_list))):
            # print(self.bin_picked)
            if(str(self.pick_list[i][0]) == self.bin_picked):
                self.go_to_zone_location()
                break
            elif(i == int(len(self.pick_list)) - 1):
                self.root.bell()

    def to_uppercase(self, frame):
        input_text = frame.get()
        length = len(input_text)
        frame.delete(0,length)
        frame.insert(0,input_text.upper())
            
    def load_picking_view(self):
        self.curr_frame.destroy()

        pick_frame = customtkinter.CTkFrame(master = self.root)
        pick_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = pick_frame                                           

        customtkinter.CTkLabel(pick_frame, text="Picking View", font=("Roboto", 40)).pack(side='top', pady=12, padx=10)      

        enter_bin_frame = customtkinter.CTkFrame(pick_frame)
        enter_bin_frame.pack(side='top')
     
        self.pick_frame_entry_1 = customtkinter.CTkEntry(enter_bin_frame, width = 80, font=("Roboto", 16))
        self.pick_frame_entry_1.pack(side='left', anchor = 'w', pady=2, padx=10)
        self.pick_frame_entry_1.bind('<Return>', self.check_picking_view)
        self.pick_frame_entry_1.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.pick_frame_entry_1))
        self.pick_frame_entry_1.focus_set()

        # Returns a list of the Bins that need to be pick
        customtkinter.CTkLabel(enter_bin_frame, text="- Enter Bin", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=10)
        self.pick_list = requests.get(
            'https://warehouse-api-wnnm.onrender.com/pick-list',
            headers={"Auth": self.token}
        ).json()
        
        for rows in self.pick_list:
            bin_name = rows[0]
            qty = rows[1]
            pick_word = str(bin_name) + ":\tPicks: " + str(qty) 
            customtkinter.CTkLabel(pick_frame, text=pick_word, font=("Roboto", 20)).pack(side='top', anchor='w', pady=2, padx=100)

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='bottom', anchor = 'w', pady=10, padx=25)
        self.bind = self.root.bind('<F3>', self.exit_window)
        
        raise_frame(self.curr_frame)

    def exit_window(self, event):
        self.root.unbind('<F3>', self.bind)
        self.curr_frame.destroy()
        self.gui_application.display_command_window()
     
def raise_frame(frame):
    frame.tkraise()
            
