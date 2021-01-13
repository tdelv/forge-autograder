
import sys, os, shutil
import re
import json

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

    with open("temp/result.rkt", "r") as f:
        result = f.read()

    return result


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python3 run_autograder.py <code> <tests> <wheats> <chaffs>")
        exit(1)

    (_, code_file, tests, wheats, chaffs) = sys.argv

    os.mkdir("temp")

    test_results = [run_pair(code_file, test_file) for test_file in glob.glob(f"{tests}/*")]
    wheat_results = [run_pair(wheat_file, code_file) for wheat_file in glob.glob(f"{wheats}/*")]
    chaff_results = [run_pair(chaff_file, code_file) for chaff_file in glob.glob(f"{chaffs}/*")]

    shutil.rmtree("temp")

    test_results = list(map(json.loads, test_results))
    wheat_results = list(map(json.loads, test_results))
    chaff_results = list(map(json.loads, test_results))

    results = {
            "test_results": test_results,
            "wheat_results": wheat_results,
            "chaff_results": chaff_results
        }

    print(json.dumps(results))

