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
        instructions="Ты помощник, делающий краткое саммари текста.",
        input=text,
        max_output_tokens=500
    )
    return response.output_text
