from flask import Flask, render_template, request, redirect, url_for
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from math import pi
from Result_Modules.result_processing import Result
from Result_Modules.result_answers_processing import Result_Answers
from Processing_Modules.llm_model_process import Llm_Model_Process
from Processing_Modules.get_spider_list import Spider_List
from Response_Generation.api import api
from Result_Modules.spider_charts import Spider_Charts
from Processing_Modules.cross_valid_list import Cross_Valid_List


# Class initializations from other python files

# R = Result()
# RA = Result_Answers()
# LMP = Llm_Model_Process()
# SL = Spider_List()
# API = api()
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
        # counter = request.form.get('counter')     # Not needed for now
        # topic = request.form.get('topic')
        
        # read the file and get the descriptions
        lines = file.stream.readlines()
        questions_list = [line.decode('utf-8').strip() for line in lines]


        # print("DATA_DICT_ANSWERS")
        # print(data_dict_answers)

        # f = open("log.txt", 'w')
        # print(data_dict_questions, file=f)
        # f.write("\n\n\n\n\n\n\n\n\n\n\n\n")
        # print(data_dict_answers, file=f)
        # f.close()
        
        # no_of_questions = len(questions_list)

        
        # return render_template('results.html', questions_list=questions_list)
        return None
            
    else:
        return render_template('upload_file_modified.html') 

    
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=8000, debug = True)