import os

def save_tmp(base_name, content, ext, folder="tmp"):
    """
    Сохранение промежуточных файлов в поддиректорию tmp.

    :param base_name: путь без расширения (например "audio/file1")
    :param content: текст для записи
    :param ext: расширение файла (например ".jsonl")
    :param folder: имя подпапки (по умолчанию "tmp")
    :return: путь к сохранённому файлу
    """
    # Определяем папку рядом со скриптом
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tmp_dir = os.path.join(script_dir, folder)

    os.makedirs(tmp_dir, exist_ok=True)

    file_name = os.path.basename(base_name) + ext
    out_path = os.path.join(tmp_dir, file_name)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"💾 Файл сохранён: {out_path}")
    return out_path
