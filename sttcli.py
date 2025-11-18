import os
import sys
import yaml
from stt_recognize import recognize_audio  # импорт из отдельного файла
from summarize.yandex import summarize  # импорт из отдельного файла
from stt_upload import upload_to_storage
from formats.format_asr import parse_asr_messages_to_dialogue
from files.tmp import save_dir
from instruction.choose import choose_instruction

def load_config():
    with open("config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not file_path:
        print("Usage: python sttcli.py <path-to-mp3> [instruction]")
        sys.exit(1)

    config = load_config()
    file_path = sys.argv[1]

    # Если инструкция передана через CLI — используем её, иначе спрашиваем
    if len(sys.argv) >= 3:
        instruction = sys.argv[2]
    else:
        instruction = choose_instruction(config)

    base = os.path.splitext(file_path)[0]    
    # 1. Загружаем файл в Object Storage
    file_url = upload_to_storage(config, file_path)

    # 2. Распознаем речь
    response = recognize_audio(config, file_url)

    # 2.1 Сохраняем raw JSONL
    save_dir(base, response, ".jsonl")

    # 3. Преобразуем ASR → диалог
    text = parse_asr_messages_to_dialogue(response.strip().split("\n"))

    # 3.1 Сохраняем транскрипт
    save_dir(base, text, ".txt")

    # 4. Генерируем summary
    summary = summarize(config, text, instructionType = instruction)

    # 4.1 Сохраняем summary
    save_dir(base, summary, f".{instruction}.md")

    print("✅ Готово!")

if __name__ == "__main__":
    main()
