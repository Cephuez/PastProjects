import customtkinter
import tkinter
import requests

'''
    Will display the view that allows the user to gather parts for a customer order
    User will move parts from their staging location to a tote to be processed as
    a completed order
'''
class Gather_Parts_Window:
    engine = ""
    cs = ""
    connection = ""
    name = ""
    root = ""
    label = ""


    def __init__(self, gui_application, name, connection, engine, root, frame2, token):
        self.gui_application = gui_application
        self.name = name
        self.connection = connection
        self.engine = engine
        self.root = root
        self.curr_frame = frame2
        self.token = token

    def update_product_view(self):
        # Returns an updated list telling user next Stage location to go to
        shelf_list = requests.get(
            'https://warehouse-api-wnnm.onrender.com/get-updated-order-view',
            params={'order_id': self.order_id, 'curr_stage': self.curr_stage},
            headers={"Auth": self.token}
        ).json()

        if(len(shelf_list) == 0):
            self.load_staging_view()
        else:
            product_id = shelf_list[0][0]
            qty = shelf_list[0][1]
            part_name = shelf_list[0][2]
            self.product_id = product_id

            size = len(self.shelf_view_product_entry.get())
            self.shelf_view_product_entry.delete(0, size)

            self.product_info_show_product.configure(text = "Product: " + str(product_id))
            self.product_info_show_quantity.configure(text = "QTY: " + str(qty))
            self.bin_pick_part_name.configure(text = "Part Name: " + str(part_name))    

    def check_product(self,event):
        self.shelf_view_quantity_entry.configure(state='normal')
        input_product_id = self.shelf_view_product_entry.get()
        input_qty = self.shelf_view_quantity_entry.get()

        if(str(input_product_id) == str(self.product_id)):
            # Check inputted product quantity is not more than the desired number
            qty_result_dic = requests.get(
                'https://warehouse-api-wnnm.onrender.com/check-total-product-qty',
                params={'order_id': self.order_id, 'input_product_id': str(input_product_id),'curr_stage': self.curr_stage},
                headers={"Auth": self.token}
            ).json()
            qty_result = qty_result_dic[0][0]
            

            if(int(input_qty) <= int(qty_result)):
                # Move product from Stage to Comp
                requests.get(
                    'https://warehouse-api-wnnm.onrender.com/move-stage-to-box',
                    params={'order_id': self.order_id, 'input_product_id': str(input_product_id),'input_qty': input_qty,
                            'curr_stage': self.curr_stage, 'box_tote': self.box_tote},
                    headers={"Auth": self.token}
                    )
                
                self.shelf_view_quantity_entry.configure(state='disabled')
                self.update_product_view()
            else:
                self.root.bell()
                self.shelf_view_quantity_entry.focus_set()
        else:
            self.root.bell()
            length = len(input_product_id)
            self.shelf_view_product_entry.delete(0, length)

    def display_product_in_shelf_view(self):
        self.curr_frame.destroy()

        shelf_view_frame = customtkinter.CTkFrame(master = self.root)
        shelf_view_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = shelf_view_frame

        shelf_view_label = customtkinter.CTkLabel(shelf_view_frame, text="Pick Part From Shelf", font=("Roboto", 40))
        shelf_view_label.pack(pady=12, padx=10)

        # Gives a list telling user how many parts to scan from Stage location
        shelf_list = requests.get(
            'https://warehouse-api-wnnm.onrender.com/get-order-scan-list',
            params={'order_id': self.order_id, 'curr_stage': self.curr_stage},
            headers={"Auth": self.token}
        ).json()

        self.product_id = shelf_list[0][0]
        self.quantity = shelf_list[0][1]
        part_name = shelf_list[0][2]       
        
        tote_text = "Tote: " + self.box_tote
        customtkinter.CTkLabel(shelf_view_frame, text=tote_text, font=("Roboto", 20)).pack(pady=10, padx=10)

        display_info_frame = customtkinter.CTkFrame(shelf_view_frame)
        display_info_frame.pack(side='top', pady=10, padx=30)

        display_product = "Product: " + str(self.product_id)
        self.product_info_show_product = customtkinter.CTkLabel(display_info_frame, text=display_product, font=("Roboto", 20))
        self.product_info_show_product.pack(side='left', anchor='w',pady=4, padx=10)

        display_quantity = "QTY: " + str(self.quantity)
        self.product_info_show_quantity = customtkinter.CTkLabel(display_info_frame, text=display_quantity, font=("Roboto", 20))
        self.product_info_show_quantity.pack(side='left', anchor='w',pady=4, padx=10)

        scan_frame = customtkinter.CTkFrame(shelf_view_frame)
        scan_frame.pack(side='top', anchor='w', pady=10, padx=10)
        
        customtkinter.CTkLabel(scan_frame, text="Scan Product:", font=("Roboto", 20)).pack(side='left', anchor='w',pady=4, padx=10)  

        self.shelf_view_product_entry = customtkinter.CTkEntry(scan_frame, width = 110, font=("Roboto", 16))
        self.shelf_view_product_entry.pack(side='left', anchor='w',pady=2, padx=2)
        self.shelf_view_product_entry.bind('<Return>', self.check_product)
        self.shelf_view_product_entry.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.shelf_view_product_entry))
        self.shelf_view_product_entry.focus_set()

        self.quantity_frame = customtkinter.CTkLabel(scan_frame,text="QTY: ",font=("Roboto",20), width=60)
        self.quantity_frame.pack(side='left', anchor='w', pady=2, padx=2)  

        validation = self.root.register(self.validate_entry)
        self.shelf_view_quantity_entry = customtkinter.CTkEntry(scan_frame, width = 55, font=("Roboto", 16), validate="key",validatecommand=(validation,"%P"))
        self.shelf_view_quantity_entry.insert(0, '1')
        self.shelf_view_quantity_entry.pack(side='left', anchor='w',pady=2, padx=2)
        self.shelf_view_quantity_entry.bind('<Return>', self.check_product)
        self.shelf_view_quantity_entry.configure(state='disabled')

        d_part_name = "Part Name: " + part_name
        self.bin_pick_part_name = customtkinter.CTkLabel(shelf_view_frame, text=d_part_name, font=("Roboto", 20))
        self.bin_pick_part_name.pack(pady=2, padx=10)

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind_exit = self.root.bind('<F3>', self.exit_display_product_view)

        customtkinter.CTkLabel(self.curr_frame, text="F5. QTY", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25) 
        self.bind_qty = self.root.bind('<F5>', self.enable_qty_input)

        raise_frame(self.curr_frame)

    def exit_display_product_view(self, event):
        self.root.unbind('<F3>', self.bind_exit)
        self.root.unbind('<F5>', self.bind_qty)
        self.curr_frame.destroy()
        self.load_staging_view()        

    def enable_qty_input(self, event):
        state_condition = self.shelf_view_quantity_entry.cget("state")
        if(state_condition == 'disabled'):
            self.shelf_view_quantity_entry.configure(state='normal')
            self.shelf_view_quantity_entry.focus_set()
        elif(state_condition == 'normal'):
            num = self.shelf_view_quantity_entry.get()
            if(len(num) == 0):
                self.shelf_view_quantity_entry.insert(0, '1')
            self.shelf_view_quantity_entry.configure(state='disabled')
            self.shelf_view_product_entry.focus_set()
            
    def check_stage_input(self,event):
        stage_input = self.staging_view_entry.get()
        if(stage_input == self.curr_stage):
            self.display_product_in_shelf_view()
        else:
            self.root.bell()
            length = len(stage_input)
            self.staging_view_entry.delete(0,length)

    def load_staging_view(self):
        self.curr_frame.destroy()

        staging_view_frame = customtkinter.CTkFrame(master = self.root)
        staging_view_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = staging_view_frame

        # Get list of Stage locations where user will get parts for the current Order
        get_stage_list = requests.get(
            'https://warehouse-api-wnnm.onrender.com/get-zone-loc-for-order',
            params={'order_id': self.order_id},
            headers={"Auth": self.token}
        ).json()

        if(len(get_stage_list) == 0):
            self.root.unbind('<F3>', self.bind)
            self.load_gather_parts_view()
        else:
            self.curr_stage = get_stage_list[0][0]

            customtkinter.CTkLabel(staging_view_frame, text="Order ID: " + str(self.order_id), font=("Roboto", 40)).pack(side='top', pady=12, padx=10)
            
            stage_display = "Scan Stage: " + self.curr_stage
            customtkinter.CTkLabel(staging_view_frame, text=stage_display, font=("Roboto", 20)).pack(side='top', pady=10, padx=2)

            self.staging_view_entry = customtkinter.CTkEntry(staging_view_frame, font=("Roboto", 16))
            self.staging_view_entry.pack(side='top', pady=12, padx=10)
            self.staging_view_entry.bind('<Return>', self.check_stage_input)
            self.staging_view_entry.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.staging_view_entry))
            self.staging_view_entry.focus_set()

            customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
            self.bind = self.root.bind('<F3>', self.exit_load_staging_view)

            raise_frame(self.curr_frame)

    def exit_load_staging_view(self, event):
        self.root.unbind('<F3>', self.bind)
        self.curr_frame.destroy()
        self.load_input_box_view()
        

    def check_input_box(self, event):
        self.box_tote = self.scan_box_entry.get()

        # Check if inputted Tote exists
        tote_exists_dic = requests.get(
            'https://warehouse-api-wnnm.onrender.com/check-tote-exist',
            params={'box_tote': self.box_tote},
            headers={"Auth": self.token}
        ).json()
        tote_exists = tote_exists_dic[0][0]

        # Check if Tote is available for use
        empty_tote_dic = requests.get(
            'https://warehouse-api-wnnm.onrender.com/check-available-tote',
            params={'box_tote': self.box_tote, 'order_id': str(self.order_id)},
            headers={"Auth": self.token}
        ).json()
        empty_tote = empty_tote_dic[0][0]

        if(int(tote_exists) == 1 and int(empty_tote) == 0):
            self.load_staging_view()
        else:
            self.root.bell()
            self.tote_indicator.configure(text="Empty Or Incorrect Tote")
            size = len(self.box_tote)
            self.scan_box_entry.delete(0,size)
        
    def load_input_box_view(self):
        self.curr_frame.destroy()

        box_display_frame = customtkinter.CTkFrame(master = self.root)
        box_display_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = box_display_frame

        customtkinter.CTkLabel(box_display_frame, text="Order ID: " + str(self.order_id), font=("Roboto", 40)).pack(side='top', pady=12, padx=10)

        scan_box_frame = customtkinter.CTkFrame(box_display_frame)
        scan_box_frame.pack(side='top', anchor = 'w', pady=10, padx=30)

        customtkinter.CTkLabel(scan_box_frame, text="Scan Box: ", font=("Roboto", 20)).pack(side='left', anchor='w', pady=10, padx=10)

        self.scan_box_entry = customtkinter.CTkEntry(scan_box_frame, font=("Roboto", 16), width = 220)
        self.scan_box_entry.pack(side='left', anchor='w', pady=12, padx=10)
        self.scan_box_entry.bind('<Return>', self.check_input_box)
        self.scan_box_entry.bind('<KeyRelease>', lambda eff:self.to_uppercase(self.scan_box_entry))
        self.scan_box_entry.focus_set()

        self.tote_indicator = customtkinter.CTkLabel(box_display_frame, text="", font=("Roboto", 20))
        self.tote_indicator.pack(side = 'top', pady=10, padx=10)

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind = self.root.bind('<F3>', self.exit_load_input_box_view)

        raise_frame(self.curr_frame)

    def exit_load_input_box_view(self, event):
        self.root.unbind('<F3>', self.bind)
        self.curr_frame.destroy()
        self.load_gather_parts_view()

    def check_order_id(self, event):
        self.order_id = self.gather_parts_enter_product.get()
        if(int(self.order_id) in self.order_list):
            self.load_input_box_view()
            
        else:
            self.root.bell()
            size = len(self.order_id)
            self.gather_parts_enter_product.delete(0,size)

    def load_gather_parts_view(self):
        self.curr_frame.destroy()

        self.order_list = []
        self.i = 0
        self.box_tote = ""
        gather_parts_frame = customtkinter.CTkFrame(master = self.root)
        gather_parts_frame.pack(pady=20, padx=20, fill="both", expand=True)
        self.curr_frame = gather_parts_frame

        customtkinter.CTkLabel(gather_parts_frame, text="Orders Ready List", font=("Roboto", 40)).pack(side='top', pady=12, padx=10)

        enter_order_id_frame = customtkinter.CTkFrame(gather_parts_frame)
        enter_order_id_frame.pack(side='top', anchor = 'w', pady=5, padx=30)

        customtkinter.CTkLabel(enter_order_id_frame, text="Order: ", font=("Roboto", 20)).pack(side='left', anchor = 'w', pady=1, padx=10)

        validation = self.root.register(self.validate_entry)
        self.gather_parts_enter_product = customtkinter.CTkEntry(enter_order_id_frame, font=("Roboto", 16), width = 80, validate="key", validatecommand=(validation, "%P"))
        self.gather_parts_enter_product.pack(pady=1, padx=1)
        self.gather_parts_enter_product.bind('<Return>', self.check_order_id)
        self.gather_parts_enter_product.focus_set()

        # Get a list of Order IDs that are ready to be picked from Stage location
        all_order_list = requests.get(
            'https://warehouse-api-wnnm.onrender.com/get-order-ids',
            headers={"Auth": self.token}
        ).json()
        list_length = len(all_order_list)

        self.order_id_list_frame = customtkinter.CTkFrame(gather_parts_frame)
        self.order_id_list_frame.pack(side='top', anchor = 'w', pady=10, padx=30)

        for i in range(list_length):
            order_id = all_order_list[i][0]
            self.order_list.append(int(order_id))
            
        self.temp_label = []
        self.display_order_list()
        self.display_extra_order()

        customtkinter.CTkLabel(self.curr_frame, text="F3. Exit", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind_exit = self.root.bind('<F3>', self.exit_window)

        customtkinter.CTkLabel(self.curr_frame, text="F5. Prev", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25) 
        self.bind_exit = self.root.bind('<F5>', self.prev_page)

        customtkinter.CTkLabel(self.curr_frame, text="F7. Next", font=("Roboto", 20)).pack(side='left', anchor = 'sw', pady=10, padx=25)
        self.bind_exit = self.root.bind('<F7>', self.next_page)
        
        raise_frame(self.curr_frame)

    def display_order_list(self):
        if(len(self.temp_label) > 0 ):
            for label in self.temp_label:
                label.destroy()
            self.temp_label = []
        min_i = self.i
        for i in range(min_i, len(self.order_list)):
            if(i == min_i+6):
                break
            order_id = self.order_list[i]
            id_text = "Order: " + str(order_id)
            id_extra_order =  "     \t" + "Order: " + str(order_id)
            order_label = customtkinter.CTkLabel(self.order_id_list_frame, text=id_text, font=("Roboto", 20))
            order_label.pack(side='top', anchor = 'w', pady=2, padx=10)
            self.temp_label.append(order_label)

    def display_extra_order(self):
        min_i = self.i + 6
        for i in range(min_i, len(self.order_list)):
            if(i == min_i+6):
                break
            x = i % 6

            label_text = self.temp_label[x]
            order_text = label_text.cget('text')
            next_order = "Order: " + str(self.order_list[i])
            o_text = order_text + "     \t" + next_order

            
            label_text.configure(text=o_text)

    def prev_page(self, event):
        self.i = self.i - 12
        if(self.i < 0):
            self.i = 0
        self.display_order_list()
        self.display_extra_order()

    def next_page(self, event):
        if(self.i + 12 < len(self.order_list)):
            self.i = self.i + 12
        self.display_order_list()
        self.display_extra_order()
        
    def exit_window(self, event):
        self.root.unbind('<F3>', self.bind_exit)
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
