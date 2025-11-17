import requests

def summarize(config, transcript):
    # API endpoint and key
    api_key = config["deepseek"]["api_key"]
    url = "https://api.deepseek.com/v1/chat/completions"

    prompt = f"""
    Создай структурированное саммари встречи на основе следующей стенограммы. Саммари должно включать следующие разделы:

    1. Проблема и Цели
    2. Рассмотренные варианты решения
    3. Ключевые обсуждения и уточнения
    4. Итоги и решения

    Стенограмма:

    {transcript}

    Формат саммари:

    ### **Саммари встречи по выбору архитектурного решения для продажи товара по цене с ценника**

    **Дата/Время:** Не указано
    **Участники:** [Спикер 1], [Спикер 2], другие коллеги

    #### **1. Проблема и Цели**

    *   **Проблема:** ...
    *   **Цели проекта:** ...
    *   **Бизнес-обоснование:** ...

    #### **2. Рассмотренные варианты решения**

    ...

    #### **3. Ключевые обсуждения и уточнения**

    ...

    #### **4. Итоги и решения**

    ...
    """

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Ты — ассистент, который анализирует стенограммы встреч и создает структурированные саммари."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(f"{response.text}")
    response_data = response.json()

    summary = response_data['choices'][0]['message']['content']
    return summary
