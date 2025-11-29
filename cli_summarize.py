import sys
import os
import yaml
import datetime
from instruction.choose import choose_instruction
from files.tmp import save_local  
from files.context import load_context_for, draw_context
from func.args import parse_args
from models import get_model

def main():
    input_path, instruction, output_file = parse_args(sys.argv)

    base, ext = os.path.splitext(input_path)
    # Загружаем конфиг
    config_path = os.path.join(os.path.dirname(__file__), "config.yml")
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    ModelClass = get_model(config['model_name'])
    if not ModelClass:
        print(f"❌ No model for: {config['model_name']}")
        return
    summarizer = ModelClass(config)

    # Выбираем инструкцию
    if len(sys.argv) >= 3:
        instruction = sys.argv[2]
    else:
        instruction = choose_instruction(config)

    # Получаем контекст
    context = load_context_for(input_path)

    # Отображаем контекст
    if context != "":
        draw_context(context)

    # Получаем метаданные файла
    file_name = os.path.basename(input_path)
    created_ts = os.path.getctime(input_path)
    created_date = datetime.datetime.fromtimestamp(created_ts).strftime("%Y-%m-%d %H:%M:%S")

    # Читаем исходный текст
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Добавляем имя и дату создания файла в начало текста
    meta_info = f"Файл: {file_name}\nДата создания: {created_date}\n\n"
    text_with_meta = meta_info + text

    print(f"→ Генерирую саммари с инструкцией '{instruction}'...")
    summary = summarizer.summarize(
        text_with_meta, 
        instruction_type = instruction,
        context = context
    )

    if output_file is None: 
        output_file = base + f".{instruction}.md" 

    # Сохраняем результат
    save_local(output_file, summary)

if __name__ == "__main__":
    main()
