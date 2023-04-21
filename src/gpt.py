import openai
import json
import requests
from typing import List, Tuple, Union

OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def get_translation(api_key: str, input: str, language: str):

    prompt = f'translate the next sentences to {language}. {input}'
 
    openai.api_key = api_key

    try:
        # res = requests.post(OPENAI_URL, headers=headers, data=req_json)
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while making the request: {e}")
        return None

    if len(res.choices) > 0:
        return res.choices[0].message.content


    return None