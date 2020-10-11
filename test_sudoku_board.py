from unittest import TestCase


class TestSudokuBox(TestCase):
    def test_create_box_no_parameter(self):
        from sudoku_board import SudokuBox
        box = SudokuBox()
        self.assertTrue(box.answer == 0 and not box.original_number and not bool(box.guesses))

    def test_create_box_with_parameter(self):
        from sudoku_board import SudokuBox
        box = SudokuBox(3)
        self.assertTrue(box.answer == 3 and box.original_number and not bool(box.guesses))

    def test_add_guess(self):
        from sudoku_board import SudokuBox
        box = SudokuBox()
        box.add_guess(4)
        box.add_guess(5)
        self.assertTrue(box.answer == 0 and 5 in box.guesses and 4 in box.guesses)
        with self.assertRaises(OverflowError):
            box.add_guess(10)
        with self.assertRaises(OverflowError):
            box.add_guess(0)

    def test_remove_guess(self):
        from sudoku_board import SudokuBox
        box = SudokuBox()
        box.add_guess(4)
        box.add_guess(5)
        box.remove_guess(4)
        self.assertTrue(box == SudokuBox() and 5 in box.guesses and not 4 in box.guesses)

    def test_clear_guesses(self):
        from sudoku_board import SudokuBox
        box = SudokuBox()
        box.add_guess(4)
        box.add_guess(5)
        box.clear_guesses()
        self.assertFalse(bool(box.guesses))

    def test_show_guesses(self):
        from sudoku_board import SudokuBox
        box = SudokuBox()
        box.add_guess(4)
        box.add_guess(5)
        self.assertEqual(box.get_guesses(), [4, 5])
        self.assertNotEqual(box.get_guesses(), [4, 6])

    def test_add_answer(self):
        from sudoku_board import SudokuBox
        box = SudokuBox()
        box.add_answer(4)
        box.add_answer(5)
        self.assertEqual(box, SudokuBox(5))
        self.assertNotEqual(box, SudokuBox(4))
        with self.assertRaises(OverflowError):
            box.add_answer(10)
        with self.assertRaises(OverflowError):
            box.add_answer(0)

    def test_add_answer_preloaded_number(self):
        from sudoku_board import SudokuBox
        box = SudokuBox(1)
        self.assertFalse(box.add_answer(2))
        self.assertEqual(box, SudokuBox(1))

    def test_erase_answer_original_number(self):
        from sudoku_board import SudokuBox
        box = SudokuBox(4)
        box.erase_answer()
        self.assertEqual(box.answer, 4)

    def test__eq__(self):
        from sudoku_board import SudokuBox
        box = SudokuBox(2)
        self.assertEqual(box, SudokuBox(2))
        self.assertNotEqual(box, SudokuBox(1))

    def test__str__(self):
        from sudoku_board import SudokuBox
        box = SudokuBox()
        box.add_answer(4)
        box.add_guess(4)
        box.add_guess(5)
        self.assertEqual(box.__str__(), '4')


class TestSudokuBoard(TestCase):
    def test_create_board(self):
        from sudoku_board import SudokuBoard
        sudoku_board = [[1, 2, 3, 4, 5, 6, 7, 8, 9],  # this sudoku board is not right but it
                        [2, 3, 4, 5, 6, 7, 8, 9, 1],  # doesn't matter we are testing if the board
                        [3, 4, 5, 6, 7, 8, 9, 1, 2],  # is correctly implemented in sudoku board
                        [4, 5, 6, 7, 8, 9, 1, 2, 3],
                        [5, 6, 7, 8, 9, 1, 2, 3, 4],
                        [6, 7, 8, 9, 1, 2, 3, 4, 5],
                        [7, 8, 9, 1, 2, 3, 4, 5, 6],
                        [8, 9, 1, 2, 3, 4, 5, 6, 7],
                        [9, 1, 2, 3, 4, 5, 6, 7, 8]
                        ]
        board = SudokuBoard(sudoku_board)
        for sudoku_row, board_row in zip(sudoku_board, board.board):
            for sudoku_number, board_number in zip(sudoku_row, board_row):
                self.assertEqual(sudoku_number, board_number.answer)

    def test_sudoku_boxes_hold_thier_location(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        for row in range(1, 10):
            for column in range(1, 10):
                self.assertEqual(board.get_sudoku_box(row, column).row, row)
                self.assertEqual(board.get_sudoku_box(row, column).column, column)

    def test_sudoku_boxes_hold_thier_location_import_board(self):
        from sudoku_board import SudokuBoard
        sudoku_board = [[1, 2, 3, 4, 5, 6, 7, 8, 9],  # this sudoku board is not right but it
                        [2, 3, 4, 5, 6, 7, 8, 9, 1],  # doesn't matter we are testing if the board
                        [3, 4, 5, 6, 7, 8, 9, 1, 2],  # is correctly implemented in sudoku board
                        [4, 5, 6, 7, 8, 9, 1, 2, 3],
                        [5, 6, 7, 8, 9, 1, 2, 3, 4],
                        [6, 7, 8, 9, 1, 2, 3, 4, 5],
                        [7, 8, 9, 1, 2, 3, 4, 5, 6],
                        [8, 9, 1, 2, 3, 4, 5, 6, 7],
                        [9, 1, 2, 3, 4, 5, 6, 7, 8]
                        ]
        board = SudokuBoard(sudoku_board)
        for row in range(1, 10):
            for column in range(1, 10):
                self.assertEqual(board.get_sudoku_box(row, column).row, row)
                self.assertEqual(board.get_sudoku_box(row, column).column, column)

    def test_add_answer_stored_in_right_location(self):
        from sudoku_board import SudokuBoard, SudokuBox
        board = SudokuBoard()
        board.add_answer(1, 2, 4)  # board uses indexing starting at 1 instead of 0
        self.assertEqual(board.get_sudoku_box(1, 2), SudokuBox(4))
        with self.assertRaises(IndexError):
            board.add_answer(0, 0, 4)

    def test_add_answer_number_already_included(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        board.add_answer(1, 2, 4)
        self.assertFalse(board.add_answer(1, 3, 4))

    def test_erase_answer(self):
        from sudoku_board import SudokuBox
        box = SudokuBox()
        box.add_answer(4)
        box.erase_answer()
        self.assertEqual(box.answer, 0)

    def test_add_answer_number_not_included(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        board.add_answer(1, 2, 4)
        self.assertTrue(board.add_answer(1, 3, 5))

    def test_get_answer(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        board.add_answer(1, 2, 4)
        self.assertEqual(board.get_answer(1, 2), 4)
        with self.assertRaises(IndexError):
            board.get_answer(0, 0)

    def test_get_answer_out_of_bounds(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        with self.assertRaises(IndexError):
            board.get_answer(0, 0)
        with self.assertRaises(IndexError):
            board.get_answer(10, 10)

    def test_add_guesses(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        board.add_guess(1, 1, 3)
        self.assertEqual(board.board[0][0].get_guesses(), [3])

    def test_get_guesses(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        board.add_guess(1, 1, 3)
        self.assertEqual(board.get_guesses(1, 1), [3])

    def test_get_guesses_out_of_bounds(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        with self.assertRaises(IndexError):
            board.get_guesses(0, 0)
        with self.assertRaises(IndexError):
            board.get_guesses(10, 10)

    def test_number_is_possible_number_included(self):
        from sudoku_board import SudokuBoard
        sudokuboard = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 6],
                       [0, 0, 0, 0, 0, 0, 0, 0, 5],
                       [0, 0, 0, 0, 0, 0, 0, 0, 4],
                       [0, 0, 0, 0, 0, 0, 7, 8, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 2, 3, 0, 0, 0, 0, 0, 0]
                       ]
        board = SudokuBoard(sudokuboard)
        self.assertTrue(board.is_valid_number(9, 9, 9))

    def test_number_is_possible_not_included(self):
        from sudoku_board import SudokuBoard
        sudokuboard = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 6],
                       [0, 0, 0, 0, 0, 0, 0, 0, 5],
                       [0, 0, 0, 0, 0, 0, 0, 0, 4],
                       [0, 0, 0, 0, 0, 0, 7, 8, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [1, 2, 3, 0, 0, 0, 0, 0, 0]
                       ]
        board = SudokuBoard(sudokuboard)
        for answer in range(1, 9):
            self.assertFalse(board.is_valid_number(9, 9, answer))

    def test_is_valid_row_not_included(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        for a in range(1, 9):
            board.add_answer(1, a, a)
        self.assertTrue(board.is_valid_row(1, 9))

    def test_is_valid_row_number_included(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        for a in range(1, 9):
            board.add_answer(1, a, a)
        for a in range(1, 9):
            self.assertFalse(board.is_valid_row(1, a))

    def test_valid_column_number_included(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        for a in range(1, 9):
            board.add_answer(a, 1, a)
        self.assertTrue(board.is_valid_column(1, 9))

    def test_valid_column_number_not_included(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        for a in range(1, 9):
            board.add_answer(a, 1, a)
        for a in range(1, 9):
            self.assertFalse(board.is_valid_column(1, a))

    def test_is_valid_nonet_number_included(self):
        from sudoku_board import SudokuBoard
        sudoku_board = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
                        [6, 7, 2, 1, 9, 5, 3, 4, 8],
                        [1, 9, 8, 3, 4, 2, 5, 6, 7],
                        [8, 0, 0, 0, 6, 0, 4, 2, 3],
                        [4, 0, 0, 8, 0, 3, 7, 9, 1],
                        [7, 0, 0, 0, 2, 0, 8, 5, 6],
                        [0, 6, 0, 0, 0, 0, 2, 8, 4],
                        [0, 0, 0, 4, 1, 9, 6, 3, 5],
                        [0, 0, 0, 0, 8, 0, 1, 7, 9]]
        board = SudokuBoard(sudoku_board)
        self.assertTrue(board.is_valid_nonnet(4, 1, 5))

    def test_is_valid_nonet_number_not_included(self):
        counter = 0
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        for i in range(1, 4):
            for j in range(1, 4):
                if counter != 0:
                    board.add_answer(i, j, counter % 9 + 1)
                counter += 1
        for a in range(2, 9):
            self.assertFalse(board.is_valid_nonnet(1, 1, a))

    def test_get_sudoku_box_number_not_between(self):
        from sudoku_board import SudokuBoard, SudokuBox
        board = SudokuBoard()
        board.add_answer(1, 1, 1)
        self.assertEqual(board.get_sudoku_box(1, 1), SudokuBox(1))

    def test_get_sudoku_box_number_not_between_one_through_nine(self):
        from sudoku_board import SudokuBoard
        board = SudokuBoard()
        with self.assertRaises(IndexError):
            board.get_sudoku_box(0, 0)

    def test_find_emptyspot(self):
        from sudoku_board import SudokuBoard
        sudoku_board = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                        [6, 0, 0, 1, 9, 5, 0, 0, 0],
                        [0, 9, 8, 0, 0, 0, 0, 6, 0],
                        [8, 0, 0, 0, 6, 0, 0, 0, 3],
                        [4, 0, 0, 8, 0, 3, 0, 0, 1],
                        [7, 0, 0, 0, 2, 0, 0, 0, 6],
                        [0, 6, 0, 0, 0, 0, 2, 8, 0],
                        [0, 0, 0, 4, 1, 9, 0, 0, 5],
                        [0, 0, 0, 0, 8, 0, 0, 7, 9]]
        board = SudokuBoard(sudoku_board)
        self.assertTrue(board.find_emptyspot().column == 3)
        self.assertTrue(board.find_emptyspot().row == 1)

    def test_find_emptyspot_full(self):
        from sudoku_board import SudokuBoard
        sudoku_board = [[1, 2, 3, 4, 5, 6, 7, 8, 9],  # this sudoku board is not right but it
                        [2, 3, 4, 5, 6, 7, 8, 9, 1],  # doesn't matter we are testing if the board
                        [3, 4, 5, 6, 7, 8, 9, 1, 2],  # is correctly implemented in sudoku board
                        [4, 5, 6, 7, 8, 9, 1, 2, 3],
                        [5, 6, 7, 8, 9, 1, 2, 3, 4],
                        [6, 7, 8, 9, 1, 2, 3, 4, 5],
                        [7, 8, 9, 1, 2, 3, 4, 5, 6],
                        [8, 9, 1, 2, 3, 4, 5, 6, 7],
                        [9, 1, 2, 3, 4, 5, 6, 7, 8]
                        ]
        board = SudokuBoard(sudoku_board)
        self.assertTrue(board.find_emptyspot() is None)

    def test_solve(self):
        from sudoku_board import SudokuBoard

        board = SudokuBoard()
        self.assertTrue(board.solve())
        print(board)
