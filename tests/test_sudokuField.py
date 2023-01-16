import unittest

import sudokuField
from sudokuField import Field


class TestFieldBasic(unittest.TestCase):
    def setUp(self) -> None:
        self.field = Field()

    def test_get_number(self):
        self.assertEqual(-1, self.field.get_number(1, 1))
        self.field.field[0][1] = 2
        self.assertEqual(2, self.field.get_number(2, 1))

    def test_set_number(self):
        self.field.set_number(1, 1, 1)
        self.assertEqual(1, self.field.get_number(1, 1))
        self.field.set_number(1, 3, 4)
        self.assertEqual(4, self.field.get_number(1, 3))

    def test_get_line(self):
        empty_line = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        line = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.assertEqual(empty_line, self.field.get_line(1))

        for i in range(1, 10):
            self.field.set_number(i, 1, i)

        self.assertEqual(line, self.field.get_line(1))

    def test_get_column(self):
        empty_column = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
        line = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.assertEqual(empty_column, self.field.get_column(1))

        for i in range(1, 10):
            self.field.set_number(1, i, i)

        self.assertEqual(line, self.field.get_column(1))

    def test_get_block(self):
        empty_block = [
            [-1, -1, -1],
            [-1, -1, -1],
            [-1, -1, -1]
        ]
        block = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]

        self.assertEqual(empty_block, self.field.get_block_for_position(2, 3))

        number = 1
        for i in range(1, 4):
            for j in range(1, 4):
                self.field.set_number(j, i, number)
                number += 1

        self.assertEqual(block, self.field.get_block_for_position(2, 3))

    def test_get_block_start_pos(self):
        block_1_start_pos = (1, 1)
        block_2_start_pos = (4, 1)

        self.assertEqual(block_1_start_pos, sudokuField.get_block_start_pos(2, 3))
        self.assertEqual(block_1_start_pos, sudokuField.get_block_start_pos(1, 3))
        self.assertEqual(block_1_start_pos, sudokuField.get_block_start_pos(3, 3))

        self.assertEqual(block_2_start_pos, sudokuField.get_block_start_pos(4, 3))

    def test_set_as_org_number(self):
        self.field.set_as_org_number(1, 1)
        self.assertTrue(self.field.org_number_map[0][0])

    def test_is_org_number(self):
        self.field.set_as_org_number(1, 1)
        self.assertTrue(self.field.is_org_number(1, 1))
        self.assertFalse(self.field.is_org_number(1, 2))


class TestFieldAdvanced(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_field = Field()
        self.valid_field.field = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [9, 1, 2, 3, 4, 5, 6, 7, 8],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [2, 3, 4, 5, 6, 7, 8, 9, 1]
        ]

        self.not_valid_column_field = Field()
        for i in range(1, 10):
            number = 1
            for j in range(1, 10):
                self.not_valid_column_field.set_number(j, i, number)
                number += 1

        self.not_valid_line_field = Field()
        for i in range(1, 10):
            number = 1
            for j in range(1, 10):
                self.not_valid_line_field.set_number(i, j, number)
                number += 1

    def test_is_line_valid(self):
        self.assertTrue(self.valid_field.is_line_valid(1))
        self.assertFalse(self.not_valid_line_field.is_line_valid(1))

    def test_is_column_valid(self):
        self.assertTrue(self.valid_field.is_column_valid(1))
        self.assertFalse(self.not_valid_column_field.is_column_valid(1))

    def test_is_block_valid(self):
        for i in range(1, 8, 3):
            for j in range(1, 8, 3):
                self.assertTrue(self.valid_field.is_block_valid(j, i))

        for i in range(1, 8, 3):
            for j in range(1, 8, 3):
                self.assertFalse(self.not_valid_line_field.is_block_valid(j, i))

    def test_is_pos_valid(self):
        self.assertTrue(self.valid_field.is_pos_valid(2, 3))
        self.assertFalse(self.not_valid_line_field.is_pos_valid(2, 3))
        self.assertFalse(self.not_valid_column_field.is_pos_valid(2, 3))

    def test_is_field_solved(self):
        self.assertTrue(self.valid_field.is_field_solved())

        field_to_solve = Field("test_data/sudoku_to_solve.txt")
        self.assertFalse(field_to_solve.is_field_solved())

        self.assertFalse(self.not_valid_line_field.is_field_solved())
        self.assertFalse(self.not_valid_column_field.is_field_solved())


class TestFieldLoad(unittest.TestCase):
    def setUp(self) -> None:
        self.valid_field = Field()
        self.valid_field.field = [
            [1, 2, 3, 4, 5, 6, 7, 8, 9],
            [7, 8, 9, 1, 2, 3, 4, 5, 6],
            [4, 5, 6, 7, 8, 9, 1, 2, 3],
            [9, 1, 2, 3, 4, 5, 6, 7, 8],
            [6, 7, 8, 9, 1, 2, 3, 4, 5],
            [3, 4, 5, 6, 7, 8, 9, 1, 2],
            [8, 9, 1, 2, 3, 4, 5, 6, 7],
            [5, 6, 7, 8, 9, 1, 2, 3, 4],
            [2, 3, 4, 5, 6, 7, 8, 9, 1]
        ]
        self.org_number_map = [
            [True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True],
            [True, True, True, True, True, True, True, True, True]
        ]

        self.sudoku_field_to_solve = Field()
        self.sudoku_field_to_solve.field = [
            [2, 6, -1, -1, 7, -1, 4, 8, 3],
            [3, 1, -1, -1, -1, -1, -1, -1, 9],
            [5, 7, -1, 3, 4, -1, -1, -1, 2],
            [1, -1, -1, -1, -1, -1, 9, -1, -1],
            [-1, 8, -1, -1, 9, -1, -1, 3, -1],
            [-1, -1, 7, -1, -1, -1, -1, -1, 5],
            [7, -1, -1, -1, 5, 2, -1, 9, 4],
            [8, -1, -1, -1, -1, -1, -1, 5, 7],
            [9, 5, 6, -1, 3, -1, -1, 2, 1]
        ]

        self.field = Field()

    def test_load_field_from_path(self):
        file_path = "test_data/valid_sudoku.txt"
        self.field.load_field(file_path)
        self.assertEqual(self.valid_field.field, self.field.field)

    def test_load_file_in_constructor(self):
        file_path = "test_data/valid_sudoku.txt"
        loaded_field = Field(file_path)
        self.assertEqual(self.valid_field.field, loaded_field.field)

        to_solve_file_path = "test_data/sudoku_to_solve.txt"
        to_solve_loaded_field = Field(to_solve_file_path)
        self.assertEqual(self.sudoku_field_to_solve.field, to_solve_loaded_field.field)

    def test_are_loaded_numbers_org_numbers(self):
        file_path = "test_data/valid_sudoku.txt"
        loaded_field = Field(file_path)
        self.assertEqual(self.org_number_map, loaded_field.org_number_map)


if __name__ == '__main__':
    unittest.main()
