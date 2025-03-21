import os
import json
import re
import chardet

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result['encoding']

def compare(path1, path2):
    f1 = open(path1, 'r', encoding='utf-8')
    f2 = open(path1, 'r', encoding='utf-8')
    #LLM can hallucinate params that don't exist, this keeps track of which ones do
    params = set()
    #Cache default so I don't have to read the whole file every time
    if not os.path.exists(f"./Analysis_Results/def_pwquality.conf.json"):
        d = {}
        with open(f"./Analysis_Results/def_pwquality.conf", 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):  # Skip comments and empty lines
                    continue
                match = re.match(r'^(\S+)\s*=\s*(.*)$', line)
                if match:
                    key, value = match.groups()
                    d[key] = value
            d['local_users_only'] = 0
            d['enforce_for_root'] = 0
        with open(f"./Analysis_Results/def_pwquality.conf.json", 'w') as fp:
            json.dump(d, fp)
    d1 = json.load(open(f"./Analysis_Results/def_pwquality.conf.json", "r", encoding="utf-8"))
    d2 = json.load(open(f"./Analysis_Results/def_pwquality.conf.json", "r", encoding="utf-8"))
    params = set(d1.keys())
    with open(path1, 'r', encoding=detect_encoding(path1)) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('local_users_only'):
                d1['local_users_only'] = 1
            if line.startswith('enforce_for_root'):
                d1['enforce_for_root'] = 1
            match = re.match(r'^(\S+)\s*=\s*(.*)$', line)
            if match:
                key, value = match.groups()
                d1[key] = value
    with open(path2, 'r', encoding=detect_encoding(path2)) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('local_users_only'):
                d2['local_users_only'] = 1
            if line.startswith('enforce_for_root'):
                d2['enforce_for_root'] = 1
            match = re.match(r'^(\S+)\s*=\s*(.*)$', line)
            if match:
                key, value = match.groups()
                d2[key] = value
    s = 0
    hal = 0
    cnt = 0
    #hallucinations found with the same value in both
    jhals = 0
    # print(params)
    # print("----------")
    # print(d1)
    # print("----------")
    # print(d2)
    for p in list(d1.keys()):
        if p in d1 and p in d2:
            if d1[p] == d2[p]:
                s += 1
                if p not in params:
                    jhals += 1
        if p not in params:
            hal += 1
        cnt+=1
    return [hal, s, s/cnt, (s-jhals)/(cnt-hal)]
    #[num hallucinations, num same, percentage same, percentage same excluding hallucinations]