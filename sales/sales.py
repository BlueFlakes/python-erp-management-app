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
    Display a table

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

    id_ = common.generate_random(table)

    list_labels = ["title", "price", "month", "day", "year"]

    data_to_add = ui.get_inputs(list_labels, "Please provide title, price, month, day, year")

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


def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table: list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        table with updated record
    """

    # your code

    return table


def get_first_alphabetically(lowest_price_games):
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

    prices_list = common.get_values_from_column(table, 2, "int")
    sorted_prices_list = common.insertion_sorting(prices_list)
    lowest_price_games = [table[i][1] for i in range(len(table)) if int(table[i][2]) == sorted_prices_list[0]]

    first_alphabetically = get_first_alphabetically(lowest_price_games)

    for i in range(len(table)):
        if first_alphabetically == table[i][1]:
            result = table[i][0]

    return result


# the question: Which items are sold between two given dates ? (from_date < sale_date < to_date)
# return type: list of lists (the filtered table)
def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):

    table = [x[:] for x in table]

    dates = [year_from, month_from, day_from, year_to, month_to, day_to]
    dates, date_from, date_to = get_dates(dates)

    dates_of_games = get_dates_of_games(table)

    games_between_dates = get_games_between_dates(dates_of_games, date_from, date_to)

    sold_games = get_sold_games(dates_of_games, games_between_dates, table)

    return sold_games


def check_correctness_of_arguments(dates):
    for i in range(len(dates)):
        dates[i] = str(dates[i])
        if len(dates[i]) < 2:
            dates[i] = "0" + dates[i]

    return dates


def get_dates_of_games(table):
    dates_of_games = []
    for item in table:
        for i in range(3, 5):
            if len(item[i]) < 2:
                item[i] = "0" + item[i]

        date = item[5] + item[3] + item[4]
        dates_of_games.append(date)

    return dates_of_games


def get_games_between_dates(dates_of_games, date_from, date_to):
    games_between_given_dates = []
    for number in dates_of_games:
        if int(number) > int(date_from) and int(number) < int(date_to):
            games_between_given_dates.append(number)

    return games_between_given_dates


def get_dates(dates):
    dates = check_correctness_of_arguments(dates)

    date_from = dates[0] + dates[1] + dates[2]
    date_to = dates[3] + dates[4] + dates[5]

    return dates, date_from, date_to


def get_sold_games(dates_of_games, games_between_dates, table):
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
