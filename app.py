import json
from jsonstream import load
from generate_response import *
#make more interactive later on, for now just pull all the prompts from prompt.json and generate responses
# GR = Gen_Resp()
f = open("prompts.json", "r")
stream = load(f)
policies = []
for p in stream:
    policies.append(p)
    