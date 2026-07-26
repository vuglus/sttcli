# Speech to text CLI interface
import os
import sys
import yaml
import logging
from recognize.yandex import recognize_audio  # Import from separate file
from files.upload import upload_to_storage
from formats.format_asr import parse_asr_messages_to_dialogue

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
logger = logging.getLogger(__name__)


def load_config():
    with open("config.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_local(output_file, content):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info(f"💾 Файл сохранён: {output_file}")

def parse_args():
    """Parse command line arguments and return (file_path, output_path, save_log)"""
    file_path = None
    output_path = None
    save_log = False
    
    # Parse command line arguments
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--log":
            save_log = True
        elif arg == "--output" and i + 1 < len(sys.argv):
            # Only accept the next argument as output_path if it doesn't start with --
            if not sys.argv[i + 1].startswith("--"):
                output_path = sys.argv[i + 1]
                i += 1  # Skip next argument
            # If the next argument starts with --, we ignore this --output flag
        elif not file_path and not arg.startswith("--"):
            file_path = arg
        i += 1
    
    if not file_path:
        logger.info("Usage: python sttcli.py <path-to-mp3> [--log] [--output <output-file>]")
        sys.exit(1)
        
    return file_path, output_path, save_log

def main():
    config = load_config()
    file_path, output_path, save_log = parse_args()
    
    base = os.path.splitext(file_path)[0]
    # 1. Upload file to Object Storage
    file_url = upload_to_storage(config, file_path, logger)

    # 2. Recognize speech
    response = recognize_audio(config, file_url, logger)

    # 2.1 Save raw JSONL only if --log flag is present
    if save_log:
        log_path = base + ".jsonl"
        save_local(log_path, response)

    # 3. Convert ASR to dialogue
    text = parse_asr_messages_to_dialogue(response.strip().split("\n"))

    # 3.1 Save transcript to specified output file or next to mp3 file
    if output_path:
        txt_path = output_path
    else:
        txt_path = base + ".txt"
    save_local(txt_path, text)

    logger.info("✅ Done!")

if __name__ == "__main__":
    main()
