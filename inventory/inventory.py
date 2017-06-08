# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: string
# manufacturer: string
# purchase_date: number (year)
# durability: number (year)


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
        result = get_available_items(table)
        ui.print_result(result, "Item that not exceed their durability: ")
    elif option == "6":
        result = get_average_durability_by_manufacturers(table)
        ui.print_result(result, "Average durability itmes for each manufacturer: ")

    return option, table


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file('inventory/inventory.csv')

    list_options = ["Show table", "Add", "Remove", "Update",
                    "Available items", "Avarege durability of tiems by manufacturers"
                    ]

    option = float("inf")
    while not option == "0":
        ui.print_menu("Inventory manager", list_options, "Exit to Menu")
        option, table = choose_option(table)

    data_manager.write_table_to_file('inventory/inventory.csv', table)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    title_list = ["id", "name", "manufacturer", "purchase date", "durability"]

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

    list_labels = ["name", "manufacturer", "purchase date", "durability"]

    data_to_add = ui.get_inputs(list_labels, "Please provide name, manufacturer, purchase date, durability")

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
        questions = ['Name', 'Manufacturer', 'Purchase date', 'Durability']
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

# the question: Which items have not exceeded their durability yet?
# return type: list of lists (the inner list contains the whole row with their actual data types)
#
# @table: list of lists
def get_available_items(table):
    """
    Check if durability of items are not exceed.

    Args:
        table: list of lists with data

    Returns:
        list of lists: inner list contain all information that are given in data structure (on top of module in comment)
    """
    CURRENT_YEAR = 2017
    list_items = []

    for index in range(len(table)):
        try:
            purchase_date = int(table[index][3])
            years_from_purchase = CURRENT_YEAR - purchase_date
            if years_from_purchase <= int(table[index][4]):
                list_items.append([table[index][0], table[index][1], table[index][2],
                                  int(table[index][3]), int(table[index][4])])
        except IndexError:
            pass

    return list_items


def creat_list_manufacturers(table):
    """
    Creat list of manufactures years based on data read from .csv file

    Args:
        table: list of lists with data

    Returns:
        list of unique strings
    """
    uniqe_manufacturers = []

    for i in range(len(table)):
        try:
            if table[i][2] not in uniqe_manufacturers:
                uniqe_manufacturers.append(table[i][2])
        except IndexError:
            pass

    return uniqe_manufacturers


# the question: What are the average durability itmes for each manufacturer?
# return type: a dictionary with this structure: { [manufacturer] : [avg] }
#
# @table: list of lists
def get_average_durability_by_manufacturers(table):

    avrg_durability = []
    manufacturers_dict = {}
    items = 0

    uniqe_manufacturers = common.create_list_of_unique(table, 2)

    for j in range(len(uniqe_manufacturers)):
        durability = 0
        items = 0

        try:
            for i in range(len(table)):
                if uniqe_manufacturers[j] == table[i][2]:
                    items += 1
                    durability += int(table[i][4])
        except (IndexError, ValueError):
            pass

        try:
            average = durability / items
        except ZeroDivisionError as err:
            ui.print_error_message(err)

        try:
            if uniqe_manufacturers[j]:
                avrg_durability.append((uniqe_manufacturers[j], average))
            raise ValueError
        except ValueError:
            pass

    for item in avrg_durability:
        manufacturers_dict[item[0]] = item[1]

    return manufacturers_dict
