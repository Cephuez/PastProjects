# Read CSV Files

import pandas as pd
import pyspark

df = pd.read_csv('Students_Grading_Dataset.csv')
print(df.head())

