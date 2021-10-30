from flask import jsonify
import json
import xmltodict

def response(body: dict, status_code: int):
    response = jsonify(body)
    response.status_code = status_code
    return response

def read_XML(nameFile):
    with open("./shared/"+nameFile, "r") as file:
        obj = xmltodict.parse(file.read())
        return(json.dumps(obj))

def readJson(nameFile):
    with open("./shared/"+nameFile, "r") as file:
        return json.load(file)

def writeJson(nameFile, data):
    with open("./shared/"+nameFile, "w") as file:
        json.dump(data, file)
        file.close()
        return True