import openai

#
def summarize(config, text):
    chunks = chunk_text(text)

    partial_summaries = []
    for idx, chunk in enumerate(chunks, start=1):
        print(f"Summarizing chunk {idx}/{len(chunks)}...")
        partial = chunk_summarize(config, chunk, config["instructions"]["summarize"])
        partial_summaries.append(f"### Chunk {idx}\n{partial}")

    combined_text = "\n\n".join(partial_summaries)

    # финальное summary уже маленькое → точно влезает
    print("Generating final summary...")
    final = chunk_summarize(config, combined_text, config["instructions"]["join"])

    return final

#
def chunk_summarize(config, text, instruction):
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
        max_output_tokens=500
    )
    # Ловим явные ошибки
    if response.error:
        raise RuntimeError(f"YandexGPT error: {response.error}")

    # Ловим ситуацию когда токены переполнились и ответа нет
    if not response.output_text:
        raise RuntimeError("Empty YandexGPT response (probably input token overflow)")    

    return response.output_text


#
def instructions_summarize(config, text, instructions):
    client = openai.OpenAI(
        api_key=config["yacloud"]["api_key"],
        base_url="https://rest-assistant.api.cloud.yandex.net/v1",
        project=config["yacloud"]["folder_id"]
    )
    response = client.responses.create(
        model=f"gpt://{config['yacloud']['folder_id']}/yandexgpt/rc",
        temperature=0.3,
        instructions=tpl(
            "Ты помощник, делающий краткое саммари текста.\n"
            "Важно не что обсуждали, а какие решения приняли и о каких задачах договорились.\n"
            "Кто эти задачи и когда договорились сделать.\n"
            "Обрати внимание именно на изменения — т.е. начинали обсуждать А, но потом решили отказаться и сделать Б.\n"
            "Формат вывода — MD файл.\n"
            "Добавь заголовок.\n"
            "си пи эс - это CPS customer profile service, "
            "монолит - это система управления заказами и интеграционный шлюз,"
            "Список задач, если о них договорились, оформи таблицей: задача | кто делает.\n"
            "Отдельной строкой добавь название файла с краткой сутью встречи."
        ),
        input=text,
        max_output_tokens=500
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
