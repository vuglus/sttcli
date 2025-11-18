import os
import sys
import yaml
from stt_recognize import recognize_audio  # импорт из отдельного файла
from summarize.yandex import summarize  # импорт из отдельного файла
from stt_upload import upload_to_storage
from formats.format_asr import parse_asr_messages_to_dialogue
from files.tmp import save_tmp

def load_config():
    with open("config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    if len(sys.argv) < 2:
        print("Usage: python sttcli.py <path-to-mp3>")
        sys.exit(1)

    config = load_config()
    file_path = sys.argv[1]
    base = os.path.splitext(file_path)[0]
    # 1. Загружаем файл в Object Storage
    file_url = upload_to_storage(config, file_path)

    # 2. Распознаем речь
    response = recognize_audio(config, file_url)

    # 2.1 Сохраняем raw JSONL
    save_tmp(base, response, ".jsonl")

    # 3. Преобразуем ASR → диалог
    text = parse_asr_messages_to_dialogue(response.strip().split("\n"))

    # 3.1 Сохраняем транскрипт
    save_tmp(base, text, ".txt")

    # 4. Генерируем summary
    summary = summarize(config, text)

    # 4.1 Сохраняем summary
    save_tmp(base, summary, ".summary.txt")

    print("✅ Готово!")

if __name__ == "__main__":
    main()
