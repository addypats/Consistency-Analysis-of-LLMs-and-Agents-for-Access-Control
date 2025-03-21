import json
from jsonstream import load
from Response_Generation.generate_response import *
from file_compare import *
import os
from dotenv import load_dotenv
load_dotenv()
#Keeps track of whether we're generating or analyzing, maybe make interactive later.

# mode = 'generate'
mode = 'analyze'

overwrite = False
dirs = [name for name in os.listdir("./Responses") if os.path.isdir(os.path.join("./Responses", name))]
pfiles = [name for name in os.listdir("./Prompts")]

#Keeps track of all policies
#Generate some number of responses for each LLM and save as JSON files
if mode == 'generate':
    #make more interactive later on, for now just pull all the prompts from prompt.json and generate responses
    
    #In the future check it with a file that keeps track of prompts we've already generated responses for
        #I guess multiple files is a little easier. Will revise
    policies = []
    
    #How many iterations we generate for
    
    iterations = 5 
    cnt = 0
    #Regular stored under /Responses/LLM/num/
    #In context learning stored under /Responses/LLM/with_docs/num
    for fl in pfiles:
        print(f"./Prompts/{fl}")
        # p = json.loads(f"./Prompts/{fl}")
        p = json.load(open(f"./Prompts/{fl}", "r", encoding="utf-8"))
        # p = str(open(f"./Prompts/{fl}", 'r').read())
        # print(p)
        policies.append(p)
        # prompt = "Generate me a /etc/security/pwquality.conf file with the following password policy rules (reply with just the contents of the file):\n" + p
        prompt = "Using the documentation at: https://man.archlinux.org/man/pwquality.conf.5.en,\nGenerate me a /etc/security/pwquality.conf file with the following password policy rules (reply with just the contents of the file):\n" + p
        for d in dirs:
            
            #idk what to call the folders, so for now I'll just number them and store the prompt in a txt file inside
            #cnt refers to which policy. It'll be 0 for prompt_0, 1 for prompt_1, etc.
            #Next time I should store the path in some kind of variable so I don't have to keep writing it/modify many lines
            if not os.path.exists(f"./Responses/{d}/with_docs/{cnt}/prompt.txt"):
                os.makedirs(os.path.dirname(f"./Responses/{d}/with_docs/{cnt}/"), exist_ok=True)
                f = open(f"./Responses/{d}/with_docs/{cnt}/prompt.txt", "w")
                f.write(prompt)
                f.close()
            if overwrite:
                f = open(f"./Responses/{d}/with_docs/{cnt}/prompt.txt", "w")
                f.write(prompt)
                f.close()
                
        #Generate and save
        #Using files instead of storing it all in memory will help with fault tolerance
        
        for i in range(iterations):
            for d in dirs:
                
                #Fault tolerance
                
                if os.path.exists(f"./Responses/{d}/with_docs/{cnt}/pwquality{i}.conf") and overwrite == False:
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
                    
                    
                f = open(f"./Responses/{d}/with_docs/{cnt}/pwquality{i}.conf", "w", encoding="utf-8")
                f.write(resp)
                f.close()
        cnt+=1

#Lets focus on self for now.
#Compare every combination of files and write the results.
#LLM/num/self, LLM/num/cross
#Have a results.txt and a summary.txt
#Results will post the raw results of every comparison
#Comparison will post an average of everything, this is more important
elif mode == 'analyze':
    # print(compare("./Responses/GPT o3-Mini/0/pwquality0.conf", "./Responses/GPT o3-Mini/0/pwquality1.conf"))
    cnt = 0
    for fl in pfiles:
        for d in dirs:
            if not os.path.exists(f"./Analysis_Results/{d}/with_docs/{cnt}/prompt.txt"):
                os.makedirs(os.path.dirname(f"./Analysis_Results/{d}/with_docs/{cnt}/"), exist_ok=True)
                f = open(f"./Analysis_Results/{d}/with_docs/{cnt}/prompt.txt", "w")
                f.write(json.load(open(f"./Prompts/{fl}", "r", encoding="utf-8")))
                f.close()
            if overwrite:
                f = open(f"./Analysis_Results/{d}/with_docs/{cnt}/prompt.txt", "w")
                f.write(json.load(open(f"./Prompts/{fl}", "r", encoding="utf-8")))
                f.close()
            files = [name for name in os.listdir(f"./Responses/{d}/with_docs/{cnt}") if name != "prompt.txt"]
            #Self consistency
            if not os.path.exists(f"./Analysis_Results/{d}/with_docs/{cnt}/self_summary.txt") or overwrite:
                f = open(f"./Analysis_Results/{d}/with_docs/{cnt}/self_results.txt", 'w')
                f.close()
                f = open(f"./Analysis_Results/{d}/with_docs/{cnt}/self_results.txt", 'a')
                fin = [0, 0, 0, 0]
                for i in range(len(files)):
                    for j in range(i + 1, len(files)):
                        temp = compare(f"./Responses/{d}/with_docs/{cnt}/pwquality{i}.conf", f"./Responses/{d}/with_docs/{cnt}/pwquality{j}.conf")
                        f.write(f"./Responses/{d}/with_docs/{cnt}/pwquality{i}.conf")
                        f.write(f"./Responses/{d}/with_docs/{cnt}/pwquality{j}.conf")
                        print(fin, file=f)
                        # f.write(fin)
                        f.write("---------------------------------------")
                        f.write("\n")
                        fin[0] += temp[0]
                        fin[1] += temp[1]
                        fin[2] += temp[2]
                        fin[3] += temp[3]
                f.close()
                f = open(f"./Analysis_Results/{d}/with_docs/{cnt}/self_summary.txt", 'w')
                sm = len(files)*((len(files)-1)/2)
                print([fin[0]/(2*sm), fin[1]/sm, fin[2]/sm, fin[3]/sm], file=f)
                f.close()
            
            #Cross consistency
            #Will take a decent bit longer
            if not os.path.exists(f"./Analysis_Results/{d}/with_docs/{cnt}/cross_summary.txt") or overwrite:
                f = open(f"./Analysis_Results/{d}/with_docs/{cnt}/cross_results.txt", 'w')
                f.close()
                f = open(f"./Analysis_Results/{d}/with_docs/{cnt}/cross_results.txt", 'a')
                fin = [0, 0, 0, 0]
                
                for i in range(len(files)):
                    for nd in dirs:
                        for j in range(len(files)):
                            temp = compare(f"./Responses/{d}/with_docs/{cnt}/pwquality{i}.conf", f"./Responses/{nd}/with_docs/{cnt}/pwquality{j}.conf")
                            f.write(f"./Responses/{d}/with_docs/{cnt}/pwquality{i}.conf")
                            f.write(f"./Responses/{nd}/with_docs/{cnt}/pwquality{j}.conf")
                            print(fin, file=f)
                            # f.write(fin)
                            f.write("---------------------------------------")
                            f.write("\n")
                            fin[0] += temp[0]
                            fin[1] += temp[1]
                            fin[2] += temp[2]
                            fin[3] += temp[3]
                f.close()
                f = open(f"./Analysis_Results/{d}/with_docs/{cnt}/cross_summary.txt", 'w')
                sm = len(files)*len(dirs)*len(files)
                print([fin[0]/(2*sm), fin[1]/sm, fin[2]/sm, fin[3]/sm], file=f)
                f.close()

            #Correctness
            if not os.path.exists(f"./Analysis_Results/{d}/{cnt}/correctness_summary.txt") or overwrite:
                f = open(f"./Analysis_Results/{d}/{cnt}/correctness_results.txt", 'w')
                f.close()
                f = open(f"./Analysis_Results/{d}/{cnt}/correctness_results.txt", 'a')
                fin = [0, 0, 0, 0]
                for i in range(len(files)):
                    temp = compare(f"./Supervision_Benchmarks/pwquality_{cnt}.conf", f"./Responses/{d}/{cnt}/pwquality{i}.conf")
                    f.write(f"./Supervision_Benchmarks/pwquality_{cnt}.conf")
                    f.write(f"./Responses/{d}/{cnt}/pwquality{i}.conf")
                    print(fin, file=f)
                    # f.write(fin)
                    f.write("---------------------------------------")
                    f.write("\n")
                    fin[0] += temp[0]
                    fin[1] += temp[1]
                    fin[2] += temp[2]
                    fin[3] += temp[3]
                f.close()
                f = open(f"./Analysis_Results/{d}/{cnt}/correctness_summary.txt", 'w')
                sm = len(files)
                print([fin[0]/sm, fin[1]/sm, fin[2]/sm, fin[3]/sm], file=f)
                f.close()


        cnt += 1
            
