
from .base import Summarizer
from transformers import pipeline

# Русскоязычные модели для саммари
class LocalSummarizer(Summarizer):
    def __init__(self, config):
        super().__init__(config)
        self.client = pipeline("summarization", model="IlyaGusev/rut5_base_sum_gazeta")

    """Суммаризация через Локальную модель."""
    def chunk_summarize(self, text, instruction, context=""):
        if context:
            instruction += "\n\n" + context

        max_len = min(len(text), self.config['local']['max_output'])
        summary = self.client(
            text, 
            max_length=max_len, 
            do_sample=False
        )

        return summary[0]["summary_text"]
