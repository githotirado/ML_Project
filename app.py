from flask import Flask, jsonify, render_template, request, redirect, url_for
import pandas as pd 
import json 
import psycopg2
import os
import numpy as np
import pickle

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################

from sqlalchemy import create_engine
## Method 1: Use local config.py
# from config import username, password, host, port, database
## Method 2: (for Heroku) Get DB configuration variables from local OS
username = os.environ.get('DBUSERNAME')
password = os.environ.get('DBPASSWORD')
host = os.environ.get('DBHOST')
port = os.environ.get('DBPORT')
database = os.environ.get('DBDATABASE')
connection_string = f'{username}:{password}@{host}:{port}/{database}'
engine = create_engine(f'postgresql://{connection_string}')


#################################################
# Flask Routes
#################################################

# HTML main page '/index' and '/'
@app.route("/index")
def index(): 
    return render_template("index.html")

@app.route("/")
def detail(): 
    return render_template("index.html")

# HTML page questionnaire
@app.route("/questionnaireHTML")
def questionnaireHTML(): 
    return render_template("questionnaire.html")

# HTML page ML analytics
@app.route("/analyticsHTML")
def analyticsHTML(): 
    return render_template("analytics.html")

# HTML page development
@app.route("/developmentHTML")
def deploymentHTML(): 
    return render_template("development.html")

# HTML page observations
@app.route("/observationsHTML")
def teamHTML(): 
    return render_template("observations.html")

# Querying the DB for questionslist questions
@app.route("/questionslistDB")
def questionslistDB():
    df_questionslist = pd.read_sql_table(table_name="questionslist", con = engine.connect(), schema ="public")
    df_questionslist_json = df_questionslist.to_dict(orient="records")
    return jsonify(df_questionslist_json)

# Querying the DB for questionnaire responses
@app.route("/questionnaireDB")
def questionnaireDB():
    df_questionnaire = pd.read_sql_table(table_name="questionnaire", con = engine.connect(), schema ="public")
    df_questionnaire_json = df_questionnaire.to_dict(orient="records")
    return jsonify(df_questionnaire_json)


# Handler for questionnaire submission
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        # print("Request.form: ", request.form)
        # print("Size: ", len(request.form))
        # for i in request.form:
        #     print("i is ", i, "and value is ", request.form[i])

        # get the response into a dataframe (1 x 91), then transpose the frame
        X_test = pd.DataFrame.from_dict(request.form, orient="index").T
        print(X_test)

        # define the possible path locations of the model file
        localparent = '/Users/henrytirado/git/usc_homework/ML_Project.githotirado'
        herokuparent = '/app'
        ## FOR DEPLOYMENT: uncomment only the correct model file location
        # modelfile = localparent + '/saved_models/IE_Predictor_model.sav'
        modelfile = herokuparent + '/saved_models/IE_Predictor_model.sav'

        # Unpickle the model file
        loaded_model = pickle.load(open(modelfile, 'rb'))

        ## This is a scoring exercise to validate that the model is responding
        r = np.array([3])
        y_test = pd.Series(r, copy=False)
        score = loaded_model.score(X_test, y_test)
        print("Score result is (1 = introvert, 2 = extrovert, 3 = ambivert): ", score)

        # Predict outcome based on user entered data
        predict_number = loaded_model.predict(X_test)[0]
        if predict_number == 1:
            ieprediction = "INTROVERT"
        elif predict_number == 2:
            ieprediction = "EXTROVERT"
        elif predict_number == 3:
            ieprediction = "AMBIVERT"
        else:
            ieprediction = "UNKNOWN"
        print("Prediction with current X_test: ", ieprediction)

        # Return the output of what we think you are
        return render_template("result.html", prediction=ieprediction)

    return render_template("questionnaire.html")


if __name__ == "__main__":
    app.run()
