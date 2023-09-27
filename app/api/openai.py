import openai
import json

def api():
    with open("app/api_key.json") as file:
        data = json.load(file)
    openai.api_key  = data["api-key"]
    return openai
