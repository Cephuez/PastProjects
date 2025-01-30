import oracledb
import pandas as pd
from Input_Command import command

from sqlalchemy import create_engine

#    dsn= "DESKTOP-J91G8VC/orclpdb"

# connect to oracle database
# dsn= "project@ORCLPDB"
cs = "(DESCRIPTION = (ADDRESS = (PROTOCOL = TCP)(HOST = localhost)(PORT = 1522)) (CONNECT_DATA = (SERVER = DEDICATED) (SERVICE_NAME = orclpdb)))"

connection=oracledb.connect( user="project", password= "password123", dsn= cs)
# create engine
engine = create_engine('oracle+oracledb://', creator=lambda: connection)
# Get the data into a DataFrame
query = "";
input_command = command("Class")
input_command.print()


while query != "1":
    query = input("Type Command")
    #query = "SELECT EMPLOYEE_ID, FIRST_NAME, LAST_NAME FROM EMPLOYEES ORDER BY 1"
    df = pd.read_sql(query, engine)
    # test data prep
    df_test = df.copy()
    # export test DataFrame with pandas to_sql
    df_test.to_sql('test', con = engine, if_exists='replace', index=False)
    print(df)
