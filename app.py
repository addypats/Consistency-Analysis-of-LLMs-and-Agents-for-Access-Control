from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from result_processing import Result
from results_answers_processing import Result_Answers
from llm_model_process import Llm_Model_Process
from get_spider_list import Spider_List
from api import api
from spider_charts import Spider_Charts
from cross_valid_list import Cross_Valid_List


R = Result()
RA = Result_Answers()
LMP = Llm_Model_Process()
SL = Spider_List()
API = api()
SPC = Spider_Charts()
CVL = Cross_Valid_List()


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer == 'yes':
            return redirect(url_for('upload_file_modified'))
        elif answer == 'no':
            return redirect(url_for('enter_question_modified'))
    else:
        return render_template('index.html')
    
    
    # Template for the actual Falsk code
 
    
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8000, debug = True)