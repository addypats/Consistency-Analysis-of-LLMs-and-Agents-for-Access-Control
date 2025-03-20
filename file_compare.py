import os
import re
import json
from typing import Dict, Tuple, List


class ConfFileComparator:
    def __init__(self, responses_dir: str, prompts_dir: str, iterations: int = 5):
        self.responses_dir = responses_dir
        self.prompts_dir = prompts_dir
        self.iterations = iterations
        self.defaults = self.load_defaults()

    def load_defaults(self) -> Dict[str, str]:
        """
        Load all default JSON files from the prompts directory.
        If a JSON file is invalid, it tries to parse it as text-based policies.
        """
        defaults = {}
        pfiles = [name for name in os.listdir(self.prompts_dir) if name.endswith('.json')]
        for fl in pfiles:
            try:
                with open(os.path.join(self.prompts_dir, fl), 'r', encoding="utf-8") as file:
                    try:
                        data = json.load(file)  # Try to load as regular JSON
                        if isinstance(data, dict):
                            defaults.update(data)
                        else:
                            print(f"Skipping {fl}: Not a valid dictionary structure")
                    except json.JSONDecodeError:  # If it's not a valid JSON, process as text
                        file.seek(0)
                        text_data = file.read().strip()
                        policies = text_data.split("\n")
                        for i, policy in enumerate(policies):
                            if policy:
                                defaults[f"policy_{i+1}"] = policy
            except Exception as e:
                print(f"Error loading file {fl}: {e}")
        return defaults


    @staticmethod
    def parse_conf_file(file_path: str) -> Dict[str, str]:
        """
        Parse a .conf file and extract key-value pairs.
        """
        config = {}
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):  # Skip comments and empty lines
                        continue
                    match = re.match(r'^(\S+)\s*=\s*(.*)$', line)
                    if match:
                        key, value = match.groups()
                        config[key] = value
        except UnicodeDecodeError:
            print(f"Failed to read file {file_path} with UTF-8 encoding. Trying cp1252...")
            with open(file_path, 'r', encoding='cp1252') as file:
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):  # Skip comments and empty lines
                        continue
                    match = re.match(r'^(\S+)\s*=\s*(.*)$', line)
                    if match:
                        key, value = match.groups()
                        config[key] = value
        return config

    def compare_configs(self, config1: Dict[str, str], config2: Dict[str, str]) -> Tuple[Dict[str, str], Dict[str, str]]:
        """
        Compare two configuration dictionaries using the loaded defaults.
        """
        mismatches = {}
        matches = {}
        all_keys = set(config1.keys()).union(set(config2.keys())).union(set(self.defaults.keys()))

        for key in all_keys:
            value1 = config1.get(key, self.defaults.get(key))
            value2 = config2.get(key, self.defaults.get(key))
            default_value = self.defaults.get(key)

            if value1 == value2:  # Files match
                matches[key] = value1
            elif value1 == default_value or value2 == default_value:  # Matches the default
                matches[key] = default_value
            else:  # Mismatch
                mismatches[key] = (value1, value2)

        return mismatches, matches

    def compare_files(self):
        """
        Loop through the directories and compare .conf files sequentially.
        """
        dirs = [name for name in os.listdir(self.responses_dir) if os.path.isdir(os.path.join(self.responses_dir, name))]

        for d in dirs:
            cnt = 0
            response_path = os.path.join(self.responses_dir, d)

            while os.path.exists(os.path.join(response_path, str(cnt))):
                for i in range(self.iterations - 1):
                    file1 = os.path.join(response_path, str(cnt), f"pwquality{i}.conf")
                    file2 = os.path.join(response_path, str(cnt), f"pwquality{i+1}.conf")

                    if os.path.exists(file1) and os.path.exists(file2):
                        config1 = self.parse_conf_file(file1)
                        config2 = self.parse_conf_file(file2)
                        mismatches, matches = self.compare_configs(config1, config2)
                        self.save_results(d, cnt, file1, file2, matches, mismatches)

                cnt += 1

    def save_results(self, d: str, cnt: int, file1: str, file2: str, matches: Dict[str, str], mismatches: Dict[str, Tuple[str, str]]):
        """
        Save comparison results to a JSON file mirroring the directory structure.
        """
        total_keys = len(matches) + len(mismatches)
        match_percentage = (len(matches) / total_keys) * 100 if total_keys > 0 else 0

        result = {
            "file1": file1,
            "file2": file2,
            "match_percentage": match_percentage,
            "matches": matches,
            "mismatches": {key: {"file1": v1, "file2": v2} for key, (v1, v2) in mismatches.items()}
        }

        output_dir = os.path.join("./Comparison_Results", d, str(cnt))
        os.makedirs(output_dir, exist_ok=True)
        result_file = os.path.join(output_dir, f"Comparison_{os.path.basename(file1)}_vs_{os.path.basename(file2)}.json")

        with open(result_file, 'w') as f:
            json.dump(result, f, indent=4)

        print(f"Comparison results saved to {result_file}")


if __name__ == "__main__":
    comparator = ConfFileComparator(responses_dir="./Responses", prompts_dir="./Prompts")
    comparator.compare_files()


# Just for reference - modified for reading prompts.json files and .conf files for comparison

# iterations = 5 
# overwrite = False
# cnt = 0
# dirs = [name for name in os.listdir("./Responses") if os.path.isdir(os.path.join("./Responses", name))]
# pfiles = [name for name in os.listdir("./Prompts")]
# #Originally I'd store every prompt in one file. This would loop over everything. No need for an outer loop
# #Will revise to read multiple files instead of using JsonStream
# for fl in pfiles:
#     print(f"./Prompts/{fl}")
#     # p = json.loads(f"./Prompts/{fl}")
#     p = json.load(open(f"./Prompts/{fl}", "r", encoding="utf-8"))
#     # p = str(open(f"./Prompts/{fl}", 'r').read())
#     # print(p)
    
    
    
# for d in dirs:
        
#     #idk what to call the folders, so for now I'll just number them and store the prompt in a txt file inside
#     #cnt refers to which policy. It'll be 0 for prompt_0, 1 for prompt_1, etc.
#     if not os.path.exists(f"./Responses/{d}/{cnt}"):
#         os.makedirs(os.path.dirname(f"./Responses/{d}/{cnt}/"), exist_ok=True)
#         for i in range(iterations):
#             f = open(f"./Responses/{d}/{cnt}/pwquality{i}.conf", "r")

