import openai
import json
import requests


'''
Call openai API and return the result translated to some language.
'''
def get_translation(text_to_translate, language):
    prompt = f'translate the next sentences to {language}. {text_to_translate}'
    api_key = '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'

    req_body = {
        'model': 'text-davinci-003',
        'prompt': prompt,
        'temperature': 0.2,
        'max_tokens': 2060
    }
    req_headers = {
        'Content-type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    response = requests.post('https://api.openai.com/v1/completions', headers=req_headers, json=req_body)
    return response.json()['choices'][0]['text']
