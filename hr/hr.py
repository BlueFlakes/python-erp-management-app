# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: string
# birth_date: number (year)


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
        result = get_oldest_person(table)
        ui.print_result(result, "The oldest people are: ")
    elif option == "6":
        result = get_persons_closest_to_average(table)
        ui.print_result(result, "The closest people to average age are: ")

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
                    "Who is the oldest person?", "Who is the closest to the average age ?"]

    table = data_manager.get_table_from_file("hr/persons.csv")

    option = float("inf")
    while not option == "0":
        ui.print_menu("Human resources manager", options_list, "Exit to menu")
        option, table = choose_option(table)

    data_manager.write_table_to_file("hr/persons.csv", table)


def show_table(table):
    """
    Calls function which prints the table.

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    title_list = ["id", "name", "year"]
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
    data_to_add = ui.get_inputs(["Name", "Birth year"], "Please provide information")

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
        # ---------------------------------------------------------------------#
        list_options = ['Modify record']
        questions = ['Name', 'Year']
        answers_types = [str, int]
        is_alpha = [True, False]
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

# the question: Who is the oldest person ?
# return type: list of strings (name or names if there are two more with the same value)
def get_oldest_person(table):
    """
    Gets the oldest people from the table.

    Args:
        table: list of lists with data

    Returns:
        List with names (strings) of the oldest people
    """

    years_list = common.get_values_from_column(table, 2, "int")
    sorted_years_list = common.insertion_sorting(years_list)
    oldest_people = [table[i][1] for i in range(len(table)) if int(table[i][2]) == sorted_years_list[0]]

    return oldest_people


# the question: Who is the closest to the average age ?
# return type: list of strings (name or names if there are two more with the same value)
def get_persons_closest_to_average(table):
    """
    Counts average birth year of all people from the table.
    Gets person (or people) who were born closest to the average birth year.

    Args:
        table: list of lists with data

    Returns:
        List with names (strings) of people closest to the average birth year
    """

    years_list = common.get_values_from_column(table, 2, "int")
    average_year = common.get_average_year(years_list)

    lowest_difference = float("inf")

    for i in range(len(table)):
        difference = (int(table[i][2]) - average_year)
        if abs(difference) < lowest_difference:
            lowest_difference = abs(difference)
            closest_value = table[i][2]

    closest_people = [table[i][1] for i in range(len(table)) if table[i][2] == closest_value]

    return closest_people
