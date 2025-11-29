import sys
import os

def parse_args(argv):
    """
    Разбирает аргументы командной строки и возвращает:
    - input_path: путь к входному файлу
    - instruction: тип инструкции (или None)
    - output_file: путь к файлу вывода (или None)
    """
    if len(argv) < 2:
        print("Использование: python summarize_file.py <файл> [инструкция] [--output файл]")
        sys.exit(1)

    input_path = argv[1]
    instruction = None
    output_file = None

    args = argv[2:]

    i = 0
    while i < len(args):
        arg = args[i]

        if arg == "--output":
            if i + 1 < len(args):
                output_file = args[i + 1]
                i += 2
                continue
            else:
                print("❌ Ошибка: после --output должен быть указан файл")
                sys.exit(1)

        # Если это не флаг, и инструкция ещё не выбрана
        if instruction is None and not arg.startswith("--"):
            instruction = arg

        i += 1

    if not os.path.exists(input_path):
        print(f"Файл не найден: {input_path}")
        sys.exit(1)

    if output_file is not None:
        output_file = _resolve_output_path(input_path, output_file)

    return input_path, instruction, output_file    

def _resolve_output_path(input_path: str, output_file: str) -> str:
    """
    Если output_file содержит путь — вернуть как есть.
    Если путь не указан — сохранить рядом с исходным файлом.
    """
    # Путь указан? (например: "D:/out/file.md", "./file.md", "../file.md")
    if os.path.dirname(output_file):
        return output_file

    # Путь НЕ указан → сохраняем рядом с исходным файлом
    input_dir = os.path.dirname(input_path)
    return os.path.join(input_dir, output_file)