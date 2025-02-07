import oracledb
import pandas as pd
from Input_Command import command
from Data_Generator import code_generator

from sqlalchemy import create_engine


query = "1"
generator = code_generator("Name")
generator.log_in()
generator.generate_orders()
#input_command = command("Class")
#input_command.print()
#input_command.log_in() #-- Assume user has already logged in for debugging purpose
#input_command.read_command()



'''
TODOs
1. When prompted, ask the user for their username and password
2. Once logged in, show the commands avaialable for the user.
    - Start Picking
    - Stage Items
    - Process Orders
    - Move Parts
    - Process Receiving Items
3. Special inputs
    - Exit = Leave Window

4. Deal with exceptions if some inputs are incorrect.


'''


