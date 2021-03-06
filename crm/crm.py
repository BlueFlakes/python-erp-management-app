# data structure:
# id: string
#     Unique and randomly generated (at least 2 special char()expect: ';'), 2 number, 2 lower and 2 upper case letter)
# name: string
# email: string
# subscribed: boolean (Is she/he subscribed to the newsletter? 1/0 = yes/not)


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
        id_ = ui.get_inputs(["Id"], "Please provide record id, which you want to change")[0]
        table = update(table, id_)
    elif option == "5":
        ui.print_result(get_longest_name_id(table), 'The Id of customer with longest name:')
    elif option == "6":
        ui.print_result(get_subscribed_emails(table), 'Subscribers:')

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

    table = data_manager.get_table_from_file('crm/customers.csv')

    list_options = ["Show table", "Add", "Remove", "Update",
                    "Id of customer with longest name", "Customers that have to subscribe newsletter"
                    ]

    option = float("inf")
    while not option == "0":
        ui.print_menu("Customer Relationship Management (CRM)", list_options, "Exit to Menu")
        option, table = choose_option(table)

    data_manager.write_table_to_file('crm/customers.csv', table)


def show_table(table):
    """
    Calls function which prints the table.

    Args:
        table: list of lists to be displayed.

    Returns:
        None
    """
    title_list = ["id", "name", "email", "subscribe newsletter"]
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
        user_input (str or int)
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
    questions = ['Name', 'E-mail', 'Subs newsletter']
    answers_types = [str, str, int]
    is_alpha = [False, False, False]

    if update_row:
        list_options = ['Modify record']
    else:
        list_options = ['Add record']

    ui.print_menu('Possible orders:', list_options, "Exit to Menu")
    user_input = ui.get_inputs([''], '')[0]

    if user_input == '1':
        user_data = get_data_from_user(questions, answers_types, id_storage, id_, is_alpha)

        # newsletter subscription value, it's similar to bool True/False
        if user_data[2] != '0':
            user_data[2] = '1'
        else:
            user_data[2] = '0'

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

# special functions:
# ------------------


def find_longest_string_in_list(list_of_names, return_row_number=False):
    rows_collector = []
    longest = common.get_max(list_of_names)

    for i in range(len(list_of_names)):
        if len(list_of_names[i]) == longest:
            rows_collector.append(i)

    if return_row_number is True:
        longest = [longest, rows_collector]

    return longest


# the question: What is the id of the customer with the longest name ?
# return type: string (id) - if there are more than one longest name, return the first by descending alphabetical order
def get_longest_name_id(table):
    """
    Gets the id of the longest name.
    If there are more than one longest names, sorts the alphabetically
    and gets the first one.

    Args:
        table: list of lists

    Returns:
        string: id of the longest name
    """

    names_data = common.get_values_from_column(table, 1)
    id_data = common.get_values_from_column(table, 0)
    longest_string, rows = find_longest_string_in_list(names_data, True)

    if len(rows) > 1:
        alphabetical_array = []
        for i in range(65, 91):
            alphabetical_array.append([])

        for row_number in rows:
            for alpha in range(65, 91):

                if names_data[row_number][0].upper() == chr(alpha):
                    alphabetical_array[alpha-65].extend([[names_data[row_number], row_number]])

        for first_name in alphabetical_array:
            if first_name:
                id_to_return = id_data[first_name[0][1]]
                break

    else:
        id_to_return = id_data[rows[0]]

    return id_to_return


# the question: Which customers has subscribed to the newsletter?
# return type: list of strings (where string is like email+separator+name, separator=";")
def get_subscribed_emails(table):
    """
    Gets the list of strings with emails of people,
    who have subscribed to the newsletter.

    Args:
        table: lsit of lists

    Returns:
        List of strings: email + name
    """

    names_data = common.get_values_from_column(table, 1)
    e_mail_data = common.get_values_from_column(table, 2)
    subs_info = common.get_values_from_column(table, 3)
    records_amount = len(table)
    row_number_of_sub_customers = []
    subscription_score = []

    for i in range(records_amount):
        if int(subs_info[i]) > 0:
            row_number_of_sub_customers.append(i)

    for i in row_number_of_sub_customers:
        subscription_score.append(e_mail_data[i]+';'+names_data[i])

    return subscription_score
