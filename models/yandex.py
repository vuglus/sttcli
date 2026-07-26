from .base import Summarizer
import openai

class YandexGPTSummarizer(Summarizer):
    def __init__(self, config):
        super().__init__(config)
        self.model = self.config['yandex']['model']
        self.max_output = self.config['yandex']['max_output']
        self.api_key = self.config['yacloud']['api_key']
        self.folder_id = self.config['yacloud']['folder_id']
        self.temperature = self.config['yandex']['temperature']

    """Суммаризация через YandexGPT."""
    def chunk_summarize(self, text, instruction, context=""):
        if not text or not text.strip():
            raise ValueError("Input text is empty or contains only whitespace")

        if not instruction or not instruction.strip():
            raise ValueError("Instruction is empty or contains only whitespace")

        if context:
            instruction += "\n\n" + context

        client = openai.OpenAI(
            api_key=self.api_key,
            base_url="https://rest-assistant.api.cloud.yandex.net/v1",
            project=self.folder_id
        )

        response = client.responses.create(
            model=f"gpt://{self.folder_id}/{self.model}",
            temperature=self.temperature,
            instructions=instruction,
            input=text,
            max_output_tokens=self.max_output
        )

        if response.error:
            raise RuntimeError(f"YandexGPT error: {response.error}")
        if not response.output_text:
            raise RuntimeError("Empty YandexGPT response (probably input token overflow)")

        return response.output_text