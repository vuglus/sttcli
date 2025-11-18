#!/usr/bin/env python3
"""
Тестовый скрипт для проверки парсера ASR сообщений.
Читает JSON строки из файла и передает их в функцию парсинга.
"""

import json
import sys
from formats.format_asr import format_dialogue_from_asr

def read_json_lines_from_file(filename: str) -> list:
    """
    Читает JSON строки из файла.
    
    Args:
        filename: Имя файла для чтения
        
    Returns:
        Список JSON строк
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # Читаем все строки, убираем пустые
            lines = [line.strip() for line in file if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

def main():
    """
    Основная функция тестирования.
    """
    if len(sys.argv) != 2:
        print("Использование: python test_parser.py <файл_с_json_строками>")
        print("Пример: python test_parser.py asr_output.txt")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    print(f"Чтение JSON строк из файла: {filename}")
    json_lines = read_json_lines_from_file(filename)
    
    if not json_lines:
        print("Не удалось прочитать данные из файла.")
        sys.exit(1)
    
    print(f"Прочитано {len(json_lines)} строк.")
    print("-" * 80)
    
    # Проверяем, что строки являются валидным JSON
    valid_count = 0
    for i, line in enumerate(json_lines, 1):
        try:
            json.loads(line)
            valid_count += 1
        except json.JSONDecodeError:
            print(f"Строка {i}: Некорректный JSON")
    
    print(f"Валидных JSON строк: {valid_count}/{len(json_lines)}")
    print("-" * 80)
    
    # Передаем данные в функцию парсинга
    print("Результат парсинга:")
    print("-" * 80)
    
    result = format_dialogue_from_asr(json_lines)
    print(result)

def test_with_sample_data():
    """
    Функция для тестирования с примером данных (если нет файла).
    """
    print("Тестирование с примером данных...")
    print("-" * 80)
    
    # Пример данных для тестирования
    sample_data = [
        '{"result":{"sessionUuid":{"uuid":"test","userRequestId":"undefined"},"audioCursors":{"receivedDataMs":"55400","resetTimeMs":"0","partialTimeMs":"7109","finalTimeMs":"7109","finalIndex":"0","eouTimeMs":"0"},"responseWallTimeMs":"1385","final":{"alternatives":[{"words":[{"text":"в","startTimeMs":"3460","endTimeMs":"3500"},{"text":"данной","startTimeMs":"3560","endTimeMs":"3820"}],"text":"в данной","startTimeMs":"0","endTimeMs":"7109","confidence":0,"languages":[]}],"channelTag":"0"},"channelTag":"0"}}',
        '{"result":{"sessionUuid":{"uuid":"test","userRequestId":"undefined"},"audioCursors":{"receivedDataMs":"55400","resetTimeMs":"0","partialTimeMs":"7109","finalTimeMs":"7109","finalIndex":"0","eouTimeMs":"0"},"responseWallTimeMs":"1386","finalRefinement":{"finalIndex":"0","normalizedText":{"alternatives":[{"words":[{"text":"в","startTimeMs":"3460","endTimeMs":"3500"},{"text":"данной","startTimeMs":"3560","endTimeMs":"3820"}],"text":"В данной","startTimeMs":"0","endTimeMs":"7109","confidence":0,"languages":[]}],"channelTag":"0"}},"channelTag":"0"}}',
        '{"result":{"sessionUuid":{"uuid":"test","userRequestId":"undefined"},"audioCursors":{"receivedDataMs":"55400","resetTimeMs":"0","partialTimeMs":"7109","finalTimeMs":"7109","finalIndex":"0","eouTimeMs":"7109"},"responseWallTimeMs":"1386","eouUpdate":{"timeMs":"7109"},"channelTag":"0"}}'
    ]
    
    result = format_dialogue_from_asr(sample_data)
    print(result)

if __name__ == "__main__":
    # Если передан аргумент - используем файл, иначе тестируем с примером
    if len(sys.argv) == 2:
        main()
    else:
        print("Для использования с файлом: python test_parser.py <файл>")
        print("Запуск теста с примером данных:")
        print()
        test_with_sample_data()