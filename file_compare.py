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

    #Keeps track of the number of parameters in the second file
    # lns = 0

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
            # lns += 1
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
    # for p in list(d1.keys()):
    for p in (set(d1)|set(d2)):
        if p in d1 and p in d2:
            if d1[p] == d2[p]:
                s += 1
                if p not in params:
                    jhals += 1
        if p not in params:
            hal += 1
        cnt+=1
    # n = 0
    # #Rushjob, but it works
    # for p in list(d2.keys()):
    #     if p not in d1 and p not in params:
            # n += 1
    #Fix the final param
    return [hal, s, s/cnt, (s-jhals)/(cnt-hal)]
    #[num hallucinations, num same, percentage same, percentage same excluding hallucinations]

def incompleteness(golden_file, candidate_file):
    """
    Checks whether every parameter present in golden_file exists in candidate_file.
    """
    golden_map = _extract_policy_map_app(golden_file)
    candidate_map = _extract_policy_map_app(candidate_file)

    required = set(golden_map.keys())
    provided = set(candidate_map.keys())
    missing = sorted(required - provided)

    total_required = len(required)
    present_parameters = total_required - len(missing)
    incompleteness_score = (len(missing) / total_required) if total_required else 0.0

    return {
        "missing_parameters": missing,
        "total_required": total_required,
        "present_parameters": present_parameters,
        "incompleteness_score": incompleteness_score,
    }

def hallucination(candidate_file, auto_comment=False, output_file=None):
    """
    Finds parameters in candidate_file that are not valid pwquality directives.
    If auto_comment=True, comments out hallucinated lines with '# '.
    """
    default_map = _load_default_policy_map_app()
    valid_params = set(default_map.keys())
    entries = _extract_policy_entries_app(candidate_file)

    hallucinated_entries = []
    for line_number, key, _, raw_line in entries:
        if key not in valid_params:
            hallucinated_entries.append({
                "line": line_number,
                "parameter": key,
                "raw_line": raw_line,
            })

    total_directives = len(entries)
    hallucination_count = len(hallucinated_entries)
    hallucination_rate = (hallucination_count / total_directives) if total_directives else 0.0

    rewritten_file = None
    if auto_comment and hallucinated_entries:
        with open(candidate_file, 'r', encoding=detect_encoding(candidate_file)) as f:
            original_lines = f.readlines()

        hallucinated_line_numbers = {entry["line"] for entry in hallucinated_entries}
        updated_lines = []
        for index, line in enumerate(original_lines, start=1):
            if index in hallucinated_line_numbers and line.strip() and not line.lstrip().startswith('#'):
                updated_lines.append('# ' + line)
            else:
                updated_lines.append(line)

        target_file = output_file if output_file else candidate_file
        with open(target_file, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        rewritten_file = target_file

    return {
        "hallucinated_parameters": sorted({entry["parameter"] for entry in hallucinated_entries}),
        "hallucinated_entries": hallucinated_entries,
        "total_directives": total_directives,
        "hallucination_count": hallucination_count,
        "hallucination_rate": hallucination_rate,
        "rewritten_file": rewritten_file,
    }

def _extract_policy_map_app(file_path):
    policy = {}
    for _, key, value, _ in _extract_policy_entries_app(file_path):
        policy[key] = value
    return policy

def _extract_policy_entries_app(file_path):
    entries = []
    with open(file_path, 'r', encoding=detect_encoding(file_path)) as f:
        for index, raw_line in enumerate(f, start=1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if stripped.startswith('local_users_only'):
                entries.append((index, 'local_users_only', '1', raw_line.rstrip('\n')))
                continue
            if stripped.startswith('enforce_for_root'):
                entries.append((index, 'enforce_for_root', '1', raw_line.rstrip('\n')))
                continue
            match = re.match(r'^(\S+)\s*=\s*(.*)$', stripped)
            if match:
                key, value = match.groups()
                entries.append((index, key, value, raw_line.rstrip('\n')))
    return entries

def _load_default_policy_map_app(default_json_path="./Analysis_Results/def_pwquality.conf.json",
                                 default_conf_path="./Analysis_Results/def_pwquality.conf"):
    if not os.path.exists(default_json_path):
        defaults = {}
        with open(default_conf_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                match = re.match(r'^(\S+)\s*=\s*(.*)$', line)
                if match:
                    key, value = match.groups()
                    defaults[key] = value
        defaults['local_users_only'] = 0
        defaults['enforce_for_root'] = 0
        with open(default_json_path, 'w', encoding='utf-8') as fp:
            json.dump(defaults, fp)
    return json.load(open(default_json_path, "r", encoding="utf-8"))
