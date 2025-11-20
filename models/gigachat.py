from .base import Summarizer
from gigachat import GigaChat

class GigaChatSummarizer(Summarizer):
    """Суммаризация через GigaChat с использованием официального SDK."""
    def __init__(self, config):
        super().__init__(config)
        self.client = GigaChat(
            credentials=self.config["giga"]["api_key"],
            model=self.config["giga"]["model"],
            verify_ssl_certs=False
        )

    def chunk_summarize(self, text, instruction, context=""):
        if context:
            instruction += context

        # Формируем запрос
        response = self.client.chat(f"{instruction}\n\n{text}")

        # Берём текст ответа из первого выбора
        try:
            output_text = response.choices[0].message.content
        except (AttributeError, IndexError):
            raise RuntimeError("Empty GigaChat response")

        return output_text
