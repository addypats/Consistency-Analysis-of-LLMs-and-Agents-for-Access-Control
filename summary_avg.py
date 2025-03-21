import os
import re
import json

def parse_four_numbers(line):
    """
    Given a line in the format (0.0, 16.9, 0.8842, 0.8842),
    extract and return the four float values as a list.
    """
    pattern = r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?"
    matches = re.findall(pattern, line)
    if len(matches) != 4:
        raise ValueError(f"Could not parse exactly 4 numbers from line: {line}")
    return [float(m) for m in matches]

def average_numbers_in_directory(dir_path):
    """
    Looks inside the given directory (e.g., Analysis_Results/dir1).
    Finds all subdirectories named 0, 1, 2, ... up to n (no hardcoded limit).
    In each subdirectory, it reads all .txt files containing four numbers in parentheses,
    accumulates them, and returns the average of the four numbers.
    
    Returns:
        list of floats (the 4-number average) or None if no valid files found.
    """
    total = [0.0, 0.0, 0.0, 0.0]
    count = 0
    
    # Go through subdirectories named 0, 1, 2, ...
    for sub in os.listdir(dir_path):
        if sub.isdigit():
            subdir_path = os.path.join(dir_path, sub)
            if os.path.isdir(subdir_path):
                # Find .txt files in this numeric subdirectory
                for filename in os.listdir(subdir_path):
                    # if filename == "self_summary.txt":
                    if filename == "correctness_summary.txt":
                        file_path = os.path.join(subdir_path, filename)
                        try:
                            with open(file_path, 'r') as f:
                                line = f.read().strip()
                            nums = parse_four_numbers(line)
                            for i in range(4):
                                total[i] += nums[i]
                            count += 1
                        except Exception as e:
                            print(f"Skipping file {file_path}: {e}")

    if count == 0:
        return None

    return [t / count for t in total]

def without_doc():
    # Always look for Analysis_Results in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    top_dir = os.path.join(script_dir, "Analysis_Results")

    if not os.path.isdir(top_dir):
        print(f"Folder 'Analysis_Results' not found at {top_dir}.")
        return

    print("################################################")
    print(top_dir)
    print("################################################")

    # Loop over subdirectories named dir1, dir2, etc.
    for d in os.listdir(top_dir):

        dir_path = os.path.join(top_dir, d)
        if os.path.isdir(dir_path):
            averages = average_numbers_in_directory(dir_path)
            if averages is not None:
                # Write to avg.json as JSON
                output_file = os.path.join(dir_path, "avg_correctness_without_docs.json")
                with open(output_file, 'w') as out:
                    json.dump({"average": averages}, out, indent=2)
                print(f"Averages written to {output_file}: {averages}")
            else:
                print(f"No valid .txt files found in {dir_path}")

def with_doc():
    # Always look for Analysis_Results in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    top_dir = os.path.join(script_dir, "Analysis_Results")

    if not os.path.isdir(top_dir):
        print(f"Folder 'Analysis_Results' not found at {top_dir}.")
        return
    
    # Loop over subdirectories named dir1, dir2, etc.
    for d in os.listdir(top_dir):
        
        dir_path = os.path.join(top_dir, d)
        if os.path.isdir(dir_path):
            # Build the with_docs directory inside the current dir (e.g., Analysis_Results/dir1/with_docs)
            top_with_docs_dir = os.path.join(dir_path, "with_docs")

            if not os.path.isdir(top_with_docs_dir):
                print(f"Folder 'with_docs' not found at {top_with_docs_dir}.")
                continue  # Skip this directory if with_docs is missing

            print("******************************************")
            print(top_with_docs_dir)
            print("******************************************")


            averages = average_numbers_in_directory(top_with_docs_dir)
            if averages is not None:
                # Write to avg.json as JSON
                output_file = os.path.join(top_with_docs_dir, "avg_correctness_with_docs.json")
                with open(output_file, 'w') as out:
                    json.dump({"average": averages}, out, indent=2)
                print(f"Averages written to {output_file}: {averages}")
            else:
                print(f"No valid .txt files found in {top_with_docs_dir}")

def main():
    without_doc()
    with_doc()
    

if __name__ == "__main__":
    main()
