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
    # from hr module
    sum_of_years = 0
    for year in years_list:
        sum_of_years += year

    average_year = sum_of_years / len(years_list)

    return average_year


def get_values_from_column(table, column_number, items_types='str'):
    temp_storage = []

    for i in range(len(table[0])):
        temp_storage.append([])

        for j in range(len(table)):
            temp_storage[i].append(table[j][i])

    if items_types == 'int':
        temp_storage = [int(number) for number in temp_storage]

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


def remove_record(table, id_):
    id_storage = get_values_from_column(table, 0)

    records_amount = len(id_storage)
    rows_to_del = None

    for i in range(records_amount):
        if id_ == id_storage[i]:
            rows_to_del = i
            break

    if rows_to_del:
        del table[i]
        successful = True

    else:
        successful = False

    return table, successful


#
