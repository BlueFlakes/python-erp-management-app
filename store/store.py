# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# title: string
# manufacturer: string
# price: number (dollars)
# in_stock: number

# importing everything you need
import os
# User interface module
import ui
# data manager module
import data_manager
# common module
import common


def choose_option(table):
    inputs = ui.get_inputs(["Please enter a number: "], "")
    option = inputs[0]

    if option == "1":
        show_table(table)
    elif option == "2":
        table = add(table)
    elif option == "3":
        id_ = ui.get_inputs(["Id"], "Please provide record you want to remove")[0]
        table = remove(table, id_)
    elif option == "4":
        id_ = ui.get_inputs(["Id"], "Please provide record you want to update")[0]
        table = update(table, id_)
    elif option == "5":
        result = get_counts_by_manufacturers(table)
        ui.print_result(result, "Each manufacturer have created")
    elif option == "6":
        manufacturer = ui.get_inputs(["Manufacturer"], "Please provide manufacturer which" +
                                     "amount of games you want see")[0]
        try:
            result = get_average_by_manufacturer(table, manufacturer)
            result = str(result)
            ui.print_result(result, "The avarage amount of games in stoc by {} is: ".format(manufacturer))
        except UnboundLocalError as err:
            ui.print_error_message(err)

    return option, table


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file('store/games.csv')

    list_options = ["Show table", "Add", "Remove", "Update",
                    "Count of games by manufacturer",
                    "Avarege amount of games in stock by manufacturer"
                    ]

    option = float("inf")
    while not option == "0":
        ui.print_menu("Store manager", list_options, "Exit to Menu")
        option, table = choose_option(table)

    data_manager.write_table_to_file('store/games.csv', table)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    title_list = ["id", "title", "manufacturer", "price (dollars)", "in stock"]

    ui.print_table(table, title_list)


def add(table):
    """
    Asks user for input and adds it into the table.

    Args:
        table: table to add new record to

    Returns:
        Table with a new record
    """
    id_storage = common.get_values_from_column(table, 0)
    id_ = common.generate_random(table)
    table = manage_data_from_user(table, id_storage, id_, False)

    return table


def remove(table, id_):
    """
    Remove a record with a given id from the table.

    Args:
        table: table to remove a record from
        id_ (str): id of a record to be removed

    Returns:
        Table without specified record.
    """
    table, successful = common.remove_record(table, id_)

    if not successful:
        ui.print_error_message('Error!')

    return table


def get_correct_data_types(user_input, answer_type, alpha_string):
    """
    get_correct_data_types function change the type of input to
    it's expected type.

    Args:
        param1: user_input (str)
        param2: answer_type (the type which input should have)
        param3: alpha_string (bool)

    Returns:
        user_input (str or int)
    """
    if answer_type == int:
        try:
            user_input = int(user_input)
        except ValueError:
            user_input = None
            ui.print_error_message("Wrong value provided.\n")

    elif answer_type == str:
        if alpha_string:
            user_input_copy = user_input.replace(' ', '')

            if not user_input_copy.isalpha():
                user_input = None
                ui.print_error_message('It not alpha string.')

    return user_input


def get_data_from_user(questions, answers_types, id_storage, id_, is_alpha):
    """
    Take input from user and delegates validation analysis.

    Args:
        param1: questions (list)
        param2: answers_types (list)
        param3: id_storage (list)
        param4: id_ (str)
        param5: is_alpha (bool)

    Returns:
        user_data (list)
    """
    user_data = []

    for i in range(len(questions)):
        user_input = None

        while type(user_input) != answers_types[i]:
            user_input = ui.get_inputs([questions[i]], '')[0]
            user_input = get_correct_data_types(user_input, answers_types[i], is_alpha[i])

            # Other differences while asking for data here

        user_data.append(user_input)

    user_data = [str(record) for record in user_data]

    return user_data

def manage_data_from_user(table, id_storage, id_, update_row=False):
    """
    Take input from user and delegates validation analysis.

    Args:
        param1: table (list)
        param2: id_storage (list)
        param3: id_ (str)
        param4: update_row (bool)

    Returns:
        table (list)
    """
    questions = ['Title', 'Manufacturer', 'Price (dollars)', 'In stock']
    answers_types = [str, str, int, int]
    is_alpha = [False, False, False, False]

    if update_row:
        list_options = ['Modify record']
    else:
        list_options = ['Add record']

    ui.print_menu('Possible orders:', list_options, "Exit to Menu")
    user_input = ui.get_inputs([''], '')[0]

    if user_input == '1':
        user_data = get_data_from_user(questions, answers_types, id_storage, id_, is_alpha)

        if update_row:
            row_number = common.get_item_row(id_storage, id_)
            user_data.insert(0, id_)
            table[row_number] = user_data

        else:
            user_data.insert(0, id_)
            table.append(user_data)

    return table


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table: list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        table with updated record
    """
    id_storage = common.get_values_from_column(table, 0)
    if id_ in id_storage:
        table = manage_data_from_user(table, id_storage, id_, True)
        # Here u can make changes:

    else:
        ui.print_error_message('This option does not exist.')

    return table


# special functions:
# ------------------

# the question: How many different kinds of game are available of each manufacturer?
# return type: a dictionary with this structure: { [manufacturer] : [count] }
def get_counts_by_manufacturers(table):
    """
    Check how many different games are made by each manufacturer.
    Return dictionary where key is manufacturer and value is number of games by it.

    Args:
        table: list of lists with data

    Returns:
        dict: key (str), value (int)
    """
    manufacturers_dict = {}
    for item in table:
        try:
            if item[2]:
                try:
                    if item[2] in manufacturers_dict.keys():
                        manufacturers_dict[item[2]] += 1
                    else:
                        manufacturers_dict[item[2]] = 1
                except IndexError:
                    pass
            else:
                raise ValueError
        except ValueError:
            pass

    return manufacturers_dict


# the question: What is the average amount of games in stock of a given manufacturer?
# return type: number
def get_average_by_manufacturer(table, manufacturer):
    """
    Give back average amount of games in stock of a given manufacturer.
    Count how many different games are in stock by given manufacturer and
    how many copies of them are in total. On that base avarege amount is count.

    Args:
        table: list of lists with data

    Returns:
        dict: key (str), value (int)
    """
    games = 0
    manufacturer_apperance = 0

    for i in range(len(table)):
        try:
            if manufacturer.lower() == table[i][2].lower():
                games += int(table[i][-1])
                manufacturer_apperance += 1
        except (IndexError, ValueError):
            pass

    try:
        avrg_games_by_manufacturer = games / manufacturer_apperance
    except ZeroDivisionError as err:
        ui.print_error_message("No entry with that manufacturer")

    avrg_games_by_manufacturer = round(avrg_games_by_manufacturer, 2)

    return avrg_games_by_manufacturer
