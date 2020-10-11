import math
from random import randrange
import time


def number_between_1_and_9(*argv):
    for arg in argv:
        if not (0 < arg < 10):
            return False
    return True


def location_between_one_and_nine(row, column=2):
    if not number_between_1_and_9(row, column):
        raise IndexError('row or column needs to be in between 1 and 9')


def answer_between_one_and_nine(guess):
    if not number_between_1_and_9(guess):
        raise OverflowError("guess or answer needs to be in between 1 and 9")


class SudokuBox:
    def __init__(self, value=0, row=0, column=0):
        self.original_number: bool = value is not 0
        self.answer: int = value
        self.guesses = {}
        self.row = row
        self.column = column

    def add_guess(self, guess):
        answer_between_one_and_nine(guess)
        self.guesses[guess] = guess

    def remove_guess(self, guess):
        self.guesses.pop(guess)

    def clear_guesses(self):
        self.guesses.clear()

    def get_guesses(self):
        return list(self.guesses.values())

    def add_answer(self, answer):
        answer_between_one_and_nine(answer)
        if not self.original_number:
            self.answer = answer
            return True
        return False

    def add_custom(self, answer):
        if self.add_answer(answer):
            self.original_number = True
            return True
        return False


    def erase_answer(self):
        if not self.original_number:
            self.answer = 0

    def is_empty(self):
        return self.answer == 0

    def __str__(self):
        if self.answer == 0:
            return " "
        return str(self.answer)

    def __eq__(self, sudoku_box):
        return sudoku_box.answer == self.answer


class SudokuBoard:
    def __init__(self, board=None):
        self.board = [[]]
        rows, cols = (9, 9)
        if board is None:
            self.board = [[SudokuBox(row=j + 1, column=i + 1) for i in range(cols)] for j in range(rows)]
        else:
            self.board = [[SudokuBox(value=board[j][i], row=j + 1, column=i + 1) for i in range(cols)] for j in
                          range(rows)]

    def get_sudoku_box(self, row, column):
        location_between_one_and_nine(row, column)
        return self.board[row - 1][column - 1]

    def get_row(self, row):
        location_between_one_and_nine(row)
        return self.board[row - 1]

    def add_answer(self, row, column, number):
        if self.is_valid_number(row, column, number):
            return self.get_sudoku_box(row, column).add_answer(number)
        return False

    def add_custom(self, row, column, number):
        if self.is_valid_number(row, column, number):
            return self.get_sudoku_box(row, column).add_custom(number)
        return False

    def get_answer(self, row, column):
        return self.get_sudoku_box(row, column).answer

    def add_guess(self, row, column, guess):
        self.get_sudoku_box(row, column).add_guess(guess)

    def get_guesses(self, row, column):
        return self.get_sudoku_box(row, column).get_guesses()

    def is_valid_number(self, row, column, guess):
        return self.is_valid_row(row, guess) & self.is_valid_nonnet(row, column, guess) & self.is_valid_column(column,
                                                                                                               guess)

    def is_valid_row(self, row, guess):
        answer_between_one_and_nine(guess)
        for box in self.get_row(row):
            if box.answer == guess:
                return False
        return True

    def is_valid_column(self, column, guess):
        location_between_one_and_nine(column)
        answer_between_one_and_nine(guess)
        for row in self.board:
            if row[column - 1].answer == guess:
                return False
        return True

    def is_valid_nonnet(self, row, column, answer):
        sub_x = 1 + math.ceil(row / 3) * 3
        sub_y = 1 + math.ceil(column / 3) * 3

        for y in range(sub_x - 3, sub_x):
            for x in range(sub_y - 3, sub_y):
                if self.get_sudoku_box(y, x).answer == answer:
                    return False
        return True

    def erase_answer(self, row, column, overide_original = False):
        if not self.get_sudoku_box(row, column).original_number or overide_original:
            self.get_sudoku_box(row, column).erase_answer()

    def erase_guess(self, row, column, guess):
        self.get_sudoku_box(row, column).remove_guess(guess)

    def find_emptyspot(self):
        for row in self.board:
            for box in row:
                if box.is_empty():
                    return box
        return None

    def solve(self):
        box = self.find_emptyspot()
        if box is None:
            return True
        else:
            for i in range(1, 10):
                if self.add_answer(number=i, column=box.column, row=box.row):
                    if self.solve():
                        return True
                box.erase_answer()
            return False

    def solvable(self):
        solvable = self.solve()
        for row in self.board:
            for box in row:
                box.erase_answer()
        return solvable

    def create(self, difficulty):
        self.__init__()
        self.add_custom(1, 1, randrange(9) + 1)
        i = 0
        while i < difficulty:
            row = randrange(9) + 1
            col = randrange(9) + 1
            guess = randrange(9) + 1
            added = self.add_custom(row, col, guess)
            if added:
                i += 1
            while not self.solvable():
                i -= 1
                self.erase_answer(row, col,True)

    def __str__(self):
        output = ""
        row_count = 0
        column_count = 1
        for row in self.board:
            if row_count % 3 == 0 and row_count % 9 != 0:
                output += "-----------\n"
            row_count += 1
            for number in row:
                output += str(number)
                if column_count % 3 == 0 and column_count % 9 != 0:
                    output += "|"
                column_count += 1

            output += "\n"
        return output
