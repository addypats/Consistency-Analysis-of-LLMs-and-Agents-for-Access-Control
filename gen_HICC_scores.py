from file_compare import *
from collections import defaultdict
import json


dirs = [name for name in os.listdir("./Responses") if os.path.isdir(os.path.join("./Responses", name))]
results = defaultdict(list)
# docs = "/"
docs = "/with_docs/"
for d in dirs:
    for i in range(7):
        files = [name for name in os.listdir(f"./Responses/{d}{docs}{i}") if name != "prompt.txt"]
        results[d].append([])
        for j in files:
            f = f"./Responses/{d}{docs}{i}/{j}"
            Hal = 1 - hallucination(f)["hallucination_rate"]
            #Flipped so bigger -> better
            Inc = 1 - incompleteness(f"./Supervision_Benchmarks/pwquality_{i}.conf",f)["incompleteness_score"]
            Con = 0
            for l in files:
                if j == l:
                    continue
                arr = compare(f"./Responses/{d}{docs}{i}/{l}",f)
                Con += arr[2]
            Con = Con / (len(files)-1)

            arr = compare(f"./Supervision_Benchmarks/pwquality_{i}.conf",f)
            Cor = arr[3]
            # d[LLM][Prompt][File]
            #File array structure: [File Path, H, I, C, C, Soundness (1 - all 4 weighted equally)]
            results[d][i].append([f, Hal, Inc, Con, Cor, 1-((Hal+Inc+Con+Cor)/4)])
# with open('zero_shot.json', 'w') as jsf:
with open('in_context_learning.json', 'w') as jsf:
    json.dump(results, jsf, indent=4)
print(results)