# implement commonly used functions here

import random


# generate and return a unique and random string
# other expectation:
# - at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter
# - it must be unique in the list
#
# @table: list of lists
# @generated: string - randomly generated string (unique in the @table)
def generate_random(table):
    """
    Generates random and unique string. Used for id/key generation.

    Args:
        table: list containing keys. Generated string should be different then all of them

    Returns:
        Random and unique string
    """

    generated = ''
    unique_id = False

    while unique_id is False:
        unique_id = True
        for times in range(0, 2):
            chosen_number = random.randint(97, 122)
            generated += chr(chosen_number)

            chosen_number = random.randint(65, 90)
            generated += chr(chosen_number)

            chosen_number = random.randint(33, 47)
            generated += chr(chosen_number)

            chosen_number = random.randint(0, 9)
            generated += str(chosen_number)

        generated = ''.join(random.sample(generated, len(generated)))

        for i in range(len(table)):
            if generated in table[i]:
                unique_id = False

    return generated


def insertion_sorting(numbers):
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
    # from hr module
    sum_of_years = 0
    for year in years_list:
        sum_of_years += year

    average_year = sum_of_years / len(years_list)

    return average_year


def get_values_from_column(table, column_number, items_types='str'):
    temp_storage = []
    digits = [i for i in range(0,10)]

    for i in range(len(table[0])):
        temp_storage.append([])

        for j in range(len(table)):
            temp_storage[i].append(table[j][i])

    if items_types == 'int':
        try:
            temp_storage[column_number] = [int(number) for number in temp_storage[column_number]]

        except:
            raise ValueError('Conversion is impossible, wrong data types have been provided.')

    return temp_storage[column_number]


def get_max(array):

    if type(array[0]) == str:
        longest = len(array[0])
    elif type(array[0]) == int:
        longest = array[0]

    for item in array:
        if type(item) == str:
            if len(item) > longest:
                longest = len(item)

        elif type(item) == int:
            if item > longest:
                longest = item

    return longest


def find_longest_string_in_list(list_of_names, return_row_number=False):
    rows_collector = []
    longest = get_max(list_of_names)

    for i in range(len(list_of_names)):
        if len(list_of_names[i]) == longest:
            rows_collector.append(i)

    if return_row_number == True:
        longest = [longest, rows_collector]

    return longest

def get_item_row(table, item):
    row_number = None

    for i in range(len(table)):
        if item == table[i]:
            row_number = i
            break

    return row_number


def remove_record(table, id_):
    id_storage = get_values_from_column(table, 0)

    records_amount = len(id_storage)
    rows_to_del = get_item_row(id_storage, id_)

    if rows_to_del != None:
        del table[rows_to_del]
        successful = True

    else:
        successful = False

    return table, successful


def create_list_of_unique(table, column_in_file):
    """
    Creat list of unique based on data read from .csv file
    and index of row we are intersted in.

    Args:
        table: list of lists with data
        column_in_file: int that is proper index in row in data

    Returns:
        list of unique strings
    """
    list_of_unique = []

    for i in range(len(table)):
        try:
            if table[i][column_in_file] not in list_of_unique:
                list_of_unique.append(table[i][column_in_file])
        except IndexError:
            pass

    return list_of_unique

#
