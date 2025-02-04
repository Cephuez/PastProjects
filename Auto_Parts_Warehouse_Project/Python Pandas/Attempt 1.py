import oracledb
import getpass

userpassword = 'fafiluas121'

connection = oracledb.connect(user="Project@orclpdb", password=userpassword,
                              host="DESKTOP-J91G8VC", port=1521, service_name="orcl")

print(userpassword)
