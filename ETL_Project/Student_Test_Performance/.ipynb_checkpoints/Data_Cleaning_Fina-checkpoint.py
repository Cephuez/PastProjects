from pyspark.sql.functions import *
import pyspark
import json
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

class data_cleaning:
    def __init__(self,name):
        print("Class Created")
        print("")
        print("")

    def fix_column_names(self, df, dic_columns):
        for old_cols, new_cols in dic_columns.items():
            df = df.withColumnRenamed(old_cols, new_cols)
        return df

    def fix_strings(self, df, string_col):
        for column in string_col:
            df = df.withColumn(column, trim(initcap(lower(trim(col(column))))))
        return df


    def add_nulls(self, df, string_col):
        for cols in string_col:
            df = df.withColumn(cols, 
                                when(col(cols) == "", None).otherwise(col(cols)))
        return df

    def simplify_chars(self, df, charCols):
        for col_name in charCols:
            df = df.withColumn(col_name, substring(col(col_name),1,1))
        return df