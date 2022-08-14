import json
def parse_result_file(path)->list:
    result = []
    with open(path, "r") as f:
        for line in f.readlines():
            if line.strip() == "":
                continue
            data = json.loads(line)
            result.append([data["host"], data["input"]])
    return result