# data structure:
# id: string
#     Unique and random generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: string
# birth_date: number (year)


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
        add(table)
    elif option == "3":
        # id_ = get_inputs(list_labels, title)
        remove(table, id_)
    elif option == "4":
        # id_ = get_inputs(list_labels, title)
        update(table, id_)
    elif option == "5":
        which_year_max(table)
    elif option == "6":
        avg_amount(table, year)
        # get_inputs(list_labels, title)


def start_module():
    """
    Starts this module and displays its menu.
    User can access default special features from here.
    User can go back to main menu from here.

    Returns:
        None
    """

    os.system("clear")

    options_list = ["Show table", "Add to table", "Remove from table", "Update table",
                    "Who is the oldest person?", "Who is the closest to the average age ?"]
    ui.print_menu("Human resources: ", options_list, "Exit to menu")

    table = data_manager.get_table_from_file("hr/persons.csv")

    choose_option(table)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """
    # chane list content
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

    # your code

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


# special functions:
# ------------------

# the question: Who is the oldest person ?
# return type: list of strings (name or names if there are two more with the same value)
def get_oldest_person(table):

    years_list = [int(table[i][2]) for i in range(len(table))]
    sorted_years_list = common.insertion_sort(years_list)
    oldest_people = [table[i][1] for i in range(len(table)) if int(table[i][2]) == sorted_years_list[0]]

    print(oldest_people)
    return oldest_people


# the question: Who is the closest to the average age ?
# return type: list of strings (name or names if there are two more with the same value)
def get_persons_closest_to_average(table):

    years_list = [int(table[i][2]) for i in range(len(table))]
    average_year = common.get_average_year(years_list)

    print(average_year)

    lowest_difference = float("inf")
    print(lowest_difference)
    for i in range(len(table)):
        difference = (int(table[i][2]) - average_year)
        if abs(difference) < lowest_difference:
            lowest_difference = abs(difference)
            closest_value = table[i][2]

    closest_people = [table[i][1] for i in range(len(table)) if table[i][2] == closest_value]
    print(closest_people)
    return closest_people


