def choose_instruction(config, user_enabled = True):
    """
    Спрашивает у пользователя, какую инструкцию применять, если не передано через CLI.
    Берёт список ключей из config['instructions'].
    Возвращает саму инструкцию, а не её тип.
    """
    instr_dict = config.get("instructions", {})
    if not instr_dict:
        raise ValueError("В конфиге нет блока 'instructions'")

    instructions = list(instr_dict.keys())

    print("Выберите инструкцию анализа:")
    if user_enabled :
        print("0. Ввести вручную")

    for i, instr in enumerate(instructions, 1):
        print(f"{i}. {instr}")

    while True:
        choice = input("Введите номер инструкции (q для выхода): ").strip()
            
        if choice.lower() in [ 'q', 'quit', 'e', 'exit']:
            return ('quit', '')

        elif choice.isdigit():
            if int(choice) == 0:
                manual_prompt = input("Введите ваш промпт: ").strip()
                # Для ручного ввода возвращаем кортеж с 'manual' и промптом
                return ('manual', manual_prompt)
            idx = int(choice) - 1
            if 0 <= idx < len(instructions):
                instruction_key = instructions[idx]
                # Проверяем, является ли инструкция служебной
                if instruction_key == 'join':
                    # Возвращаем ключ для служебных инструкций
                    return (instruction_key, instr_dict[instruction_key])
                # Возвращаем саму инструкцию
                return (instruction_key, instr_dict[instruction_key])
        print("Неверный ввод, попробуйте снова.")
