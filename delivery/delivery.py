# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: string
# city: string
# delivery hours: int


# Importing everything you need
import os
# User interface module
import ui
# Data manager module
import data_manager
# Common module
import common


def choose_option(table):
    """
    Asks user for input and basing on this calls proper function

    Args:
        table: list of lists with data

    Returns:
        Table with a new record
        String with user's input
    """

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
        result = get_most_common_city(table)
        ui.print_result(result, "Most common delivers are to city: ")
    elif option == "6":
        result = get_average_delivery_time(table)
        ui.print_result(result, "Average delivery time is: ")

    return option, table


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.
    File is being overwritten from here.

    Returns:
        None
    """

    options_list = ["Show table", "Add to table", "Remove from table", "Update table",
                    "Where goes deliveries most of times?", "What is the average delivery time?"]

    table = data_manager.get_table_from_file("delivery/delivery.csv")

    option = float("inf")
    while not option == "0":
        ui.print_menu("Delivery Menager", options_list, "Exit to menu")
        option, table = choose_option(table)

    data_manager.write_table_to_file("delivery/delivery.csv", table)


def show_table(table):
    """
    Calls function which prints the table.

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    title_list = ["id", "name", "city", "hours"]
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
    data_to_add = ui.get_inputs(["Name", "City", "Hours"], "Please provide delivery information")

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
        # ---------------------------------------------------------------------#
            # Other differences while asking for data here

        # ---------------------------------------------------------------------#
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
        # ---------------------------------------------------------------------#
        list_options = ['Modify record']
        questions = ['Name', 'City', 'Hours']
        answers_types = [str, str, int]
        is_alpha = [True, True, False]
        # --------------------------------------------------------------------#

        ui.print_menu('Possible orders:', list_options, "Exit to Menu")
        user_input = ui.get_inputs([''], '')[0]
        if user_input == '1':
            table, row = get_data_for_update(table, questions, answers_types, id_storage, id_, is_alpha)

        # Individual differences after getting data HERE \/

        # ---------------------------------------------------------------------#
    else:
        ui.print_error_message('This option does not exist.')

    return table


# special functions:
# ------------------

def get_most_common_city(table):
    """
    Gets a most common city and returns it as an element of a list.
    If there are cities which appear same times returns a list with all of them.

    Args:
        table: list of lists

    Returns:
        list of cities
    """

    cities_list = common.get_values_from_column(table, 2, items_types='str')
    cities_appearance = get_cities_appearence(cities_list)

    highest = 0
    most_common_cities = []
    for city, delivers in cities_appearance.items():
        if delivers > highest:
            highest = delivers
            common_city = city
    most_common_cities.append(common_city)

    most_common_cities = check_if_equal_appearance(cities_appearance, most_common_cities, highest)

    return most_common_cities


def get_cities_appearence(cities_list):
    """
    Counts how many times city appears.

    Args:
        cities_list: list

    Returns:
        dict with structure city:times_of_appearence
    """

    cities_appearance = {}

    for item in cities_list:
        if item in cities_appearance.keys():
            cities_appearance[item] += 1
        else:
            cities_appearance[item] = 1

    return cities_appearance


def check_if_equal_appearance(cities_appearance, most_common_cities, highest):
    """
    Checks if there cities which appear equal times as the most common city.

    Args:
        cities_appearance: dict with structure city:times_of_appearence
        most_common_cities: list with one string
        highest: int

    Returns:
        most_common_cities: list with one or more strings
    """

    for city, delivers in cities_appearance.items():
        if delivers == highest:
            if city not in most_common_cities:
                most_common_cities.append(city)

    return most_common_cities


def get_average_delivery_time(table):
    delivery_times = common.get_values_from_column(table, 3, items_types='int')

    delivery_time = common.get_average_value(delivery_times)
    delivery_time = str(delivery_time)

    if len(delivery_time) > 4:
        delivery_time = delivery_time[0:4]

    delivery_time = delivery_time + " hours"

    return delivery_time
