# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 23:54:54 2018

@author: Deepu
"""

import pymsql

def create_connection():

        conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql')
        return conn

db = create_connection()
cursor = db.cursor()

sql = "SELECT * FROM product_table WHERE item_group_id > '%d'" % (200067380)

try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
      # Now print fetched result
      print ("fname = %s,lname = %s,age = %d,sex = %s,income = %d" % \
             (fname, lname, age, sex, income ))
except:
   print ("Error: unable to fetch data")

# disconnect from server
db.close()
