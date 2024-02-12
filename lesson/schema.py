import json


def load(path='') -> dict:
    with open(path) as file:
        return json.loads(file.read())
