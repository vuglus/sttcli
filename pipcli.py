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
    summary = meta_info + text
    user_prompt = ''

    if instruction is None:
        instruction, user_prompt  = choose_instruction(config)
    

    while True:
        # Выбираем инструкцию
        print(f"→ Генерирую ответ на {instruction} запрос:")
        draw_context(user_prompt)

        summary = summarizer.summarize(
            summary,
            instruction_type = instruction,  # Keep 'manual' as instruction_type
            context = context,
            manual_prompt = user_prompt  # Pass the manual prompt separately
        )        
        draw_context(summary)
        next_instruction, user_prompt  = choose_instruction(config)
        # Если выбрана инструкция quit, выходим из цикла
        if next_instruction == 'quit': 
            break
        # Если нет то продолжаем цикл
        instruction = next_instruction


    # После завершения manual режима выходим из программы
    print("Работа в режиме chat завершена.")

    if output_file is None:
        # Generate timestamp in DD-MM-YY-HH-SS format
        timestamp = datetime.datetime.now().strftime("%d-%m-%y-%H-%M-%S")
        output_file = f"{base}_{timestamp}.{instruction}.md"

    # Сохраняем результат
    save_local(output_file, summary)

if __name__ == "__main__":
    main()
