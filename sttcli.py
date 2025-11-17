import os
import sys
import yaml
from stt_recognize import recognize_audio  # импорт из отдельного файла
from summarize.yandex import summarize  # импорт из отдельного файла
from stt_upload import upload_to_storage

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

    # загрузка в Object Storage
    file_url = upload_to_storage(config, file_path)

    # распознавание речи
    text = recognize_audio(config, file_url)
    with open(f"{base}.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"💾 Транскрипт сохранён: {base}.txt")

    # генерация саммари
    summary = summarize(config, text)
    with open(f"{base}.summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"💾 Саммари сохранено: {base}.summary.txt")

    print("✅ Готово!")

if __name__ == "__main__":
    main()
