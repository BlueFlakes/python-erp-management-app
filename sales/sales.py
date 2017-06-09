# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# title: string
# price: number (the actual sale price in $)
# month: number
# day: number
# year: number
# month,year and day combined gives the date the sale was made

# importing everything you need
import os
# User interface module
import ui
# data manager module
import data_manager
# common module
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
        result = get_lowest_price_item_id(table)
        ui.print_result(result, "The id of the item that was sold for the lowest price is")
    elif option == "6":
        answers_list = ui.get_inputs(["Month from", "Day from",
                                      "Year from", "Month to",
                                      "Day to", "Year to"], "Please provide dates from and to")
        result = get_items_sold_between(table, answers_list[0], answers_list[1], answers_list[2],
                                        answers_list[3], answers_list[4], answers_list[5])
        ui.print_result(result, "Items sold between those dates")

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

    table = data_manager.get_table_from_file('sales/sales_test.csv')

    list_options = ["Show table", "Add", "Remove", "Update",
                    "Id of item sold with the lowest price", "Items sold between dates"
                    ]

    option = float("inf")
    while not option == "0":
        ui.print_menu("Sales manager", list_options, "Exit to Menu")
        option, table = choose_option(table)

    data_manager.write_table_to_file('sales/sales.csv', table)


def show_table(table):
    """
    Calls function which prints the table.

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    # maybe "month", "day", "year" need to be combinated to date right now
    title_list = ["id", "title", "price", "month", "day", "year"]

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
        user_input (int or str)
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


def check_additional_specific_conditions(i, user_input):
    """
    get_correct_data_types function change the type of input to
    it's expected type.

    Args:
        param1: i (int) it is stepping progress of iterator
        param2: user_input (str or int)

    Returns:
        user_input (str or int or None)
    """
    if i == 2:
        if type(user_input) == int:
            if user_input > 12 or user_input < 1:
                user_input = None
                ui.print_error_message("Wrong value provided.")

    elif i == 3:
        if type(user_input) == int:
            if user_input > 31 or user_input < 1:
                user_input = None
                ui.print_error_message("Wrong value provided.")

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
            user_input = check_additional_specific_conditions(i, user_input)

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
    questions = ['Title', 'Price', 'Month', 'Day', 'Year']
    answers_types = [str, int, int, int, int]
    is_alpha = [False, False, False, False, False]

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


def get_first_alphabetically(lowest_price_games):
    """
    Sorts the list alphabetically using insertion sort,
    then returns first element of a sorted list.

    Args:
        list with strings

    Returns:
        String
    """

    lower_cased_list = [item.lower() for item in lowest_price_games]

    sorted_alph = common.insertion_sorting(lower_cased_list[:])

    for i in range(len(lower_cased_list)):
        if sorted_alph[0] == lower_cased_list[i]:
            index = i

    return lowest_price_games[index]


# special functions:
# ------------------

# the question: What is the id of the item that was sold for the lowest price ?
# return type: string (id)
# if there are more than one with the lowest price, return the first by descending alphabetical order
def get_lowest_price_item_id(table):
    """
    Gets id of item with the lowest price.
    If there are two items with the same, lowest price, returns first alphabetically.

    Args:
        table: list of lists with data

    Returns:
        String
    """

    prices_list = common.get_values_from_column(table, 2, "int")
    sorted_prices_list = common.insertion_sorting(prices_list)
    lowest_price_games = [table[i][1] for i in range(len(table)) if int(table[i][2]) == sorted_prices_list[0]]

    first_alphabetically = get_first_alphabetically(lowest_price_games)

    for i in range(len(table)):
        if first_alphabetically == table[i][1]:
            item = table[i][0]

    return item


# the question: Which items are sold between two given dates ? (from_date < sale_date < to_date)
# return type: list of lists (the filtered table)
def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):
    """
    Gets items sold between given dates.

    Args:
        table: list of lists with data
        month_from: string (input from user)
        day_from: string (input from user)
        year_from: string (input from user)
        month_to: string (input from user)
        month_to: string (input from user)
        month_to: string (input from user)

    Returns:
        Filtered table with games sold only between given dates.
    """

    table = [x[:] for x in table]

    dates = [year_from, month_from, day_from, year_to, month_to, day_to]
    dates, date_from, date_to = get_dates(dates)

    dates_of_games = get_dates_of_games(table)

    games_between_dates = get_games_between_dates(dates_of_games, date_from, date_to)

    sold_games = get_sold_games(dates_of_games, games_between_dates, table)

    return sold_games


def check_correctness_of_arguments(dates):
    """
    Makes strings from all the dates given (test.py gives int as an arg)
    Makes days and months with correct form: i. e. 03 instead of 3.

    Args:
        List with strings

    Returns:
        Corrected list.
    """

    for i in range(len(dates)):
        dates[i] = str(dates[i])
        if len(dates[i]) < 2:
            dates[i] = "0" + dates[i]

    return dates


def get_dates_of_games(table):
    """
    Merges years, months and days from every element of the table.
    Makes list with all merged dates.

    Args:
        List of lists

    Returns:
        List of strings
    """

    dates_of_games = []
    for item in table:
        for i in range(3, 5):
            if len(item[i]) < 2:
                item[i] = "0" + item[i]

        date = item[5] + item[3] + item[4]
        dates_of_games.append(date)

    return dates_of_games


def get_games_between_dates(dates_of_games, date_from, date_to):
    """
    Gets all the games which were sold between given dates.

    Args:
        List of strings: merged dates of all games
        String: beginning date
        String: ending date

    Returns:
        List of merged dates
    """

    games_between_given_dates = []
    for number in dates_of_games:
        if int(number) > int(date_from) and int(number) < int(date_to):
            games_between_given_dates.append(number)

    return games_between_given_dates


def get_dates(dates):
    """
    Makes variables and calls inner functions.

    Args:
        List of strings: merged dates of all games
        String: beginning date
        String: ending date

    Returns:
        List with dates
        String with begin date
        String with end date
    """

    dates = check_correctness_of_arguments(dates)

    date_from = dates[0] + dates[1] + dates[2]
    date_to = dates[3] + dates[4] + dates[5]

    return dates, date_from, date_to


def get_sold_games(dates_of_games, games_between_dates, table):
    """
    Filters the table to include only games which were
    sold between given dates.
    Converts numbers in filtered table from string to int.

    Args:
        List of strings: merged dates of all games
        List of strings: merged dates which are between given dates only
        Table: list of lists

    Returns:
        Filtered table
    """

    sold_games = []
    for i in range(len(dates_of_games)):
        for j in range(len(games_between_dates)):
            if dates_of_games[i] == games_between_dates[j]:
                sold_games.append(table[i])

    for item in sold_games:
        item[2] = int(item[2])
        item[3] = int(item[3])
        item[4] = int(item[4])
        item[5] = int(item[5])

    return sold_games
