from DBConnection import DBConnect
from json import load as json_load

if __name__ == '__main__':
    # Открытие файлика конфга
    with open('config.json') as config_file:
        config = json_load(config_file)
        cmd_structure = config["cmd_structure"]

    # Инициализация подключения к базе данных по путю config["path_db"]
    db = DBConnect(config["path_db"])

    # Ссылки на методы нашей библиотеки для вставки
    input_func = {level_name: func for level_name, func in zip(cmd_structure,
                                                               [db.insert_category, db.insert_fabricator,
                                                                db.insert_product, db.create_order])}

    # Ссылки на методы нашей библиотеки для показа информации из бд
    show_func = {level_name: func for level_name, func in zip(cmd_structure, [db.show_category, db.show_fabricator,
                                                                              db.show_product, db.show_order])}

    # Первый ввод пользователя
    inp: str = input()
    # Завершаем цикл когда пользователь вводит "exit"
    while inp != "exit":
        # Делаем из ввода пользователя список слов
        inp_list: list[str] = inp.split()
        # Конструкция для проверки ввода пользователя
        match inp_list:
            case ["exit"]:
                print("Goodbye...")

            # Для отладки
            case ["debug", x]:
                if x == "True":
                    db.debug = True
                elif x == "False":
                    db.debug = False
                else:
                    print("Аргументом может быть только \"True\" или \"False\"")

            # Ввод данных
            case ["input", level_name]:
                # Проверка на существующий уровень вставки
                if level_name in input_func:
                    # Аргументы, ввод которых сохраняется
                    args = []
                    # Визуальные отступы стрелочек
                    max_arg_len = max(map(len, cmd_structure[level_name]))
                    # arg - аргументы которые надо ввести
                    for arg in cmd_structure[level_name]:
                        # Отлов бесконечного ввода продуктов (ведь продуктов в одном заказе может быть больше одного)
                        if arg != "product_quant_lst":
                            args.append(input(f"{arg}".ljust(max_arg_len) + " < "))
                        else:
                            # Список продуктов и их кол-во
                            product_quantity_list = []
                            # Ввод продукта
                            product = input("Product or \"stop\"".ljust(max_arg_len) + " < ")
                            # Проверка если продукт = stop чтобы выйти из цикла
                            while product not in ["stop", ""]:
                                # Ввод кол-ва продуктов
                                quantity = input(f"Quantity of \"{product}\"".ljust(max_arg_len) + " < ")
                                # Добавляем в список
                                product_quantity_list.append((product, quantity))
                                # Повторяем ввод продукта
                                product = input("Product or \"stop\"".ljust(max_arg_len) + " < ")
                            # Добавляем в аргументы к функции список продуктов
                            args.append(product_quantity_list)

                    # Конструкция для отлова ошибок
                    try:
                        # Вызов нужного метода для вставки
                        input_func[level_name](*args)
                    except ValueError as E:
                        # Сообщение об ошибке
                        print(f"{"".join(E.args)}")
                # Неправильно ввели уровень
                else:
                    print(f"Такого уровня не существует.\n"
                          f"Существующие уровни для вставки: {", ".join(input_func.keys())}")

            # Команда для показа данных из базы данных
            case ["show", level_name]:
                # Проверка наличия данного уровня
                if level_name in show_func:
                    print(f"{level_name}:\n\t- " +
                          "\n\t- ".join(map(repr, show_func[level_name]())))
                else:
                    print(f"Такого уровня не существует.\n"
                          f"Существующие уровни для вставки: {", ".join(input_func.keys())}")
            # Вывод журнала с фильтрами
            case ["filter"]:
                # Необходимые параметры ввода для фильтра
                params = ["order_id", 'product_name', "quantity", "fabricator_name", "category_name"]
                # То, что мы вводим
                args = []
                # Украшалка для ввода
                max_arg_len = max(map(len, params))
                print("Введите критерии для поиска: (Чтобы не вводить критерий нажмите \"Enter\")")
                # Ввод каждого параметра
                for param in params:
                    args.append(input(f"{param}".ljust(max_arg_len) + " < "))
                print(
                    "Order journal:\n\t- " +
                    "\n\t- ".join(map(repr, db.search_by_criteria(*args)))
                )
            # помощь
            case ["help"]:
                print("Доступные команды:\n"
                      "\t- show {level_name} \t- показывает информацию данного уровня.\n"
                      "\t- input {level_name} \t- вставляет информацию данного уровня.\n"
                      "\t- debug {True/False} \t- включает/выключает режим отладки.\n"
                      "\t- filter\t- фильтр заказов по критериям.\n"
                      "\t- exit  \t- выход из программы.\n"
                      "\t- help  \t- помощь.\n"
                      "Доступные уровни:\n\t- " +
                      "\n\t- ".join(cmd_structure))
            # Если ввели неправильный запрос
            case req:
                print("Неверный запрос.\nДля помощи введите \"help\"")
        inp = input()
