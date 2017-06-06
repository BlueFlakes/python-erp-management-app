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
    print(table)

    lol = input("x")
    if lol == "x":
        get_oldest_person(table)
    elif lol == "y":
        get_persons_closest_to_average(table)


def show_table(table):
    """
    Display a table

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """

    # your code

    pass


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
    sorted_years_list = insertion_sort(years_list)
    oldest_people = [table[i][1] for i in range(len(table)) if int(table[i][2]) == sorted_years_list[0]]

    print(oldest_people)
    return oldest_people


# the question: Who is the closest to the average age ?
# return type: list of strings (name or names if there are two more with the same value)
def get_persons_closest_to_average(table):

    years_list = [int(table[i][2]) for i in range(len(table))]
    average_year = get_average_year(years_list)

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


def insertion_sort(numbers):
    """
    Parameters
    ----------
    numbers : list of int

    Returns
    -------
    list of int
        Sorted numbers list.
    """

    for i in range(1, len(numbers)):
        value = numbers[i]
        previous_index = i - 1
        while (previous_index >= 0) and (numbers[previous_index] > value):
            numbers[previous_index + 1] = numbers[previous_index]
            previous_index = previous_index - 1
        numbers[previous_index + 1] = value

    return numbers


def get_average_year(years_list):
    sum_of_years = 0
    for year in years_list:
        sum_of_years += year

    average_year = sum_of_years / len(years_list)

    return average_year

