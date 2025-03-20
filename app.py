import json
from jsonstream import load
from Response_Generation.generate_response import *
import os
from dotenv import load_dotenv
load_dotenv()
#Keeps track of whether we're generating or analyzing, maybe make interactive later.

mode = 'generate'

# mode = 'analyze'

#Keeps track of all policies
#Generate some number of responses for each LLM and save as JSON files
if mode == 'generate':
    #make more interactive later on, for now just pull all the prompts from prompt.json and generate responses
    
    #In the future check it with a file that keeps track of prompts we've already generated responses for
        #I guess multiple files is a little easier. Will revise
    policies = []
    
    #How many iterations we generate for
    
    iterations = 5 
    overwrite = False
    cnt = 0
    dirs = [name for name in os.listdir("./Responses") if os.path.isdir(os.path.join("./Responses", name))]
    pfiles = [name for name in os.listdir("./Prompts")]
    #Originally I'd store every prompt in one file. This would loop over everything. No need for an outer loop
    #Will revise to read multiple files instead of using JsonStream
    for fl in pfiles:
        print(f"./Prompts/{fl}")
        # p = json.loads(f"./Prompts/{fl}")
        p = json.load(open(f"./Prompts/{fl}", "r", encoding="utf-8"))
        # p = str(open(f"./Prompts/{fl}", 'r').read())
        # print(p)
        policies.append(p)
        prompt = "Generate me a /etc/security/pwquality.conf file with the following password policy rules (reply with just the contents of the file):\n" + p
        for d in dirs:
            
            #idk what to call the folders, so for now I'll just number them and store the prompt in a txt file inside
            #cnt refers to which policy. It'll be 0 for prompt_0, 1 for prompt_1, etc.
            if not os.path.exists(f"./Responses/{d}/{cnt}/prompt.txt"):
                os.makedirs(os.path.dirname(f"./Responses/{d}/{cnt}/"), exist_ok=True)
                f = open(f"./Responses/{d}/{cnt}/prompt.txt", "w")
                f.write(prompt)
                
        #Generate and save
        #Using files instead of storing it all in memory will help with fault tolerance
        
        for i in range(iterations):
            for d in dirs:
                
                #Fault tolerance
                
                if os.path.exists(f"./Responses/{d}/{cnt}/pwquality{i}.conf"):
                    continue
                resp = ""
                
                #Don't have a nicer looking way of doing this rn
                
                if d == 'Bloom':
                    resp = generate_response_bloom(prompt)
                elif d == 'Cohere':
                    resp = generate_response_Cohere(prompt)
                elif d == 'DeepSeek':
                    resp = generate_response_deepseek(prompt)
                elif d == 'Gemini':
                    resp = generate_response_gemini(prompt)
                elif d == 'GPT 4o-Mini':
                    resp = generate_response_chat4om(prompt)
                elif d == 'GPT o3-Mini':
                    resp = generate_response_chato3m(prompt)
                elif d == 'Llama3':
                    resp = generate_response_Llama(prompt)
                    
                    
                f = open(f"./Responses/{d}/{cnt}/pwquality{i}.conf", "w", encoding="utf-8")
                f.write(resp)

            
        cnt+=1      
    # In case, we are not doing self, (just removed the iteration factor, rest of the code is the same)
    # Delete later if necessary

    #Unnecessary for cross comparison, we'll just use the already generated responses
    #If we end up doing validation will uncomment later
    
# if mode == 'generate':
    
    
#     #make more interactive later on, for now just pull all the prompts from prompt.json and generate responses
    
#     #In the future check it with a file that keeps track of prompts we've already generated responses for
    
#     policies = []
#     f = open("prompts.json", "r")
#     stream = load(f)
    
    
#     #How many iterations we generate for
#     iterations = 5          
#     overwrite = False
#     cnt = 0
#     dirs = [name for name in os.listdir("./Responses") if os.path.isdir(os.path.join("./Responses", name))]
#     for p in stream:
#         policies.append(p)
#         prompt = "Generate me a /etc/security/pwquality.conf file with the following password policy rules (reply with just the file):\n" + p
#         for d in dirs:
            
#             #idk what to call the folders, so for now I'll just number them and store the prompt in a txt file inside
            
#             if not os.path.exists(f"./Responses/{d}/{cnt}/prompt.txt"):
#                 os.makedirs(os.path.dirname(f"./Responses/{d}/{cnt}/"), exist_ok=True)
#                 f = open(f"./Responses/{d}/{cnt}/prompt.txt", "w")
#                 f.write(prompt)
                
#         #Generate and save
#         #Using files instead of storing it all in memory will help with fault tolerance
        
#         for d in dirs:
            
#             #Fault tolerance
                
#             if os.path.exists(f"./Responses/{d}/{cnt}/pwquality{i}.conf"):
#                 continue
#             resp = ""
                
#             #Don't have a nicer looking way of doing this rn
#             # Don't need a nicer way, just need it to work
                
#             if d == 'Bloom':
#                 resp = GR.generate_response_bloom(prompt)
#             elif d == 'Cohere':
#                 resp = GR.generate_response_Cohere(prompt)
                    
#                 #In progress
#                 # elif d == 'DeepSeek':
#                 #     resp = generate_response_deepseek(prompt)
                
#             elif d == 'Gemini':
#                 resp = GR.generate_response_gemini(prompt)
#             elif d == 'GPT 4o-Mini':
#                 resp = GR.generate_response_chat4om(prompt)
#             elif d == 'GPT o3-Mini':
#                 resp = GR.generate_response_chato3m(prompt)
#             elif d == 'Llama3':
#                 resp = GR.generate_response_Llama(prompt)
                    
                    
#             f = open(f"./Responses/{d}/{cnt}/pwquality{i}.conf", "w")
#             f.write(resp)

            
#         cnt+=1