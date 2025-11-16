import openai

def summarize(config, text):
    client = openai.OpenAI(
        api_key=config["yacloud"]["api_key"],
        base_url="https://rest-assistant.api.cloud.yandex.net/v1",
        project=config["yacloud"]["folder_id"]
    )
    response = client.responses.create(
        model=f"gpt://{config['yacloud']['folder_id']}/yandexgpt/rc",
        temperature=0.3,
        instructions=(
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
    return response.output_text
