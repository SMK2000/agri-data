import mysql.connector
import time  # FOR the time.sleep()
from datetime import datetime
from random import seed
from random import randint


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

for i in range(3):  # polling for 3 iterations (to be timed based on device delays)
    for _ in range(10):  # assume 10 devices for now
        now = datetime.now()
        temp_mean = randint(10,50)
        humid_mean = randint(10,100)
        soilmoist_mean = randint(5,100)
        dev_count += 1
        time.sleep(0.5)
        sql_query = "INSERT INTO getdummydata  (recdate, device_id, temperature, humid, soil_moistur) VALUES(%s,%s,%s,%s,%s)"
        values_query = (now, dev_count, temp_mean,humid_mean,soilmoist_mean)
        mycursor.execute(sql_query,values_query)
        mydb.commit()
    dev_count = 0
    i += 1
    time.sleep(0.5)
    print(f"{i*10} records inserted successfully")

print("All records inserted successfully!")
