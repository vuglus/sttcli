
class Summarizer:
    """Базовый класс для суммаризации текста."""
    def __init__(self, config):
        self.config = config
        self.all_instructions = {}
        self.all_instructions.update(config["instructions"])
        self.all_instructions.update(config["service_instructions"])

    def summarize(self, text, instruction_type, context="", manual_prompt=None):
        chunks = self.chunk_text(text)
        partial_summaries = []

        if manual_prompt.strip() != '':
            instruction = manual_prompt
        else:
            instruction = self.all_instructions.get(instruction_type)

        if not instruction or not instruction.strip():
            raise ValueError(f"Instruction '{instruction_type}' is empty or contains only whitespace")

        for idx, chunk in enumerate(chunks, start=1):
            print(f"Summarizing chunk {idx}/{len(chunks)}...")
            partial = self.chunk_summarize(chunk, instruction, context)

            if instruction_type == "normalize":
                partial_summaries.append(partial)
            else:
                partial_summaries.append(f"### Chunk {idx}\n{partial}")

        if instruction_type == "normalize":
            combined_text = "".join(partial_summaries)
        else:
            combined_text = "\n\n".join(partial_summaries)
        if len(chunks) > 1 and instruction_type != "normalize":
            print("Generating final summary...")
            join_instruction = self.all_instructions.get("join")
            if not join_instruction:
                raise ValueError("В конфиге нет служебной инструкции 'join'")

            return self.chunk_summarize(combined_text, join_instruction)
        return combined_text

    def chunk_summarize(self, text, instruction, context=""):
        raise NotImplementedError("Must implement chunk_summarize in subclass")

    @staticmethod
    def chunk_text(text, max_chars=5_000):
        chunks = []
        current_chunk = []
        current_len = 0

        for line in text.splitlines(keepends=True):
            line_len = len(line)

            if current_len + line_len > max_chars and current_chunk:
                chunks.append(''.join(current_chunk))
                current_chunk = []
                current_len = 0

            current_chunk.append(line)
            current_len += line_len

        if current_chunk:
            chunks.append(''.join(current_chunk))

        return chunks