
import sys, os, shutil
import re
import json
import glob

def forge_to_grading(from_file, to_file, code_file):
    with open(from_file, "r") as f:
        from_contents = f.read()

    to_contents = re.sub("#lang\s+forge/core", f"#lang forge/testme/core \"{code_file}\"", from_contents)
    to_contents = re.sub("#lang\s+forge", f"#lang forge/testme \"{code_file}\"", to_contents)

    with open(to_file, "w") as f:
        f.write(to_contents)


def run_pair(code_file, test_file):
    shutil.copyfile(code_file, "temp/code.rkt")
    forge_to_grading(test_file, "temp/test.rkt", "code.rkt")
    os.system("racket temp/test.rkt > temp/result")

    with open("temp/result", "r") as f:
        result = list(filter(lambda line: line != "", f.read().split("\n")))[-1]

    return result


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 run_autograder.py <submission> <lfs> <assignment data>")
        exit(1)

    _, submission_folder, lfs_folder, assignment_data_file = sys.argv

    with open(assignment_data_file, "r") as f:
        assignment_data = json.load(f)
    assignment_name, year, sub_assignments = \
        assignment_data["assignment_name"],  \
        assignment_data["year"],             \
        assignment_data["sub_assignments"]

    os.mkdir("temp")

    results = []

    for sub_assignment in sub_assignments:
        name, file = sub_assignment["name"], sub_assignment["file"]
        code, tests = sub_assignment["code"], sub_assignment["tests"]

        sub_assignment_dir = f"{lfs_folder}/{year}/{assignment_name}/{name}"

        code_file = f"{submission_folder}/{file}"
        test_dir = f"{sub_assignment_dir}/tests"
        wheat_dir = f"{sub_assignment_dir}/wheats"
        chaff_dir = f"{sub_assignment_dir}/chaffs"

        test_results = [run_pair(code_file, test_file) for test_file in glob.glob(f"{test_dir}/*")] if code else []
        wheat_results = []
        if tests:
            for wheat_file in glob.glob(f"{wheat_dir}/*"):
                wheat_results.append({
                    "name": os.path.basename(wheat_file),
                    "results": run_pair(wheat_file, code_file),
                })
            for chaff_file in glob.glob(f"{chaff_dir}/*"):
                chaff_results.append({
                    "name": os.path.basename(chaff_file),
                    "results": run_pair(chaff_file, code_file),
                })

        test_results = list(map(json.loads, test_results))
        wheat_results = list(map(json.loads, wheat_results))
        chaff_results = list(map(json.loads, chaff_results))

        results.append({
                "name": name,
                "functionality": test_results,
                "wheats": wheat_results,
                "chaffs": chaff_results
            })


    shutil.rmtree("temp")

    print(json.dumps(results))
