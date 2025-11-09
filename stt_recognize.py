import requests
import time
import urllib3
import json
import os

def recognize_audio(config, file_uri: str):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    api_key = config["yacloud"]["api_key"]
    folder_id = config["yacloud"]["folder_id"]

    # имя файла в бакете (только basename)
    file_name = os.path.basename(file_uri)
    
    print(f"▶ Распознаём речь: {file_name}")

    request_data = {
        "uri": file_uri,
        "recognitionModel": {
            "model": "general:rc",
            "audioFormat": {
                "containerAudio": {
                    "containerAudioType": "MP3"
                }
            },
            "languageRestriction": {
                "restrictionType": "WHITELIST",
                "languageCode": ["ru-RU"]
            },
            "textNormalization": {
                "textNormalization": "TEXT_NORMALIZATION_ENABLED"
            }
        },
        "speakerLabeling": {
            "enable": True,
            "minSpeakers": 1,
            "maxSpeakers": 5
        }
    }

    headers = {
        "Authorization": f"Api-Key {api_key}",
        "x-folder-id": folder_id
    }

    response = requests.post(
        "https://stt.api.cloud.yandex.net/stt/v3/recognizeFileAsync",
        headers=headers,
        json=request_data,
        verify=False
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Recognition request failed: {response.status_code}\n{response.text}"
        )

    operation_data = response.json()
    operation_id = operation_data.get("id")
    if not operation_id:
        raise RuntimeError("Operation ID not found in response")

    print(f"▶ Operation ID: {operation_id}")
    print("⏳ Ожидаем завершения распознавания...")

    operation_url = f"https://operation.api.cloud.yandex.net/operations/{operation_id}"

    while True:
        op_response = requests.get(operation_url, headers=headers, verify=False)
        if op_response.status_code != 200:
            print(f"Ошибка проверки операции: {op_response.status_code}")
            time.sleep(10)
            continue

        op_data = op_response.json()
        if op_data.get("done"):
            if "error" in op_data:
                raise RuntimeError(f"Operation failed:\n{json.dumps(op_data['error'], ensure_ascii=False, indent=2)}")
            break

        print(".", end="", flush=True)
        time.sleep(10)

    # получаем результат
    speech_response = requests.get(
        f"https://stt.api.cloud.yandex.net/stt/v3/getRecognition?operation_id={operation_id}",
        headers=headers,
        verify=False,
    )
    speech_response.raise_for_status()

    # Вместо .json() парсим построчно
    lines = speech_response.text.strip().split("\n")
    texts = []
    for line in lines:
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue

        # ищем final или finalRefinement
        if "result" in data:
            res = data["result"]
            for key in ("final", "finalRefinement"):
                if key in res:
                    if "alternatives" in res[key]:
                        for alt in res[key]["alternatives"]:
                            if "text" in alt:
                                texts.append(alt["text"])

    return "\n".join(texts)
