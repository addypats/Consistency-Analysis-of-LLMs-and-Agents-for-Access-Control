import json
from jsonstream import load
from generate_response import *
#make more interactive later on, for now just pull all the prompts from prompt.json and generate responses
f = open("prompts.json", "r")
stream = load(f)
#Keeps track of whether we're generating or analyzing, maybe make interactive later.
mode = 'generate'
# mode = 'analyze'
#Keeps track of all policies
#In the future check it with a file that keeps track of prompts we've already generated responses for
policies = []
#Generate some number of responses for each LLM and save as JSON files

if mode == 'generate':
    #How many iterations we generate for
    iterations = 5
    for p in stream:
        policies.append(p)

    