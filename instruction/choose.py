def choose_instruction(config, user_enabled = True):
    """
    Спрашивает у пользователя, какую инструкцию применять, если не передано через CLI.
    По умолчанию выбирает тип manual и ждет ввода текста.
    Если введена цифра или введённый текст инструкция то выбирать её.
    """
    instr_dict = config.get("instructions", {})
    instructions = list(instr_dict.keys())
    
    # Показываем доступные инструкции
    print("Доступные инструкции:")
    for i, instr in enumerate(instructions, 1):
        print(f"{i}. {instr}")
    print("Или введите свой промпт:")
    
    user_input = input().strip()
    
    # Проверяем, является ли ввод числом (выбор инструкции по номеру)
    if user_input.isdigit():
        idx = int(user_input) - 1
        if 0 <= idx < len(instructions):
            instruction_key = instructions[idx]
            # Проверяем, является ли инструкция служебной
            if instruction_key == 'join':
                # Возвращаем ключ для служебных инструкций
                return (instruction_key, instr_dict[instruction_key])
            # Возвращаем саму инструкцию
            return (instruction_key, instr_dict[instruction_key])
    
    # Проверяем, совпадает ли ввод с названием инструкции
    if user_input in instr_dict:
        instruction_key = user_input
        # Проверяем, является ли инструкция служебной
        if instruction_key == 'join':
            # Возвращаем ключ для служебных инструкций
            return (instruction_key, instr_dict[instruction_key])
        # Возвращаем саму инструкцию
        return (instruction_key, instr_dict[instruction_key])
    if user_input in ['quit', 'exit', 'q', 'e']:
        return ('quit', user_input)
    
    # Если ввод не совпадает ни с одной инструкцией, считаем его промптом
    return ('manual', user_input)
