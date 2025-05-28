#!/usr/bin/env python
# coding: utf-8

# In[65]:


import requests
import urllib.request
import httpx
import os
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')
import pandas as pd
import pyspark
import json
import pyarrow
from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException
from pyspark.sql import Row
from pyspark.sql.window import Window
from py4j.protocol import Py4JJavaError
from datetime import datetime, timedelta

from pyspark.sql.functions import *
from pyspark.sql.types import IntegerType, BooleanType

os.environ['SPARK_HOME'] = 'C:/Users/saul2/Spark_DF/spark-3.5.5-bin-hadoop3'
os.environ['HADOOP_HOME'] = 'C:/Users/saul2/Spark_DF/spark-3.5.5-bin-hadoop3'
os.environ['JAVA_HOME'] = 'C:/Program Files/Java/jdk1.8.0_202'


# In[67]:


# 45 Popular City Ids from around the world
city_ids = [
    "5128581", "2643743", "2988507", "1850147", "2147714", "2950159", "6167865", "3448433", "3530597", "1275339",
    "360630", "1816670", "524901", "292223", "3369157", "3169070", "1609350", "745044", "5368361", "1880252",
    "3435910", "1835848", "3117735", "1642911", "4887398", "3936456", "184745", "3871336", "108410", "1735161",
    "2332459", "756135", "2761369", "3067696", "3054643", "1701668", "2964574", "658225", "2800866", "2618425",
    "3143244", "2673730", "2759794", "2657896", "3413829", "264371", "112931", "98182", "1581130", "1668341",
    "2063523", "2193733", "5856195", "6173331", "293397", "2553604"
]
weather_api_key = "cd287a1f7182d4161353e9b62eaa2227"
ids = ",".join(city_ids)


# In[69]:


timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"50_City_{timestamp}.json"
with open(filename, "w") as f:
    for city_id in city_ids:
        url = f"http://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={weather_api_key}&units=metric"
        response = requests.get(url)
        
        #data = response.json()
        if response.status_code == 200:
            data = response.json()
            f.write(json.dumps(data) + "\n")
            #print(filename)
            #print(f"{data['name']}: {data['main']['temp']}°C")
        else:
            print(f"❌ Failed for city ID {city_id}: {response.status_code}")


# In[70]:


spark = SparkSession.builder.appName("Weather_Session").getOrCreate()


# In[71]:


try:
    df = spark.read.json(filename)
except AnalysisException  as e:
    # Path does not exists
    print(e)


# In[72]:


#df.show()


# In[73]:


# Create location DF
location_df = df.select(
    df["id"].alias("ID"),
    df["name"].alias("City"),
    df["sys.country"].alias("Country"),
    df["coord.lat"].alias("Latitude"),
    df["coord.lon"].alias("Longitude")
).orderBy("ID")


# In[74]:


# Create Temperature & Pressure Table
temperature_df = df.select(
    df["id"].alias("City_ID"),
    df["main.temp"].alias("Temp"),
    df["main.temp_max"].alias("Temp_Max"),
    df["main.temp_min"].alias("Temp_Min"),
    df["main.feels_like"].alias("Feels_Like"),
    df["main.humidity"].alias("Humidity"),
    df["main.pressure"].alias("Pressure"),
    df["main.sea_level"].alias("Sea_Level")
).orderBy("City_ID")


# In[75]:


# Create Wind & Clouds Table
wind_df = df.select(
    df["id"].alias("City_ID"),
    df["clouds.all"].alias("Cloudiness_Percentage"),
    df["wind.deg"].alias("Wind_Direction_Degree"),
    df["wind.gust"].alias("Gust_Speed"),
    df["wind.speed"].alias("Wind_Speed")
).orderBy("City_ID")


# In[76]:


# Create Weather Description
weather_desc_df = df.select(
    df["id"].alias("City_ID"),
    df["weather"][0]["main"].alias("Main_Weather"),
    df["weather"][0]["description"].alias("Description"),
    df["weather"][0]["icon"].alias("Icon")
).orderBy("City_ID")


# In[81]:


# Sunrise_Sunset_Table
sunrise_sunset_df = df.select(
    df["id"].alias("City_ID"),
    df["sys.sunrise"].alias("Sunrise"),
    df["sys.sunset"].alias("Sunset"),
    df["timezone"].alias("Timezone")
).orderBy("City_ID")


# In[86]:


# Which cities have the longest daylight duration?
# Convert the time into readable time. Order by daylight hour
top_10_cities = sunrise_sunset_df.select(
    col("City_ID"), 
    date_format(from_unixtime(col("Sunrise") + col("Timezone")),"HH:mm:ss").alias("Sunrise"),
    date_format(from_unixtime(col("Sunset") + col("Timezone")),"HH:mm:ss").alias("Sunset"), 
    round(((col("Sunset") - col("Sunrise")) / 3600),2).alias("Daylight_Hours"),
    col("Timezone")).orderBy(col("Daylight_Hours").desc()).limit(10)

final_table = top_10_cities.join(location_df, top_10_cities["City_ID"] == location_df["ID"]
                ).select(location_df["ID"], 
                         location_df["City"], 
                         location_df["Country"], 
                         top_10_cities["Sunrise"], 
                         top_10_cities["Sunset"], 
                         top_10_cities["Daylight_Hours"], 
                         top_10_cities["Timezone"]
                ).orderBy(col("Daylight_Hours").desc())
#final_table.show()

final_table.createOrReplaceTempView("Final_Table")

query = '''
        SELECT ID, CITY, COUNTRY, SUNRISE, SUNSET, DAYLIGHT_HOURS, TIMEZONE, RANK()OVER(ORDER BY DAYLIGHT_HOURS DESC) RANK
        FROM FINAL_TABLE
    '''
result = spark.sql(query)
result.show()


# In[88]:


# Which city has the highest difference between actual temperature and feels-like temperature?
# temperature_df
top_10_cities = temperature_df.select(
    col("City_ID"), 
    col("Temp"), 
    col("Feels_Like"), 
    round(abs(col("Temp") - col("Feels_Like")),2).alias("Difference")
        ).orderBy(col("Difference").desc()).limit(10)
#top_10_cities.show()

final_top_10_cities_temperature = top_10_cities.join(location_df, top_10_cities["City_ID"] == location_df["ID"]).select(
    top_10_cities["City_ID"], 
    location_df["City"], 
    location_df["Country"], 
    top_10_cities["Temp"], 
    top_10_cities["Feels_Like"], 
    top_10_cities["Difference"]
        ).orderBy(col("Difference").desc())
#final_top_10_cities_temperature.show()

final_top_10_cities_temperature.createOrReplaceTempView("Final_Table")

query = '''
        SELECT CITY_ID, CITY, COUNTRY, TEMP, FEELS_LIKE, DIFFERENCE, RANK()OVER(ORDER BY DIFFERENCE DESC) RANK
        FROM FINAL_TABLE
    '''

final_result = spark.sql(query)
final_result.show()


# In[ ]:




