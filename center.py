#imports
import mysql.connector
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from random import seed
from random import randint
from array import *

# Connecting to mysql
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Shakti18",   # Change accordingly
  database="prec_agri"
)

dev_count = 0
seed(1)
print(mydb)  # for debugging
mycursor = mydb.cursor()
  # max() + 1
serial_num = 0

sql_query = "select max(rec_no) from dummydata"
mycursor.execute(sql_query)
myresult = mycursor.fetchone()


start_index = 0
if myresult[0] is None:
    start_index = 0

else: start_index = myresult[0]

serial_num = start_index+1
print(f'Starting from record number {start_index+1}')
# 3 separate dictionaries
dict_temp = dict()
dict_humid = dict()
dict_sm = dict()

for i in range(2):  # polling for 3 iterations (to be timed based on device delays)
    for _ in range(10):  # assume 10 devices for now

        now = datetime.now()
        temp_mean = randint(10,50)
        humid_mean = randint(10,100)
        soilmoist_mean = randint(5,100)
        dev_count += 1

# Using dictionaries
        dict_temp[f'{serial_num}'] = temp_mean
        dict_humid[f'{serial_num}'] = humid_mean
        dict_sm[f'{serial_num}'] = soilmoist_mean

        sql_query = "INSERT INTO dummydata  (rec_no, recdate, device_id, temperature, humid, soil_moist) VALUES(%s,%s,%s,%s,%s,%s)"
        values_query = (serial_num, now, dev_count, temp_mean,humid_mean,soilmoist_mean)
        mycursor.execute(sql_query,values_query)
        mydb.commit()
        serial_num += 1
    dev_count = 0
    i += 1
    # plotting

    print(f"{serial_num - 1} records inserted successfully")

print("All records inserted successfully!")
list_temp = sorted(dict_temp.items()) # sorted by key, return a list of tuples
x1, y1 = zip(*list_temp) # unpack a list of pairs into two tuples
list_humid = sorted(dict_humid.items()) # sorted by key, return a list of tuples
x2, y2 = zip(*list_humid) # unpack a list of pairs into two tuples
list_sm = sorted(dict_sm.items()) # sorted by key, return a list of tuples
x3, y3 = zip(*list_sm) # unpack a list of pairs into two tuples

plt.subplot(311)
plt.scatter(x1,y1,marker='o')
plt.xlabel('serial_num')
plt.ylabel('temperature')


plt.subplot(312)
plt.scatter(x2,y2,marker="o")
plt.xlabel('serial_num')
plt.ylabel('humidity')


plt.subplot(313)
plt.scatter(x3,y3,marker='o')
plt.xlabel('serial_num')
plt.ylabel('soil moisture')



sql_query = "select max(rec_no) from dummydata"
mycursor.execute(sql_query)
myresult = mycursor.fetchone()
serial_num = abs(int(start_index/20))


plt.savefig(f'sample{serial_num}.png')

plt.show()
