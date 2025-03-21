import os
import json
import re
def compare(path1, path2):
    f1 = open(path1, 'r', encoding='utf-8')
    f2 = open(path1, 'r', encoding='utf-8')
    #LLM can hallucinate params that don't exist, this keeps track of which ones do
    params = set()
    #Cache default so I don't have to read the whole file every time
    if not os.path.exists(f"./Comparison_Results/def_pwquality.conf.json"):
        d = {}
        with open(f"./Comparison_Results/def_pwquality.conf", 'r', encoding='utf-8') as f:
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
        with open(f"./Comparison_Results/def_pwquality.conf.json", 'w') as fp:
            json.dump(d, fp)
    d1 = json.load(open(f"./Comparison_Results/def_pwquality.conf.json", "r", encoding="utf-8"))
    d2 = json.load(open(f"./Comparison_Results/def_pwquality.conf.json", "r", encoding="utf-8"))
    params = set(d1.keys())
    with open(path1, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = re.match(r'^(\S+)\s*=\s*(.*)$', line)
            if match:
                key, value = match.groups()
                d1[key] = value
    with open(path2, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('local_users_only'):
                d['local_users_only'] = 1
            if line.startswith('enforce_for_root'):
                d['enforce_for_root'] = 1
            if not line or line.startswith('#'):
                continue
            match = re.match(r'^(\S+)\s*=\s*(.*)$', line)
            if match:
                key, value = match.groups()
                d2[key] = value
    s = 0
    hal = 0
    cnt = 0
    for p in list(d1.keys()):
        if d1[p] == d2[p]:
            s += 1
        if p not in params:
            hal += 1
        cnt+=1
    return [hal, s, s/cnt, (s-hal)/(cnt-hal)]
    #[num hallucinations, num same, percentage same, percentage same excluding hallucinations]