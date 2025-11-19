def choose_instruction(config, context_enabled = True):
    """
    Спрашивает у пользователя, какую инструкцию применять, если не передано через CLI.
    Берёт список ключей из config['instructions'].
    """
    instr_dict = config.get("instructions", {})
    if not instr_dict:
        raise ValueError("В конфиге нет блока 'instructions'")

    instructions = list(instr_dict.keys())

    print("Выберите инструкцию анализа:")
    if context_enabled : 
        print("0. Сохранить контекст")

    for i, instr in enumerate(instructions, 1):
        print(f"{i}. {instr}")

    while True:
        choice = input("Введите номер инструкции: ").strip()
            
        if choice.isdigit():
            if int(choice) == 0: 
                return 'context'
            idx = int(choice) - 1
            if 0 <= idx < len(instructions):
                return instructions[idx]
        print("Неверный ввод, попробуйте снова.")
