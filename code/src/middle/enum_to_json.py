import json


def enum_to_json(enum):
    tuples = [(str(member.value), int(member)) for member in enum]
    result = "{\n"
    for t in tuples:
        result += '"' + t[0] + '": ' + str(t[1]) + ',\n'
    result = result[:-2]  # Removes last comma
    result += "\n}\n"
    return json.loads(result)
