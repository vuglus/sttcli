import requests

def summarize(config, transcript, instructionType):
    # API endpoint and key
    api_key = config["deepseek"]["api_key"]
    url = "https://api.deepseek.com/v1/chat/completions"
    instruction = config["instructions"][instructionType]

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": transcript}
        ],
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"{response.text}")
    response_data = response.json()

    summary = response_data['choices'][0]['message']['content']
    return summary
