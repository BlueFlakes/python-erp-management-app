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
