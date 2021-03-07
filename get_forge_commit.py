import json

def main():
    with open("/autograder/source/assignment_data.json", "r") as f:
        data = json.loads(f.read())["assignment_name"]

    assert "assignment_name" in data, "assignment_data.json missing assignment"
    assignment = data["assignment_name"]

    with open("/autograder/source/forge_commits.json", "r") as f:
        data = json.loads(f.read())
    
    assert assignment in data, f"forge_commits.json missing commit for {assignment}"
    commit = data[assignment]

    print(commit)

if __name__ == "__main__":
    main()
