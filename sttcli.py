import yaml
import sys
import os
import tempfile
from ycloudml import YCloud
from ycloudml.models import YandexGPT

def load_config():
    with open("config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def upload_to_bucket(ycloud, bucket, file_path):
    file_name = os.path.basename(file_path)
    return ycloud.storage.upload(bucket, file_path, file_name)

def transcribe_audio(ycloud, file_url, lang="ru-RU"):
    job = ycloud.speech.recognize(url=file_url, language=lang)
    return job.result_text()

def generate_summary(gpt, text):
    prompt = f"Сделай краткое саммари следующего текста:\n\n{text}"
    return gpt.complete(prompt, temperature=0.3)

def main():
    if len(sys.argv) < 2:
        print("Usage: sttcli.py <path-to-audio-file>")
        sys.exit(1)
    
    config = load_config()
    audio_path = sys.argv[1]
    base, _ = os.path.splitext(audio_path)

    ycloud = YCloud(folder_id=config["yacloud"]["folder_id"], oauth_token=config["yacloud"]["oauth_token"])
    gpt = YandexGPT(model=config["gpt"]["model"], folder_id=config["yacloud"]["folder_id"], oauth_token=config["yacloud"]["oauth_token"])

    # upload
    file_url = upload_to_bucket(ycloud, config["yacloud"]["bucket_name"], audio_path)

    # transcription
    text = transcribe_audio(ycloud, file_url, lang=config["stt"]["language"])
    with open(f"{base}.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # summary
    summary = generate_summary(gpt, text)
    with open(f"{base}.summary.txt", "w", encoding="utf-8") as f:
        f.write(summary)

    print("✅ Done:", base + ".txt", "and", base + ".summary.txt")

if __name__ == "__main__":
    main()
