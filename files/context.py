import os
import shutil

CONTEXT_DIR = "./data/"
CONTEXT_FILE = "context.txt"
CONTEXT_PREFIX = "\n There is context you can use: \n"

def save_context_file(file_path: str, context_file = CONTEXT_FILE):
    """
    Сохраняет переданный файл в папку ./data.
    Имя файла сохраняется без изменений.
    """
    if not os.path.exists(file_path):
        print(f"❌ Файл {file_path} не найден")
        return

    os.makedirs(CONTEXT_DIR, exist_ok=True)
    dest_path = os.path.join(CONTEXT_DIR, context_file)
    shutil.copy(file_path, dest_path)

    print(f"✅ Файл сохранен в {dest_path}")


def save_context(text, context_file = CONTEXT_FILE):
    target_file = os.path.join(CONTEXT_DIR, context_file)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Контекст сохранен в {context_file}")

def load_context(context_file = CONTEXT_FILE):
    """
    Читает контекст из файла ./data/context.txt, если он существует.
    Возвращает строку с содержимым файла, иначе пустую строку.
    """
    source_file = os.path.join(CONTEXT_DIR, context_file)
    
    if os.path.exists(source_file):
        with open(source_file, "r", encoding="utf-8") as f:
            return CONTEXT_PREFIX + f.read()
    return ""
