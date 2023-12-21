from DBConnection import DBConnect
from json import load as json_load

if __name__ == '__main__':
    with open('config.json') as config_file:
        config = json_load(config_file)
        cmd_structure = config["cmd_structure"]
    db = DBConnect(config["path_db"])

    print(list(cmd_structure))
    input_func = {level_name: func for level_name, func in zip(cmd_structure,
                                                               [db.insert_category, db.insert_fabricator,
                                                                db.insert_product, db.create_order])}
    show_func = {level_name: func for level_name, func in zip(cmd_structure, [db.show_category, db.show_fabricator,
                                                                              db.show_product, db.show_order])}
    print(input_func)
    inp: str = input()
    while inp != "exit":
        inp_list: list[str] = inp.split()
        match inp_list:
            case ["exit"]:
                print("Goodbye...")
            case ["debug", x]:
                if x == "True":
                    db.debug = True
                elif x == "False":
                    db.debug = False
                else:
                    print("Аргументом может быть только \"True\" или \"False\"")
            case ["input", level_name]:
                if level_name in input_func:
                    args = []
                    max_arg_len = max(map(len, cmd_structure[level_name]))
                    for arg in cmd_structure[level_name]:
                        if arg != "product_quant_lst":
                            args.append(input(f"{arg}".ljust(max_arg_len) + " < "))
                        else:
                            product_quantity_list = []
                            product = input("Product or \"stop\"".ljust(max_arg_len) + " < ")
                            while product not in ["stop", ""]:
                                quantity = input(f"Quantity of \"{product}\"".ljust(max_arg_len) + " < ")
                                product_quantity_list.append((product, quantity))
                                product = input("Product or \"stop\"".ljust(max_arg_len) + " < ")
                            args.append(product_quantity_list)
                    try:
                        input_func[level_name](*args)
                    except ValueError as E:
                        print(f"{"".join(E.args)}")
                else:
                    print(f"Такого уровня не существует.\n"
                          f"Существующие уровни для вставки: {", ".join(input_func.keys())}")
            case ["show", level_name]:
                if level_name in show_func:
                    print(f"{level_name}:\n\t- " +
                          "\n\t- ".join(map(repr, show_func[level_name]())))
                else:
                    print(f"Такого уровня не существует.\n"
                          f"Существующие уровни для вставки: {", ".join(input_func.keys())}")
            case ["filter"]:
                params = ["order_id", 'product_name', "quantity", "fabricator_name", "category_name"]
                args = []
                max_arg_len = max(map(len, params))
                print("Введите критерии для поиска: (Чтобы не вводить критерий нажмите \"Enter\")")
                for param in params:
                    args.append(input(f"{param}".ljust(max_arg_len) + " < "))
                print(
                    "Order journal:\n\t- " +
                    "\n\t- ".join(map(repr, db.search_by_criteria(*args)))
                )
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
            case req:
                print("Неверный запрос.\nДля помощи введите \"help\"")
        inp = input()
