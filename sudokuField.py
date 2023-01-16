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

    def set_number(self, pos_x: int, pos_y: int, value: int):
        self.field[pos_y - 1][pos_x - 1] = value

    def get_number(self, pos_x: int, pos_y: int) -> int:
        return self.field[pos_y - 1][pos_x - 1]

    def get_line(self, index: int) -> list:
        return self.field[index - 1]

    def get_column(self, index: int) -> list:
        column = []

        for i in range(1, 10):
            number = self.get_number(index, i)
            column.append(number)

        return column

    def get_block(self, pos_x: int, pos_y: int) -> list:
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
        line_without_empty_field = [x for x in self.get_line(index) if -1 != x]

        is_valid = len(set(line_without_empty_field)) >= len(line_without_empty_field)
        return is_valid

    def is_column_valid(self, index: int) -> bool:
        column_without_empty_field = [x for x in self.get_column(index) if -1 != x]

        is_valid = len(set(column_without_empty_field)) >= len(column_without_empty_field)
        return is_valid

    def is_block_valid(self, pos_x: int, pos_y: int) -> bool:
        block = self.get_block(pos_x, pos_y)
        numbers_of_block = []
        for line in block:
            for number in line:
                numbers_of_block.append(number)

        numbers_of_block_without_empty_fields = [x for x in numbers_of_block if -1 != x]

        is_valid = len(set(numbers_of_block_without_empty_fields)) >= len(numbers_of_block_without_empty_fields)
        return is_valid

    def load_field(self, file_path):
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
        self.org_number_map[pos_y - 1][pos_x - 1] = True

    def is_org_number(self, pos_x: int, pos_y: int) -> bool:
        return self.org_number_map[pos_y - 1][pos_x - 1]

    def is_field_solved(self) -> bool:
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
        if not self.is_line_valid(pos_y):
            return False
        if not self.is_column_valid(pos_x):
            return False
        if not self.is_block_valid(pos_x, pos_y):
            return False
        return True


def get_block_start_pos(pos_x: int, pos_y: int) -> tuple:
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
