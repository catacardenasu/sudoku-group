import math, random, pygame

"""
This was adapted from a GeeksforGeeks article "Program for Sudoku Generator" by Aarti_Rathi and Ankur Trisal
https://www.geeksforgeeks.org/program-sudoku-generator/

"""


class SudokuGenerator:
    '''
	create a sudoku board - initialize class variables and set up the 2D board
	This should initialize:
	self.row_length		- the length of each row
	self.removed_cells	- the total number of cells to be removed
	self.board			- a 2D list of ints to represent the board
	self.box_length		- the square root of row_length

	Parameters:
    row_length is the number of rows/columns of the board (always 9 for this project)
    removed_cells is an integer value - the number of cells to be removed

	Return:
	None
    '''

    def __init__(self, row_length, removed_cells):
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = int(math.sqrt(row_length))
        self.board = [[0 for x in range(row_length)] for y in range(row_length)]

    '''
	Returns a 2D python list of numbers which represents the board

	Parameters: None
	Return: list[list]
    '''

    def get_board(self):
        return self.board

    '''
	Displays the board to the console
    This is not strictly required, but it may be useful for debugging purposes

	Parameters: None
	Return: None
    '''

    def print_board(self):
        for row in self.board:
            print(row)

    '''
	Determines if num is contained in the specified row (horizontal) of the board
    If num is already in the specified row, return False. Otherwise, return True

	Parameters:
	row is the index of the row we are checking
	num is the value we are looking for in the row

	Return: boolean
    '''

    def valid_in_row(self, row, num):
        return num not in self.board[row]

    '''
	Determines if num is contained in the specified column (vertical) of the board
    If num is already in the specified col, return False. Otherwise, return True

	Parameters:
	col is the index of the column we are checking
	num is the value we are looking for in the column

	Return: boolean
    '''

    def valid_in_col(self, col, num):
        for r in range(self.row_length):
            if self.board[r][col] == num:
                return False
        return True

    '''
	Determines if num is contained in the 3x3 box specified on the board
    If num is in the specified box starting at (row_start, col_start), return False.
    Otherwise, return True

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)
	num is the value we are looking for in the box

	Return: boolean
    '''

    def valid_in_box(self, row_start, col_start, num):
        for r in range(0, 3):
            for c in range(0, 3):
                if num == self.board[row_start + r][col_start + c]:
                    return False
        return True

    '''
    Determines if it is valid to enter num at (row, col) in the board
    This is done by checking that num is unused in the appropriate, row, column, and box

	Parameters:
	row and col are the row index and col index of the cell to check in the board
	num is the value to test if it is safe to enter in this cell

	Return: boolean
    '''

    def is_valid(self, row, col, num):
        box_row = row - row % self.box_length
        box_col = col - col % self.box_length

        return (self.valid_in_row(row, num) and
                self.valid_in_col(col, num) and
                self.valid_in_box(box_row, box_col, num))

    '''
    Fills the specified 3x3 box with values
    For each position, generates a random digit which has not yet been used in the box

	Parameters:
	row_start and col_start are the starting indices of the box to check
	i.e. the box is from (row_start, col_start) to (row_start+2, col_start+2)

	Return: None
    '''

    def fill_box(self, row_start, col_start):
        nums = list(range(1, self.row_length + 1))
        random.shuffle(nums)
        index = 0

        for r in range(self.box_length):
            for c in range(self.box_length):
                self.board[row_start + r][col_start + c] = nums[index]
                index = index + 1

    '''
    Fills the three boxes along the main diagonal of the board
    These are the boxes which start at (0,0), (3,3), and (6,6)

	Parameters: None
	Return: None
    '''

    def fill_diagonal(self):
        for i in range(0, self.row_length, self.box_length):
            self.fill_box(i, i)

    '''
    DO NOT CHANGE
    Provided for students
    Fills the remaining cells of the board
    Should be called after the diagonal boxes have been filled

	Parameters:
	row, col specify the coordinates of the first empty (0) cell

	Return:
	boolean (whether or not we could solve the board)
    '''

    def fill_remaining(self, row, col):
        if (col >= self.row_length and row < self.row_length - 1):
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    '''
    DO NOT CHANGE
    Provided for students
    Constructs a solution by calling fill_diagonal and fill_remaining

	Parameters: None
	Return: None
    '''

    def fill_values(self):
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    '''
    Removes the appropriate number of cells from the board
    This is done by setting some values to 0
    Should be calleds has been called
     after the entire solution has been constructed
    i.e. after fill_value
    NOTE: Be careful not to 'remove' the same cell multiple times
    i.e. if a cell is already 0, it cannot be removed again

	Parameters: None
	Return: None
    '''

    def remove_cells(self):
        removed = 0
        while removed < self.removed_cells:
            r = random.randrange(0, self.row_length)
            c = random.randrange(0, self.row_length)

            if self.board[r][c] != 0:
                removed = removed + 1
                self.board[r][c] = 0


'''
DO NOT CHANGE
Provided for students
Given a number of rows and number of cells to remove, this function:
1. creates a SudokuGenerator
2. fills its values and saves this as the solved state
3. removes the appropriate number of cells
4. returns the representative 2D Python Lists of the board and solution

Parameters:
size is the number of rows/columns of the board (9 for this project)
removed is the number of cells to clear (set to 0)

Return: list[list] (a 2D Python list to represent the board)
'''


def generate_sudoku(size, removed):
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    solution = [row[:] for row in sudoku.get_board()]
    sudoku.remove_cells()
    board = [row[:] for row in sudoku.get_board()]
    return board, solution


class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = 0
        self.selected = False

    def set_cell_value(self, value):
        self.value = value
        if value != 0:
            self.sketched_value = 0

    def set_sketched_value(self, value):
        # set value for the sketched value in pygame
        self.sketched_value = value

    def draw(self):
        # 57 x 57
        cell_size = 513 // 9  # = 57 pixels per cell
        x = self.col * cell_size + 142
        y = self.row * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)

        # Check if mouse is inside this cell
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]  # left button

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
        elif rect.collidepoint(mouse_pos) and mouse_pressed:
            pygame.draw.rect(self.screen, (255, 0, 0), rect, 3)
        else:
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

        # Draw the main value if nonzero
        if self.value != 0:
            font = pygame.font.SysFont("arial", 32)
            text = font.render(str(self.value), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
        elif self.sketched_value != 0:
            sketch_font = pygame.font.SysFont("arial", 18)
            text = sketch_font.render(str(self.sketched_value), True, (150, 150, 150))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected_cell = None

        if self.difficulty == "Easy":
            removed = 30
        if self.difficulty == "Medium":
            removed = 40
        if self.difficulty == "Hard":
            removed = 50

        self.board, self.solution = generate_sudoku(9, removed)
        self.original_board = [row[:] for row in self.board]

        self.cells = [[Cell(self.board[r][c], r, c, screen) for c in range(9)] for r in range(9)]
        self.selected_cell = None

    def draw(self):
        # grid
        for i in range(10):
            y = i * 57
            pygame.draw.line(self.screen, (0, 0, 0), (142, y), (655, y), 1)
        for j in range(10):
            x = j * 57 + 142
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, 513), 1)

        # bold lines
        for k in range(0, 10, 3):
            y = k * 57
            pygame.draw.line(self.screen, (0, 0, 0), (142, y), (655, y), 3)
        for k in range(0, 10, 3):
            x = k * 57 + 142
            pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, 513), 3)

    def select(self, row, col):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].selected = False
        self.cells[row][col].selected = True
        self.selected_cell = (row, col)
        # Marks the cell at (row, col) in the board as the current selected cell.
        # Once a cell has been selected, the user can edit its value or sketched value.

    def click(self, x, y):
        if 0 <= x < 513 and 0 <= y < 513:
            row = y // 57
            col = x // 57
            return row, col
        return None

    # If a tuple of (x,y) coordinates is within the displayed board,
    # this function returns a tuple of the (row, col) of the cell which was clicked.
    # Otherwise, this function returns None.

    def clear(self):
        if self.selected_cell:
            r, c = self.selected_cell
            if self.original_board[r][c] == 0:
                self.cells[r][c].set_cell_value(0)
                # self.cells[r][c].set_sketched_value(0)

    #     Clears the value cell.
    # Note that the user can only remove the cell values and
    # sketched values that are filled by themselves.

    def sketch(self, value):
        if self.selected_cell:
            r, c = self.selected_cell
            if self.original_board[r][c] == 0:
                self.cells[r][c].set_sketched_value(value)
        # Sets the sketched value of the current selected cell equal to the user entered value.
        # It will be displayed at the top left corner of the cell using the draw() function.

    def place_number(self, value):
        if self.selected_cell:
            r, c = self.selected_cell
            if self.original_board[r][c] == 0:
                self.cells[r][c].set_cell_value(value)

    #     Sets the value of the current selected cell equal to the user entered value.
    # Called when the user presses the Enter key.

    def reset_to_original(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].set_cell_value(self.original_board[r][c])
                self.cells[r][c].set_sketched_value(0)
        # Resets all cells in the board to their original values
        # (0 if cleared, otherwise the corresponding digit).

    def is_full(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return False
        return True
        # Returns a Boolean value indicating whether the board is full or not.

    def update_board(self):
        updboard = []
        for r in range(9):
            row = []
            for c in range(9):
                row.append(self.cells[r][c].value)
            updboard.append(row)
        return updboard
        # Updates the underlying 2D board with the values in all cells.

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return (r, c)
        return None
        # Finds an empty cell and returns its row and col as a tuple (x,y).

    def check_board(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].value != self.solution[i][j]:
                    return False
        return True
        # for r in range(9):
        #     nums = set()
        #     for c in range(9):
        #         if self.board[r][c] in nums:
        #             return False
        #         nums.add(self.board[r][c])
        #
        # for c in range(9):
        #     nums = set()
        #     for r in range(9):
        #         if self.board[r][c] in nums:
        #             return False
        #         nums.add(self.board[r][c])
        #
        #
        # return True
