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
        result = get_average_by_manufacturer(table, manufacturer)
        result = str(result)
        ui.print_result(result, "The avarage amount of games in stoc by {} is: ".format(manufacturer))

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

    id_ = common.generate_random(table)

    list_labels = ["title", "manufacturer", "price (dollars)", "in stock"]

    data_to_add = ui.get_inputs(list_labels, "Please provide title, manufacturer, price (dollars), item in stock")

    data_to_add.insert(0, id_)

    table.append(data_to_add)

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


def get_correct_type(user_input, answers_types, alpha_string):
    if answers_types == int:
        try:
            user_input = int(user_input)
        except:
            user_input = None
            ui.print_error_message("Wrong value provided.\n")

    elif answers_types == str:
        if alpha_string:
            user_input = user_input.replace(' ', '')

            if not user_input.isalpha():
                user_input = None
                ui.print_error_message('It not alpha string.')

    return user_input


def get_data_for_update(table, questions, answers_types, id_storage, id_, is_alpha):
    user_data = []

    for i in range(len(questions)):
        user_input = None

        while type(user_input) != answers_types[i]:
            user_input = ui.get_inputs([questions[i]], '')[0]
            user_input = get_correct_type(user_input, answers_types[i], is_alpha[i])
        #---------------------------------------------------------------------#
            # Other differences while asking for data here


        #---------------------------------------------------------------------#
        user_data.append(user_input)

    user_data.insert(0, id_)
    user_data = [str(record) for record in user_data]
    row_number = common.get_item_row(id_storage, id_)
    table[row_number] = user_data

    return table, row_number


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
        # Here u can make changes:
        #---------------------------------------------------------------------#
        list_options = ['Modify record']
        questions = ['Title', 'Manufacturer', 'Price (dollars)', 'In stock']
        answers_types = [str, str, int, int]
        is_alpha = [False, False, False, False]
        #---------------------------------------------------------------------#

        ui.print_menu('Possible orders:', list_options, "Exit to Menu")
        user_input = ui.get_inputs([''], '')[0]
        if user_input == '1':
            table, row = get_data_for_update(table, questions, answers_types, id_storage, id_, is_alpha)

        # Individual differences after getting data HERE \/


        #---------------------------------------------------------------------#
    else:
        ui.print_error_message('This option does not exist.')

    return table



# special functions:
# ------------------

# the question: How many different kinds of game are available of each manufacturer?
# return type: a dictionary with this structure: { [manufacturer] : [count] }
def get_counts_by_manufacturers(table):

    manufacturers_dict = {}
    for item in table:
        if item[2] in manufacturers_dict.keys():
            manufacturers_dict[item[2]] += 1
        else:
            manufacturers_dict[item[2]] = 1

    return manufacturers_dict


# the question: What is the average amount of games in stock of a given manufacturer?
# return type: number
def get_average_by_manufacturer(table, manufacturer):

    # maybe to common
    games = 0
    manufacturer_apperance = 0

    for i in range(len(table)):
        if manufacturer.lower() == table[i][2].lower():
            games += int(table[i][-1])
            manufacturer_apperance += 1

    avrg_games_by_manufacturer = games / manufacturer_apperance

    return avrg_games_by_manufacturer
