import oracledb
import pandas as pd
from Data_Generator import code_generator
from GUI_Application import gui_application

from sqlalchemy import create_engine

'''
    This allows the start up of the code.
    This will launch the application
'''

gui = gui_application("Name")
gui.print()
gui.log_in()
gui.beginning_screen()



