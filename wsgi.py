# -*- coding: utf-8 -*-
"""
Created on Thu May  3 18:03:52 2018

@author: anumula_anudeep
"""

from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import json, apiai
import pymysql

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
    #print(obj['result']['parameters'])
    catogery = str(obj['result']['parameters']['catogery'])
    brand = str(obj['result']['parameters']['Brands'])
    collection = str(obj['result']['parameters']['Collection'])
    pattern = str(obj['result']['parameters']['print_pattern'])
    
    conn = create_connection()
    cur = conn.cursor()
    
    return jsonify(obj)

def Dialogflow_connection():
    
    CLIENT_ACCESS_TOKEN = '632b51a9acaa4f0c9b92962c3df817f0'
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    airequest = ai.text_request()
    airequest.lang = 'de'  # optional, default value equal 'en'
    airequest.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    return airequest


def create_connection():

        conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql')
        return conn

if __name__ == "__main__":
    application.run()

