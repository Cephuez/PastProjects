import pyspark
from pyspark.sql.functions import *
from pyspark.sql.types import *

'''
    1. Check for missing and blank values
    2. Check for inconsistent Capitalization
    3. Check for duplicate rows
    4. Check column names / reformat them
    5. Check if some values inputted are valid
    6. Check if any values are consistent (int is valid input, double, etc)
    7. Check data type consistency
    8. Check value format("Bachelor's vs Bachelors")
    9. Decide if you have to add null or not
    10. Encoding issues. (utf-8 vs latin1)

'''
class Clean_Dataframe:

    def __init__(self):
        print("Initiated")

    # 1 Check for missing and blank values
    def check_missing_blank_values(self, df):
        final_condition = None
        for column in df.columns:
            # Build condition to only allow distinct rows
            condition = (trim(col(column)) == "") | col(column).isNull()

            # This will add multiple conditions so it gets filter in one go
            final_condition = condition if final_condition is None else final_condition | condition

        bad_rows = df.filter(final_condition)
        if(bad_rows.count() > 0):
            bad_rows.show()


    # 2 Check for capitalization
    def check_capitalization(self, df, string_col_dic):
        final_condition = None
        for column in string_col_dic:
            condition = col(column) != initcap(col(column))
            final_condition = condition if final_condition is None else final_condition | condition
            
        bad_rows = df.filter(final_condition)
        if(bad_rows.count() > 0):
            bad_rows.show(50, False)

    def check_individual_capitalization(self, df, column):
        df.filter(col(column) != initcap(col(column))).select("Rank",column).dropDuplicates([column]).orderBy("Rank").distinct().show()

    def check_more_individual_capitalization(self, df, column, rowNum):
        df.filter(col(column) != initcap(col(column))).select("Rank",column).dropDuplicates([column]).orderBy("Rank").show(rowNum, False)

    # 3 Check for duplicate Rows
    def check_duplicate_rows(self, df):
        duplicate_rows = df.groupBy(df.columns).count().filter("count > 1")
        duplicate_rows.show()

    # 4 Change them to their types / Check wrong values
    def checkTypeChange(self, df, dic, typ):
        for column in dic:
            if(typ == "int"):
                # Don't filter if 
                # - Value is NULL
                # - Value is N/A
                filtered = df.filter((col(column).isNotNull()) & (col(column) != lit("N/A")))

                # Create a temporary table that shows the changes
                temp_col = "Int Col"
                filtered = filtered.withColumn(temp_col, col(column).cast(IntegerType()))

                # Only show columns that were turned to NULL
                nullTable = filtered.filter(col(temp_col).isNull())
    
                # Now show me which values were turned to null
                nullTable.select("Rank", column).show(truncate=False)
            elif(typ == "double"):
                # Don't filter if 
                # - Value is NULL
                filtered = df.filter(col(column).isNotNull())

                temp_col = "Double Col"
                filtered = filtered.withColumn(temp_col, col(column).cast(IntegerType()))

                nullTable = filtered.filter(col(temp_col).isNull())
                
                nullTable.select("Rank", column).orderBy(col("Rank")).show(truncate=False)

    # 
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