# -*- coding: utf-8 -*-
"""
Created on Thu May  3 18:03:52 2018

@author: anumula_anudeep
"""

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import json, apiai, sqlite3,os
from sqlite3 import Error

os.chdir(r"C:\Users\Deepu\Desktop\Techgig\Ecommerce-master\final")
application = Flask(__name__)
cors = CORS(application)
application.config['CORS_HEADERS'] = 'Content-Type'



@application.route('/submit/<userText>',methods=['GET'])
@cross_origin()
def get_bot_response(userText):
    
    """ Fetching user dialog from UI """
    airequest = Dialogflow_connection()
    airequest.query = str(userText)
    airesponse = airequest.getresponse()
    raw_data = airesponse.read()
    print(userText)
    # JSON default
    encoding = airesponse.info().get_content_charset('utf8')
    obj = json.loads(raw_data.decode(encoding))
    print(obj['result']['parameters'])
    catogery = str(obj['result']['parameters']['catogery']).lower()
    brand = str(obj['result']['parameters']['Brands']).lower()
    collection = str(obj['result']['parameters']['Collection']).lower()
    pattern = str(obj['result']['parameters']['print_pattern']).lower()
    print(catogery)
    print(brand)
    print(collection)
    print(pattern)
    con = create_connection()
    cur = con.cursor()

    # getting group_id
    cur.execute("SELECT distinct(item_group_id) FROM product_table WHERE lower(catogery) = ? and lower(brand) = ? and lower(collection) = ? and lower(pattern) = ?", (catogery, brand,collection,pattern ))
    grp_id = int(cur.fetchone()[0])
    print(grp_id)
    curr_user=1
    cur.execute("SELECT count(*) FROM user_search WHERE item_group_id = ? and user_id = ?", (grp_id,curr_user ))
    ser_count = cur.fetchone()[0]
    if ser_count==0:
        print("No records in ")
        cur.execute("INSERT INTO user_search (user_id, item_group_id,count) VALUES (?,?,?)",(curr_user,grp_id,1) )
    else:
        print("incrementing count")
        cur.execute("UPDATE user_search set count = count+1 WHERE item_group_id = ? and user_id = ?", (grp_id,curr_user ) )
        
    con.commit()
    
    return jsonify(obj)

def Dialogflow_connection():
    
    CLIENT_ACCESS_TOKEN = '632b51a9acaa4f0c9b92962c3df817f0'
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    airequest = ai.text_request()
    airequest.lang = 'de'  # optional, default value equal 'en'
    airequest.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    return airequest


def create_connection():

    try:
        conn = sqlite3.connect('ecomm.db')
        print("connected")
       
        return conn
    except Error as e:
        print(e)
    return None
    

if __name__ == "__main__":
    application.run()

