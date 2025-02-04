import oracledb
import pandas as pd
from Input_Command import command

from sqlalchemy import create_engine


query = "1";
input_command = command("Class")
input_command.print()
input_command.log_in() #-- Assume user has already logged in
# input_command.read_command()
input_command.read_command()



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


'''

