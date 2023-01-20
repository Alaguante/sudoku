import os

from multipledispatch import dispatch


def get_block_start_pos(pos_x: int, pos_y: int) -> tuple:
    """
    Calculates the position of the top left corner of the block the given position is a part of.
    :param pos_x: X position from 1 to 9.
    :param pos_y: Y position from 1 to 9.
    :return: The position of the top left corner of the block.
    """
    return get_block_start(pos_x), get_block_start(pos_y)


def get_char_list_from_file(file_path: str) -> list:
    """
    Returns all chars from the given file ignoring ",", " " and newline characters.
    :param file_path: The path to the file which shall be loaded.
    :return: A list of chars.
    """
    with open(file_path) as f:
        file_content = f.read()
    chars = [x for x in [*file_content] if x not in [",", " ", "\n"]]
    return chars


def get_block_start(pos: int) -> int:
    """
    Returns the starting position of the block.
    :param pos: Position from 1 to 9.
    :return: Starting position of the block.
    """
    check_if_pos_is_valid(pos)
    if pos <= 3:
        block_start = 1
    elif pos <= 6:
        block_start = 4
    else:
        block_start = 7
    return block_start


def get_spots_from_file(file_path: str) -> list:
    """
    Returns a list containing the spots from a sudoku extracted from the given file.
    :param file_path: The path to the file which shall be loaded.
    :return: A list of ints containing the spots of the sudoku.
    """
    chars = get_char_list_from_file(file_path)
    numbers = get_numbers_ignoring_empty_spots(chars)
    return numbers


def get_numbers_ignoring_empty_spots(chars: list) -> list:
    """
    Returns a list containing the numbers from a sudoku extracted from the given list.
    Empty spots are converted to -1.
    :param chars: The list from which to extract the numbers.
    :return: A list of ints containing the numbers.
    """
    numbers = []
    for i in range(0, len(chars)):
        if chars[i] not in "#":
            current_number = int(chars[i])
            numbers.append(current_number)
        else:
            numbers.append(-1)
            i += 1
    return numbers


def extract_numbers_from_block(block: list) -> list:
    """
    Returns the numbers of the plock.
    :param block: The block from which to extract the numbers.
    :return: A list[int] containing the numvers of the block
    """
    numbers_of_block = []
    for line in block:
        for number in line:
            numbers_of_block.append(number)
    return numbers_of_block


def does_list_not_contain_multiples(list_to_check: list) -> bool:
    """
    Checks if the list contains multiples. That is, if every item in the unique.
    :param list_to_check: The list to check for multiples.
    :return: True if the list does not contain multiples, False otherwise.
    """
    return len(set(list_to_check)) >= len(list_to_check)


def check_if_number_is_valid(number):
    if number < 1 or number > 9:
        raise NotAValidSudokuNumberException("The number must be between 1 and 9")


@dispatch(int)
def check_if_pos_is_valid(pos):
    if pos < 1 or pos > 9:
        raise NotInPosRangeException("The position must be between 1 and 9")


@dispatch(int, int)
def check_if_pos_is_valid(pos_x, pos_y):
    if pos_x < 1 or pos_x > 9:
        raise NotInPosRangeException("The position must be between 1 and 9")
    if pos_y < 1 or pos_y > 9:
        raise NotInPosRangeException("The position must be between 1 and 9")


def check_if_index_is_valid(index):
    if index < 1 or index > 9:
        raise NotInPosRangeException("The index must be between 1 and 9")


class Field:

    @dispatch()
    def __init__(self):
        self.field = [
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        ]
        self.org_number_map = [
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False],
            [False, False, False, False, False, False, False, False, False]
        ]

    @dispatch(str)
    def __init__(self, file_path: str):
        self.__init__()
        self.load_field(file_path)

    def __str__(self):
        out = ""

        for line_idx, line in enumerate(self.field):
            if line_idx != 0 and line_idx % 3 == 0:
                for y in range(21):
                    if y == 6 or y == 14:
                        out += "+"
                    else:
                        out += "-"
                out += "\n"
            for line_item_idx, line_item in enumerate(line):
                if line_item_idx != 0 and line_item_idx % 3 == 0:
                    out += "| "
                if line_item != -1:
                    out += str(line_item) + " "
                else:
                    out += "# "
            out += "\n"

        return out

    def set_number(self, pos_x: int, pos_y: int, number: int) -> None:
        """
        Sets the number of the given positions to the given number.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :param number: The number to set.
        """
        check_if_number_is_valid(number)
        check_if_pos_is_valid(pos_x, pos_y)

        self.field[pos_y - 1][pos_x - 1] = number

    def get_number(self, pos_x: int, pos_y: int) -> int:
        """
        Returns the number in the given position.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: The number in the given position
        """
        check_if_pos_is_valid(pos_x, pos_y)
        return self.field[pos_y - 1][pos_x - 1]

    def get_line(self, index: int) -> list:
        """
        Returns the line of the given index.
        :param index: Index from 1 to 9.
        :return: A list of numbers (as ints) from the line.
        """
        check_if_index_is_valid(index)
        return self.field[index - 1]

    def get_column(self, index: int) -> list:
        """
        Returns the column of the given index.
        :param index: Index from 1 to 9.
        :return: A list of numbers (ints) from the column
        """
        check_if_index_is_valid(index)
        column = []

        for i in range(1, 10):
            number = self.get_number(index, i)
            column.append(number)

        return column

    def get_block_for_position(self, pos_x: int, pos_y: int) -> list:
        """
        Returns the block (3x3) the given position is a part of.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: A list containing lists containing the numbers (ints) of the block.
        """
        check_if_pos_is_valid(pos_x, pos_y)
        block_start_pos_x = get_block_start_pos(pos_x, pos_y)[0]
        block_start_pos_y = get_block_start_pos(pos_x, pos_y)[1]

        block = self.get_block(block_start_pos_x, block_start_pos_y)

        return block

    def get_block(self, block_start_x: int, block_start_y: int) -> list:
        """
        Returns the block starting at the given position.
        :param block_start_x: X position where the block starts.
        :param block_start_y: Y position where the block starts.
        :return: A list containing lists containing the numbers (ints) of the block.
        """
        block = []
        for i in range(3):
            block.append(self.get_block_line(block_start_x, block_start_y, i))
        return block

    def get_block_line(self, line_start_pos_x: int, line_start_pos_y: int, line_idx: int) -> list:
        """
        Returns a line from the block.
        :param line_start_pos_x: X position where the line starts.
        :param line_start_pos_y: Y position where the line starts.
        :param line_idx: Index which line from the block is to be returned.
        :return: A list[int] containing a line from the block.
        """
        block_line = []
        for j in range(3):
            block_line.append(self.get_number(line_start_pos_x + j, line_start_pos_y + line_idx))
        return block_line

    def is_line_valid(self, index: int) -> bool:
        """
        Checks if a line is considered as valid regarding the sudoku rules.
        :param index: Index from 1 to 9.
        :return: True if the line is considered valid, False otherwise
        """
        line_without_empty_field = [x for x in self.get_line(index) if -1 != x]

        is_valid = does_list_not_contain_multiples(line_without_empty_field)
        return is_valid

    def is_column_valid(self, index: int) -> bool:
        """
        Checks if a column is considered as valid regarding the sudoku rules.
        :param index: Index from 1 to 9.
        :return: True if the column is considered valid, False otherwise
        """
        column_without_empty_field = [x for x in self.get_column(index) if -1 != x]

        is_valid = does_list_not_contain_multiples(column_without_empty_field)
        return is_valid

    def is_block_valid(self, pos_x: int, pos_y: int) -> bool:
        """
        Checks if a block (3x3) is considered as valid regarding the sudoku rules.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: True if the block is considered valid, False otherwise.
        """
        numbers_of_block = self.get_numbers_from_block(pos_x, pos_y)

        numbers_of_block_without_empty_fields = [x for x in numbers_of_block if -1 != x]

        is_valid = does_list_not_contain_multiples(numbers_of_block_without_empty_fields)
        return is_valid

    def get_numbers_from_block(self, pos_x: int, pos_y: int) -> list:
        """
        Returns the numbers of the block the given position is part of.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: A list[int] containing the numbers of the block.
        """
        block = self.get_block_for_position(pos_x, pos_y)
        numbers_of_block = extract_numbers_from_block(block)
        return numbers_of_block

    def load_field(self, file_path: str) -> None:
        """
        Loads a field from the given file. The file format must match\n
        2,6,#,#,7,#,4,8,3\n
        3,1,#,#,#,#,#,#,9\n
        5,7,#,3,4,#,#,#,2\n
        1,#,#,#,#,#,9,#,#\n
        #,8,#,#,9,#,#,3,#\n
        #,#,7,#,#,#,#,#,5\n
        7,#,#,#,5,2,#,9,4\n
        8,#,#,#,#,#,#,5,7\n
        9,5,6,#,3,#,#,2,1\n
        where # is an empty spot.
        :param file_path: The path to the file which shall be loaded.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError("The provided path does not exist")
        elif not os.path.isfile(file_path):
            raise NotAFileError("The provided path is not a file")
        numbers = get_spots_from_file(file_path)

        self.load_numbers_into_field(numbers)

    def load_numbers_into_field(self, numbers: list) -> None:
        """
        Loads the given numbers into the field.
        :param numbers: A list of numbers to load into the field.
        """
        for i in range(1, 10):
            for j in range(1, 10):
                current_number = numbers.pop(0)
                if 1 <= current_number <= 9:
                    self.set_number(j, i, current_number)
                    self.set_as_org_number(j, i)

    def set_as_org_number(self, pos_x: int, pos_y: int) -> None:
        """
        Sets the number of the given position as an original number.
        Original numbers are those, which are already given at the start.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        """
        check_if_pos_is_valid(pos_x, pos_y)
        self.org_number_map[pos_y - 1][pos_x - 1] = True

    def is_org_number(self, pos_x: int, pos_y: int) -> bool:
        """
        Checks if a number is an original number
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: True if the number at the given position if an original number, False otherwise
        """
        check_if_pos_is_valid(pos_x, pos_y)
        return self.org_number_map[pos_y - 1][pos_x - 1]

    def is_field_solved(self) -> bool:
        """
        Checks if a field is solved completely.
        That is, if the field does not contain empty spots and all positions are considered valid.
        :return: True if the field is solved completely, False otherwise
        """
        if self.does_field_contain_empty_spots():
            return False

        if not self.are_all_positions_valid():
            return False

        return True

    def does_field_contain_empty_spots(self) -> bool:
        """
        Checks if the field is completely filled, that is, if the field does not contain empty spots.
        :return: True if the field does not contain empty spots, False otherwise
        """
        for line in self.field:
            if -1 in line:
                return True
        return False

    def are_all_positions_valid(self) -> bool:
        """
        Checks is all positions are valid.
        :return: True if all positions are valid, False otherwise
        """
        for i in range(1, 10):
            for j in range(1, 10):
                if not self.is_pos_valid(j, i):
                    return False
        return True

    def is_pos_valid(self, pos_x, pos_y) -> bool:
        """
        Checks if the given position is considered valid.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: True if the position is considered valid, False otherwise
        """
        if not self.is_block_valid(pos_x, pos_y):
            return False
        elif not self.is_column_valid(pos_x):
            return False
        elif not self.is_line_valid(pos_y):
            return False
        else:
            return True


class NotAValidSudokuNumberException(Exception):
    """
    Raised when the given number is not in the range of 1 to 9.
    """
    pass


class NotInPosRangeException(Exception):
    """
    Raised when the given position is not in the range of 1 to 9.
    """
    pass


class PathNotFoundError(Exception):
    """
    Raised when the given path is not found.
    """
    pass


class NotAFileError(Exception):
    """
    Raised when the given path is not a file.
    """
    pass
