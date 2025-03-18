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


# R = Result()
# RA = Result_Answers()
# LMP = Llm_Model_Process()
# SL = Spider_List()
API = api()
# SPC = Spider_Charts()
# CVL = Cross_Valid_List()


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
    
    
    # Template for the actual Flask code

@app.route('/upload_file_modified', methods=['GET', 'POST'])
def upload_file_modified():

    # initializations
    
    if request.method == 'POST':

        # get parameters from user
        file = request.files['file']
        # counter = request.form.get('counter')
        # topic = request.form.get('topic')
        
        # read the file and get questions
        lines = file.stream.readlines()
        policy_descriptions = [line.decode('utf-8').strip() for line in lines]

        policy_descriptions = API.process_policy_description(policy_descriptions, counter)

        print("POLICY DESCRIPTIONS\n")
        print(policy_descriptions)
        
        # data_dict_answers = API.process_answers(policy_descriptions, counter)  Redundant in this case

       
        
        # no_of_questions = len(questions_list)   Not sure if we need this (most probably not - just keeping it here for reference (for what idk for now - will remove it later))

        
        
        # return render_template('results.html', no_of_questions=no_of_questions, policy_descriptions=policy_descriptions)
        return None

            
    else:
        return render_template('upload_file_modified.html') 

    
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8000, debug = True)