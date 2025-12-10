from .base import Summarizer
import openai

class YandexGPTSummarizer(Summarizer):
    """Суммаризация через YandexGPT."""
    def chunk_summarize(self, text, instruction, context=""):
        # Проверяем, что текст не пустой
        if not text or not text.strip():
            raise ValueError("Input text is empty or contains only whitespace")
            
        # Проверяем, что инструкция не пустая
        if not instruction or not instruction.strip():
            raise ValueError("Instruction is empty or contains only whitespace")
            
        if context:
            instruction += "\n\n" + context

        client = openai.OpenAI(
            api_key=self.config["yacloud"]["api_key"],
            base_url="https://rest-assistant.api.cloud.yandex.net/v1",
            project=self.config["yacloud"]["folder_id"]
        )

        response = client.responses.create(
            model=f"gpt://{self.config['yacloud']['folder_id']}/yandexgpt/rc",
            temperature=0.3,
            instructions=instruction,
            input=text,
            max_output_tokens=self.config['yandex']['max_output']
        )

        if response.error:
            raise RuntimeError(f"YandexGPT error: {response.error}")
        if not response.output_text:
            raise RuntimeError("Empty YandexGPT response (probably input token overflow)")

        return response.output_text