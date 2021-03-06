def check_lists_length(table, title_list):
    """
    Check the length of nested list in table and compare it to the length of
    title_list.

    Args:
        param1: table (list) contains lists
        param2: title_list

    Returns:
        is_length_equal (bool)

    """
    start_size = len(table[0])

    for nested_list in table:
        if len(nested_list) != start_size or len(title_list) != start_size:
            is_length_equal = False
        else:
            is_length_equal = True

    return is_length_equal


def convert_each_string_to_integer(table, temp):
    """
    This function covert every string to it's length as integer

    Args:
        param1: table (list) contains lists
        param2: temp records amount of nested list in table

    Returns:
        table (list) contains lists

    """
    # get length of each string
    table = [len(column) for row in table for column in row]
    # pack every column length into lists by rows
    table = [table[i-temp+1:i+1] for i in range(len(table)) if (i+1) % temp == 0]

    return table


def check_table_for_type_bugs(table):
    """
    Iterate through the list and check for invalid data types

    Args:
        param1: table (list) contains lists

    Returns:
        broken_data (bool)

    """
    broken_data = False

    for row in table:
        if type(row) == list and broken_data is False:
            for column in row:
                if type(column) == str:
                    broken_data = False

                else:
                    broken_data = True
                    break

        else:
            broken_data = True
            break

    return broken_data


def check_title_list_for_type_bugs(title_list):
    """
    Iterate through the list and check for invalid data types

    Args:
        param1: title_list (list) contains str

    Returns:
        broken_data (bool)

    """
    for record in title_list:
        if type(record) == str:
            broken_data = False

        else:
            broken_data = True

    return broken_data


def check_data_for_bugs(table, title_list):
    """
    Analysing data for unexpected errors

    Args:
        param1: table (list) contains list
        param2: title_list (list) contains str

    Example:
        Operated errors:
            difference between items amount in every row
            difference between items amount in row and titles
            data types inside table, table should contain list of lists
            data types inside title_list, title_list should contain strings

    Returns:
        None. Just raise Error if any bug appear

    """
    if (not table) or (not title_list):
        raise ValueError('Not enough data delivered.')

    is_data_in_table_broken = check_table_for_type_bugs(table)
    is_data_in_title_list_broken = check_title_list_for_type_bugs(title_list)
    if is_data_in_table_broken or is_data_in_title_list_broken:
        raise TypeError('Wrong types are stored in data.')

    lists_length_equal = check_lists_length(table, title_list)
    if not lists_length_equal:
        raise ValueError('Wrong amount of data is stored in table or title_list.')


def highest_numbers_in_collections(data):
    """
    This func finding highest values in collections and return it

    Args:
        param1: data (list)

    Returns:
        highest_value (int)

    """
    temp_storage = []

    for record in data:

        highest_number = record[0]

        for column in record:
            if column > highest_number:
                highest_number = column

        temp_storage.append(highest_number)

    return temp_storage


def get_highest_value_per_column(sizes, records_amount_in_nested_list):
    """
    This func collect the values in each list by columns

    Args:
        param1: table (list) contains list
        param2: title_list (list) contains str

    Returns:
        highest_value (int)

    """
    temp_storage = []

    # create list for every column
    for i in range(records_amount_in_nested_list):
        temp_storage.append([])

    # make collections by columns
    for record in sizes:
        temp_storage[record[1]].append(record[0])

    highest_values = highest_numbers_in_collections(temp_storage)

    return highest_values


def get_columns_sizes(table, title_list):
    """
    This function collect sizes width of each row and then find the longest
    value of each column

    Args:
        param1: table (list) contains list
        param2: title_list (list) contains str

    Returns:
        columns_sizes (list) contains int

    """
    # wyciągnij filtry do głównego ciała i stwórz flage

    columns_sizes = []
    records_amount_in_nested_list = len(table[0])
    table = convert_each_string_to_integer(table, records_amount_in_nested_list)

    # find longest strings in each nested list
    if len(table) > 1:
        for x in range(len(table)):
            temp_value = table[x][0]
            index = 0

            for y in range(records_amount_in_nested_list):
                temp_value, index = table[x][y], y
                columns_sizes.append([temp_value, index])

        columns_sizes = get_highest_value_per_column(columns_sizes, records_amount_in_nested_list)
    else:
        # get rid of nested list if just one list is inside table
        columns_sizes = [record[i] for record in table for i in range(len(record))]

    temp_storage = []

    for i in range(len(columns_sizes)):
        if columns_sizes[i] > len(title_list[i]):
            temp_storage.append(columns_sizes[i])
        else:
            temp_storage.append(len(title_list[i]))

    columns_sizes = temp_storage

    return columns_sizes


def get_rid_of_empty_columns(table, title_list):
    """
    This function clean off board from empty columns

    Args:
        param1: table (list) contains list
        param2: title_list (list) contains str

    Returns:
        table (list) contains lists
        title_list (list) contains str

    """

    temp_storage = []
    # Find empty column index
    table_index_to_del = [i for row in table for i in range(len(row)) if len(row[i]) == 0]
    title_index_to_del = set([i for i in range(len(title_list)) if len(title_list[i]) == 0])

    # clean off repetitive values
    for index in table_index_to_del:
        if index not in temp_storage:
            temp_storage.append(index)

    # change to data types to set and compare
    table_index_to_del = set(temp_storage)
    common_part = list(title_index_to_del & table_index_to_del)
    common_part = common_part[::-1]

    # Delete part of common empty columns
    for record in common_part:
        for j in range(len(table)):
            del table[j][record]

        del title_list[record]

    return table, title_list


def add_free_space_on_the_sides(columns_width):
    """
    This function calculate the amount of columns in board

    Args:
        param1: columns_width (list) contains int

    Returns:
        columns_width (int)

    """
    # added value must be ODD and higher or equal than 3
    columns_width = [column_length+3 for column_length in columns_width]

    return columns_width


def calculate_height(table, record_height):
    """
    This function calculate the amount of rows in board

    Args:
        param1: table (list) contains lists
        param2: record_height (int)

    Returns:
        rows_amount (int)

    """
    rows_amount = (len(table) * record_height) + 1 + record_height

    return rows_amount


def sum_numbers(list_of_numbers):
    """
    This function sum the numbers which are provided

    Args:
        param1: list_of_numbers (list) contains int

    Returns:
        sum_score (int)

    """
    sum_score = 0

    for number in list_of_numbers:
        sum_score += number

    return sum_score


def create_board(height, width, record_height, separators):
    """
    This function insert values into rows.

    Args:
        param1: height (int)
        param2: width (int)
        param3: record_height (int)
        param4: separators (list) contains int

    Returns:
        board: list of nested lists

    """
    board = []
    height = height
    width = width+1

    for y in range(height):
        temp_storage = []

        for x in range(width):
            if y == 0 or y == (height-1):
                temp_storage.append('-')
            elif x == 0 or x in separators:
                temp_storage.append('|')
            elif (x > 0 and x < (width-1)) and y % record_height == 0:
                temp_storage.append('-')
            else:
                temp_storage.append(' ')

        board.append(temp_storage)

    return board


def print_board(board):

    for row in board:
        for column in row:
            print(column, end='')

        print()


def insert_title(board, title_list, columns_width, column_separators):
    """
    This function insert values into rows.

    Args:
        param1: board (list) contains lists,
        param2: title_list (list) contains str,
        param3: columns_width (list) contains int
        param4: column_separators (list) contains int

    Example:
        difference between columns_width and column_separators:
            columns_separators is the stepping sum through columns_width:

            columns_width = [5, 9, 12]
            column_separators = [5, 14, 26]

    Returns:
        board: list of nested lists

    """
    for i in range(len(title_list)):
        # start_point calculationg the X in XY dimension
        start_point = int((columns_width[i]-len(title_list[i]))/2) + column_separators[i] + 1

        for j in range(len(title_list[i])):
            # iterate throught string and insert letter by letter
            board[2][start_point+j] = title_list[i][j]

    return board


def insert_to_table(board, table, columns_width, column_separators, record_height):
    """
    This function insert values into board rows.

    Args:
        param1: board (list) contains lists,
        param2: table (list) contains lists,
        param3: columns_width (list) contains int
        param4: column_separators (list) contains int
        param5: record_height (int)

    Example:
        difference between columns_width and column_separators:
            columns_separators is the stepping sum through columns_width:

            columns_width = [5, 9, 12]
            column_separators = [5, 14, 26]

    Returns:
        board: list of nested lists

    """
    next_row = 0

    for nested_list in table:
        next_row += record_height

        for i in range(len(nested_list)):
            # start_point calculationg the X in XY dimension
            start_point = int((columns_width[i] - len(nested_list[i]))/2) + column_separators[i] + 1

            for j in range(len(nested_list[i])):
                # iterate throught string and insert letter by letter
                board[2+next_row][j+start_point] = nested_list[i][j]

    return board


def insert_data_to_rows(board, table, title_list, columns_width, column_separators, record_height):
    """This function modify corners, it's is such easyer way to insert values
    in corners because they got constant index in table.
    like [0][0] is always north-west corner in two dimensional table

    Args:
        param1: board (list) contains lists

    Returns:
        board: list of nested lists

    """
    columns_width = [number-1 for number in columns_width]
    column_separators.insert(0, 0)
    del column_separators[-1]

    board = insert_title(board, title_list, columns_width, column_separators)
    board = insert_to_table(board, table, columns_width, column_separators, record_height)

    return board


def modify_corners(board):
    """This function modify corners, it's is such easyer way to insert values
    in corners because they got constant index in table.
    like [0][0] is always north-west corner in two dimensional table

    Args:
        param1: board (list of nested lists)

    Returns:
        board: list of nested lists

    """
    board[0][0] = '/'
    board[0][-1] = '\\'
    board[-1][0] = '\\'
    board[-1][-1] = '/'

    return board


def print_list_elements(results):
    """Printing result from dictionary data type

    Args:
        results (dict): The first parameter.

    Returns:
        This function doesn't return anything it only prints to console.

    """
    for i in range(len(results)):
        print("{}{}. {}".format('\t', str(i+1), results[i]))


def print_dict_elements(results):
    """
    Printing result from dictionary data type

    Args:
        results (dict): The first parameter.

    Returns:
        This function doesn't return anything it only prints to console.
    """
    for key, value in results.items():
        print('{}{} : {}'.format('\t', key.capitalize(), value))


def print_table(table, title_list):
    """
    Prints table with data. Sample output:
        /-----------------------------------\
        |   id   |      title     |  type   |
        |--------|----------------|---------|
        |   0    | Counter strike |    fps  |
        |--------|----------------|---------|
        |   1    |       fo       |    fps  |
        \-----------------------------------/

    Args:
        table: list of lists - table to display
        title_list: list containing table headers

    Returns:
        This function doesn't return anything it only prints to console.
    """
    RECORD_HEIGHT = 4

    # filtry
    check_data_for_bugs(table, title_list)
    table, title_list = get_rid_of_empty_columns(table, title_list)

    # get sizes
    columns_width = get_columns_sizes(table, title_list)
    columns_width = add_free_space_on_the_sides(columns_width)
    board_width = sum_numbers(columns_width)
    board_height = calculate_height(table, RECORD_HEIGHT)
    column_separators = [sum_numbers(columns_width[:i+1]) for i in range(len(columns_width))]

    # create board
    board = create_board(board_height, board_width, RECORD_HEIGHT, column_separators)

    # insert board
    board = insert_data_to_rows(board, table, title_list, columns_width, column_separators, RECORD_HEIGHT)
    board = modify_corners(board)

    # print board
    print_board(board)


def print_result(result, label):
    """
    Displays results of the special functions.

    Args:
        result: string, list or dictionary - result of the special function
        label: label of the result

    Returns:
        This function doesn't return anything it only prints to console.
    """
    print(label)
    if type(result) == list:
        print_list_elements(result)
    elif type(result) == dict:
        print_dict_elements(result)
    elif type(result) == str:
        print(result)


def print_menu(title, list_options, exit_message):
    """
    Displays a menu. Sample output:
        Main menu:
            (1) Store manager
            (2) Human resources manager
            (3) Inventory manager
            (4) Accounting manager
            (5) Sales manager
            (6) Customer relationship management (CRM)
            (0) Exit program

    Args:
        title (str): menu title
        list_options (list): list of strings - options that will be shown in menu
        exit_message (str): the last option with (0) (example: "Back to main menu")

    Returns:
        This function doesn't return anything it only prints to console.
    """
    print(title)

    for i in range(len(list_options)):
        position_number = "({}) ".format(str(i+1))
        print(1 * '\t' + position_number + list_options[i])

    print(1 * '\t' + "(0) " + exit_message)


def get_inputs(list_labels, title):
    """
    Gets list of inputs from the user.
    Sample call:
        get_inputs(["Name","Surname","Age"],"Please provide your personal information")
    Sample display:
        Please provide your personal information
        Name <user_input_1>
        Surname <user_input_2>
        Age <user_input_3>

    Args:
        list_labels: list of strings - labels of inputs
        title: title of the "input section"

    Returns:
        List of data given by the user. Sample return:
            [<user_input_1>, <user_input_2>, <user_input_3>]
    """
    inputs = []
    if type(list_labels) == list:
        print(title)

        for question in list_labels:
            user_input = input(question+': ')
            inputs.append(user_input)

    elif len(list_labels) == 1:
        user_input = input(list_labels[0]+':')
        inputs.append(user_input)

    return inputs


# This function displays an error message. (example: Error: @message)
#
# @message: string - the error message
def print_error_message(message):
    """
    Displays an error message

    Args:
        message(str): error message to be displayed

    Returns:
        This function doesn't return anything it only prints to console.
    """
    print(message)
