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
    print(input_func)
    inp: str = input()
    while inp != "exit":
        inp_list: list[str] = inp.split()
        match inp_list:
            case ["exit"]:
                print("Goodbye...")
            case ["debug", x]:
                if x == "True":
                    db = DBConnect(config["path_db"], debug=True)
                elif x == "False":
                    db = DBConnect(config["path_db"], debug=False)
                else:
                    print("Аргументом может быть только \"True\" или \"False\"")
            case ["input", level_name]:
                if level_name in input_func:
                    args = []
                    max_arg_len = max(map(len, cmd_structure[level_name]))
                    for arg in cmd_structure[level_name]:
                        if arg != "product_quantity_list":
                            args.append(input(f"{arg}".ljust(max_arg_len)+" < "))
                        else:
                            product_quantity_list = []
                            product = input("Product or \"stop\"".ljust(max_arg_len)+" < ")
                            while product not in ["stop", ""]:
                                quantity = input(f"Quantity of \"{product}\"".ljust(max_arg_len)+" < ")
                                product_quantity_list.append((product, quantity))
                                product = input("Product or \"stop\"".ljust(max_arg_len)+" < ")
                            args.append(product_quantity_list)
                    try:
                        input_func[level_name](*args)
                    except ValueError as E:
                        print(f"{"".join(E.args)}")
                else:
                    print(f"Такого уровня не существует.\nСуществующие уровни для вставки: {", ".join(input_func.keys())}")
            case req:
                print(f"Неверный запрос")
        inp = input()
