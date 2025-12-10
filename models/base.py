
class Summarizer:
    """Базовый класс для суммаризации текста."""
    def __init__(self, config):
        self.config = config

    def summarize(self, text, instruction_type, context="", manual_prompt=None):
        chunks = self.chunk_text(text)
        partial_summaries = []

        # If manual_prompt is provided, use it directly as the instruction
        if manual_prompt is not None:
            instruction = manual_prompt
        else:
            # Otherwise, look up the instruction in the config
            instruction = self.config["instructions"][instruction_type]

        for idx, chunk in enumerate(chunks, start=1):
            print(f"Summarizing chunk {idx}/{len(chunks)}...")
            partial = self.chunk_summarize(chunk, instruction, context)
            partial_summaries.append(f"### Chunk {idx}\n{partial}")

        combined_text = "\n\n".join(partial_summaries)
        if len(chunks) > 1:
            print("Generating final summary...")
            # Используем служебную инструкцию join из отдельной настройки
            join_instruction = self.config.get("service_instructions", {}).get("join")
            if not join_instruction:
                raise ValueError("В конфиге нет служебной инструкции 'join'")
            return self.chunk_summarize(combined_text, join_instruction)
        return combined_text

    def chunk_summarize(self, text, instruction, context=""):
        """Метод для переопределения в наследниках."""
        raise NotImplementedError("Must implement chunk_summarize in subclass")

    @staticmethod
    def chunk_text(text, max_chars=70_000):
        chunks = []
        start = 0
        while start < len(text):
            end = start + max_chars
            chunks.append(text[start:end])
            start = end
        return chunks