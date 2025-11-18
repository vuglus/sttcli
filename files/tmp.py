import os

def save_dir(base_name, content, ext):
    """
    Сохранение промежуточных файлов в папку с именем файла без расширения.

    :param base_name: путь к файлу без расширения (например "audio/file1")
    :param content: текст для записи
    :param ext: расширение файла (например ".jsonl")
    :return: путь к сохранённому файлу
    """
    # Имя папки — это имя файла без последнего расширения
    os.makedirs(base_name, exist_ok=True)

    # Имя файла с расширением
    file_name = os.path.basename(base_name) + ext
    out_path = os.path.join(base_name, file_name)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"💾 Файл сохранён: {out_path}")
    return out_path

def save_local(base_name, content, ext):
    """
    Сохранение промежуточных файлов

    :param base_name: путь к файлу без расширения (например "audio/file1")
    :param content: текст для записи
    :param ext: расширение файла (например ".jsonl")
    :return: путь к сохранённому файлу
    """
    # Имя файла с расширением
    out_path = base_name + ext

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"💾 Файл сохранён: {out_path}")
    return out_path
