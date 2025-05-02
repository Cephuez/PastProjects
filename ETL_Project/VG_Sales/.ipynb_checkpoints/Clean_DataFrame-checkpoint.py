import pyspark
from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, DoubleType

class Clean_Dataframe:
    def __init__(self):
        print("Initiated")

    def changeColType(self, df, dic, typ):
        for column in dic:
            if(typ == "int"):
                df = df.withColumn(column, col(column).cast(IntegerType()))
            elif(typ == "double"):
                df = df.withColumn(column, col(column).cast(DoubleType()))
        return df

    def check_data_mismatch(self):
        print("Checking Rows")
        
    def check_cap(self, word):
        if s is None:
            return False
        return s == s.title()