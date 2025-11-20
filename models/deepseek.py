import requests
from .base import Summarizer

class DeepSeekSummarizer(Summarizer):

    def __init__(self, config):
        super().__init__(config)
        self.api_key = config["deepseek"]["api_key"]

    """Суммаризация через DeepSeek"""
    def chunk_summarize(self, text, instruction, context=""):
        if context:
            instruction += "\n\n" + context

        url = "https://api.deepseek.com/v1/chat/completions"

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": instruction},
                {"role": "user", "content": text}
            ],
            "temperature": 0.3
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        summary = response_data['choices'][0]['message']['content']

        return summary
