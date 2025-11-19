import openai

#
def summarize(config, text, instructionType, context):
    chunks = chunk_text(text)

    partial_summaries = []
    for idx, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {idx}/{len(chunks)}...")
        partial = chunk_summarize(config, chunk, config["instructions"][instructionType], context)
        partial_summaries.append(f"### Chunk {idx}\n{partial}")

    combined_text = "\n\n".join(partial_summaries)
    if len(chunks) > 1 : 
        # финальное summary уже маленькое → точно влезает
        print("Generating final summary...")
        return chunk_summarize(config, combined_text, config["instructions"]["join"])
    
    return combined_text

#
def chunk_summarize(config, text, instruction, context = ''):
    if context: 
        instruction = instruction + context
    client = openai.OpenAI(
        api_key=config["yacloud"]["api_key"],
        base_url="https://rest-assistant.api.cloud.yandex.net/v1",
        project=config["yacloud"]["folder_id"]
    )
    response = client.responses.create(
        model=f"gpt://{config['yacloud']['folder_id']}/yandexgpt/rc",
        temperature=0.3,
        instructions = instruction,
        input=text,
        max_output_tokens=config['yacloud']['max_output']
    )
    # Ловим явные ошибки
    if response.error:
        raise RuntimeError(f"YandexGPT error: {response.error}")

    # Ловим ситуацию когда токены переполнились и ответа нет
    if not response.output_text:
        raise RuntimeError("Empty YandexGPT response (probably input token overflow)")    

    return response.output_text

#
def chunk_text(text, max_chars=70_000):
    chunks = []
    start = 0
    while start < len(text):
        end = start + max_chars
        chunks.append(text[start:end])
        start = end
    return chunks
