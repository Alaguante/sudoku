from multipledispatch import dispatch


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
        self.field[pos_y - 1][pos_x - 1] = number

    def get_number(self, pos_x: int, pos_y: int) -> int:
        """
        Returns the number in the given position.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: The number in the given position
        """
        return self.field[pos_y - 1][pos_x - 1]

    def get_line(self, index: int) -> list:
        """
        Returns the line of the given index.
        :param index: Index from 1 to 9.
        :return: A list of numbers (as ints) from the line.
        """
        return self.field[index - 1]

    def get_column(self, index: int) -> list:
        """
        Returns the column of the given index.
        :param index: Index from 1 to 9.
        :return: A list of numbers (ints) from the column
        """
        column = []

        for i in range(1, 10):
            number = self.get_number(index, i)
            column.append(number)

        return column

    def get_block(self, pos_x: int, pos_y: int) -> list:
        """
        Returns the block (3x3) the given position is a part of.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: A list containing lists containing the numbers (ints) of the block.
        """
        block = []

        block_start_pos_x = get_block_start_pos(pos_x, pos_y)[0]
        block_start_pos_y = get_block_start_pos(pos_x, pos_y)[1]

        for i in range(3):
            block_line = []
            for j in range(3):
                block_line.append(self.get_number(block_start_pos_x + j, block_start_pos_y + i))
            block.append(block_line)

        return block

    def is_line_valid(self, index: int) -> bool:
        """
        Checks if a line is considered as valid regarding the sudoku rules.
        :param index: Index from 1 to 9.
        :return: True if the line is considered valid, False otherwise
        """
        line_without_empty_field = [x for x in self.get_line(index) if -1 != x]

        is_valid = len(set(line_without_empty_field)) >= len(line_without_empty_field)
        return is_valid

    def is_column_valid(self, index: int) -> bool:
        """
        Checks if a column is considered as valid regarding the sudoku rules.
        :param index: Index from 1 to 9.
        :return: True if the column is considered valid, False otherwise
        """
        column_without_empty_field = [x for x in self.get_column(index) if -1 != x]

        is_valid = len(set(column_without_empty_field)) >= len(column_without_empty_field)
        return is_valid

    def is_block_valid(self, pos_x: int, pos_y: int) -> bool:
        """
        Checks if a block (3x3) is considered as valid regarding the sudoku rules.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: True if the block is considered valid, False otherwise.
        """
        block = self.get_block(pos_x, pos_y)
        numbers_of_block = []
        for line in block:
            for number in line:
                numbers_of_block.append(number)

        numbers_of_block_without_empty_fields = [x for x in numbers_of_block if -1 != x]

        is_valid = len(set(numbers_of_block_without_empty_fields)) >= len(numbers_of_block_without_empty_fields)
        return is_valid

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
        with open(file_path) as f:
            file_content = f.read()

        chars = [x for x in [*file_content] if x not in [",", " ", "\n"]]

        numbers = []
        for i in range(0, len(chars)):
            if chars[i] not in "#":
                current_number = int(chars[i])
                numbers.append(current_number)
            else:
                numbers.append(-1)
                i += 1

        for i in range(1, 10):
            for j in range(1, 10):
                current_number = numbers.pop(0)
                self.set_number(j, i, current_number)
                if 1 <= current_number <= 9:
                    self.set_as_org_number(j, i)

    def set_as_org_number(self, pos_x: int, pos_y: int) -> None:
        """
        Sets the number of the given position as an original number.
        Original numbers are those, which are already given at the start.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        """
        self.org_number_map[pos_y - 1][pos_x - 1] = True

    def is_org_number(self, pos_x: int, pos_y: int) -> bool:
        """
        Checks if a number is an original number
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: True if the number at the given position if an original number, False otherwise
        """
        return self.org_number_map[pos_y - 1][pos_x - 1]

    def is_field_solved(self) -> bool:
        """
        Checks if a field is solved completely.
        That is, if the field does not contain empty spots and all positions are considered valid.
        :return: True if the field is solved completely, False otherwise
        """
        for line in self.field:
            if -1 in line:
                return False

        for i in range(1, 10):
            for j in range(1, 10):
                if not self.is_line_valid(i):
                    return False
                if not self.is_column_valid(j):
                    return False
                if not self.is_block_valid(j, i):
                    return False

        return True

    def is_pos_valid(self, pos_x, pos_y) -> bool:
        """
        Checks if the given position is considered valid.
        :param pos_x: X position from 1 to 9.
        :param pos_y: Y position from 1 to 9.
        :return: True if the position is considered valid, False otherwise
        """
        if not self.is_line_valid(pos_y):
            return False
        if not self.is_column_valid(pos_x):
            return False
        if not self.is_block_valid(pos_x, pos_y):
            return False
        return True


def get_block_start_pos(pos_x: int, pos_y: int) -> tuple:
    """
    Calculates the position of the top left corner of the block the given position is a part of.
    :param pos_x: X position from 1 to 9.
    :param pos_y: Y position from 1 to 9.
    :return: The position of the top left corner of the block.
    """
    if pos_x <= 3:
        block_start_x_pos = 1
    elif pos_x <= 6:
        block_start_x_pos = 4
    else:
        block_start_x_pos = 7

    if pos_y <= 3:
        block_start_y_pos = 1
    elif pos_y <= 6:
        block_start_y_pos = 4
    else:
        block_start_y_pos = 7

    return block_start_x_pos, block_start_y_pos
