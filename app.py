from flask import Flask, jsonify, render_template, request, redirect, url_for
import pandas as pd 
import json 
import psycopg2
import os

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from sqlalchemy import create_engine
# Method 1: Use local config.py
from config import username, password, host, port, database
# # Method 2: (for Heroku) Get DB configuration variables from local OS
# username = os.environ.get('DBUSERNAME')
# password = os.environ.get('DBPASSWORD')
# host = os.environ.get('DBHOST')
# port = os.environ.get('DBPORT')
# database = os.environ.get('DBDATABASE')
connection_string = f'{username}:{password}@{host}:{port}/{database}'
engine = create_engine(f'postgresql://{connection_string}')


#################################################
# Flask Routes
#################################################
@app.route("/index")
def index(): 
    return render_template("index.html")

@app.route("/")
def detail(): 
    return render_template("index.html")

@app.route("/questionslistDB")
def questionslistDB():
    df_questionslist = pd.read_sql_table(table_name="questionslist", con = engine.connect(), schema ="public")
    df_questionslist_json = df_questionslist.to_dict(orient="records")
    return jsonify(df_questionslist_json)

@app.route("/questionnaireDB")
def questionnaireDB():
    df_questionnaire = pd.read_sql_table(table_name="questionnaire", con = engine.connect(), schema ="public")
    df_questionnaire_json = df_questionnaire.to_dict(orient="records")
    return jsonify(df_questionnaire_json)

@app.route("/questionnaireHTML")
def questionnaireHTML(): 
    return render_template("questionnaire.html")

@app.route("/demographics1")
def demographics1(): 
    return render_template("demographics1.html")

@app.route("/demographics2")
def demographics2(): 
    return render_template("demographics2.html")

if __name__ == "__main__":
    app.run()
