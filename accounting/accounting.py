# data structure:
# id: string
#     Unique and randomly generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# month: number
# day: number
# year: number
# type: string (in = income, out = outcome)
# amount: number (dollar)


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
        which_year_max(table)
    elif option == "6":
        year = ui.get_inputs(["Year"], "Please provide year for which you want to see profit")[0]
        avg_amount(table, year)

    return option, table


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """

    table = data_manager.get_table_from_file('accounting/items.csv')

    list_options = ["Show table", "Add", "Remove", "Update",
                    "Year with the hightest profit", "Avarege profit in year"
                    ]

    option = float("inf")
    while not option == "0":
        ui.print_menu("Accounting manager", list_options, "Exit to Menu")
        option, table = choose_option(table)

    data_manager.write_table_to_file('accounting/items.csv', table)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    title_list = ["id", "month", "day", "year", "incom / outcome", "amount (dollars)"]

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

    list_labels = ["month", "day", "year", "incom / outcome", "amount (dollars)"]

    data_to_add = ui.get_inputs(list_labels, "Please provide month, day, year, incom / outcome, amount (dollars)")

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

    # your code

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


def creat_list_uniqe_years(table):
    uniqe_year = []

    for i in range(len(table)):
        if table[i][3] not in uniqe_year:
            uniqe_year.append(table[i][3])

    return uniqe_year


def make_list_profit_year(uniqe_year, table):
    profit_list = []

    for j in range(len(uniqe_year)):
        profit = 0
        for i in range(len(table)):
            if uniqe_year[j] == table[i][3]:
                if table[i][4] == "in":
                    profit += int(table[i][5])
                elif table[i][4] == "out":
                    profit -= int(table[i][5])
        profit_list.append((profit, uniqe_year[j]))

    return profit_list


# special functions:
# ------------------

# the question: Which year has the highest profit? (profit=in-out)
# return the answer (number)
def which_year_max(table):

    uniqe_year = creat_list_uniqe_years(table)
    profit_list = make_list_profit_year(uniqe_year, table)

    year_highest_profit = 0
    for i in range(1, len(profit_list)):
        if profit_list[i][0] > profit_list[i - 1][0]:
            year_highest_profit = profit_list[i]
        else:
            year_highest_profit = profit_list[i - 1]

    year_highest_profit = int(year_highest_profit[1])

    return year_highest_profit


# the question: What is the average (per item) profit in a given year? [(profit)/(items count) ]
# return the answer (number)
def avg_amount(table, year):

    profit = 0
    items = 0

    for i in range(len(table)):
        if year == table[i][3]:
            items += 1
            if table[i][4] == "in":
                profit += int(table[i][5])
            elif table[i][4] == "out":
                profit -= int(table[i][5])

    avrg_profit_per_item = profit / items

    return avrg_profit_per_item
