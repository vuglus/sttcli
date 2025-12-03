# Speech to text CLI interface
import os
import sys
import yaml
from recognize.yandex import recognize_audio  # Import from separate file
from files.upload import upload_to_storage
from formats.format_asr import parse_asr_messages_to_dialogue
from files.tmp import save_dir

def load_config():
    with open("config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    config = load_config()
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    if not file_path:
        print("Usage: python sttcli.py <path-to-mp3>")
        sys.exit(1)

    file_path = sys.argv[1]

    base = os.path.splitext(file_path)[0]
    # 1. Upload file to Object Storage
    file_url = upload_to_storage(config, file_path)

    # 2. Recognize speech
    response = recognize_audio(config, file_url)

    # 2.1 Save raw JSONL
    save_dir(base, response, ".jsonl")

    # 3. Convert ASR to dialogue
    text = parse_asr_messages_to_dialogue(response.strip().split("\n"))

    # 3.1 Save transcript
    save_dir(base, text, ".txt")

    print("✅ Done!")

if __name__ == "__main__":
    main()
