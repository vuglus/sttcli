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

    input_path = None
    instruction = None
    output_file = None

    # Parse command line arguments
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg == "--output" and i + 1 < len(argv):
            # Only accept the next argument as output_file if it doesn't start with --
            if not argv[i + 1].startswith("--"):
                output_file = argv[i + 1]
                i += 2  # Skip next argument
                continue
            else:
                # If the next argument starts with --, we ignore this --output flag
                i += 1
        elif not input_path and not arg.startswith("--"):
            input_path = arg
        elif not instruction and not arg.startswith("--"):
            instruction = arg
        i += 1
    
    if not input_path:
        print("Использование: python summarize_file.py <файл> [инструкция] [--output файл]")
        sys.exit(1)

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