import oracledb
import pandas as pd
from Input_Command import command

from sqlalchemy import create_engine


query = "1";
input_command = command("Class")
input_command.print()
input_command.log_in()
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

'''
# connect to oracle database
cs = "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1522)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = orclpdb)))"
connection=oracledb.connect( user="project", password= "password123", dsn= cs)


#create engine
print(connection)
engine = create_engine('oracle+oracledb://', creator=lambda: connection)
#Get the data into a DataFrame
input_command.read_command()
query = input("Type Command")
query = "SELECT EMPLOYEE_ID, FIRST_NAME, LAST_NAME FROM EMPLOYEES ORDER BY 1"
df = pd.read_sql(query, engine)
# test data prep
df_test = df.copy()
 export test DataFrame with pandas to_sql
df_test.to_sql('test', con = engine, if_exists='replace', index=False)
print(df)
'''
'''
while query != "1":
    query = input("Type Command")
    query = "SELECT EMPLOYEE_ID, FIRST_NAME, LAST_NAME FROM EMPLOYEES ORDER BY 1"
    df = pd.read_sql(query, engine)
    # test data prep
    df_test = df.copy()
    # export test DataFrame with pandas to_sql
    df_test.to_sql('test', con = engine, if_exists='replace', index=False)
    print(df)
'''
