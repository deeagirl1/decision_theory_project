class BaseGrid:
    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    def __init__(self):
        self.__user, self.__left_side, self.__right_side, self.__up_side, self.__down_side = None, False, False, False, False

    def get_user(self):
        return self.__user

    def add_user(self, user):
        self.__user = user

    def has_line_on_side(self, side):
        if side == self.LEFT:
            if self.__left_side:
                return True
        if side == self.UP:
            if self.__up_side:
                return True
        if side == self.RIGHT:
            if self.__right_side:
                return True
        if side == self.DOWN:
            if self.__down_side:
                return True
        return False

    def add_line(self, side):
        if not self.has_line_on_side(side):
            if side == self.LEFT:
                self.__left_side = True
                return True
            if side == self.UP:
                self.__up_side = True
                return True
            if side == self.RIGHT:
                self.__right_side = True
                return True
            if side == self.DOWN:
                self.__down_side = True
                return True
        return False

    def four_lines_placed(self):
        if self.has_line_on_side(self.LEFT) and self.has_line_on_side(self.UP) and self.has_line_on_side(
                self.RIGHT) and self.has_line_on_side(self.DOWN):
            return True
        return False


##############################################################################
class FullGridLoaded:
    user1 = "A"
    user2 = "B"
    DRAW = "draw"

    def __init__(self, grid_width, grid_height, user_name_1, user_name_2):
        self.__grid_width, self.__grid_height, self.__user_name_1, self.__user_name_2 = grid_width, grid_height, user_name_1, user_name_2
        self.__grid = self.create_grid()

    def create_grid(self):
        return [[BaseGrid() for _ in range(self.__grid_width)] for _ in range(self.__grid_height)]

    def adding_owner_name_if_four_line(self, obj_, user):
        if user == self.__user_name_1:
            obj_.add_user(self.user1)
        elif user == self.__user_name_2:
            obj_.add_user(self.user2)

    def add_line(self, x, y, side, user):
        bool_value_1, bool_value_2 = False, False
        if self.__grid[x - 1][y - 1].add_line(side):
            bool_value_1 = True
            self.update_neighbour_of_box(x - 1, y - 1, side)
            if self.__grid[x - 1][y - 1].four_lines_placed():
                self.adding_owner_name_if_four_line(self.__grid[x - 1][y - 1], user)
                bool_value_2 = True
        return bool_value_1, bool_value_2

    def update_neighbour_of_box(self, row_index, column_index, side):
        if self.get_neighbour_on_side(side, row_index - 1, column_index - 1) is not None:
            self.get_neighbour_on_side(side, row_index - 1, column_index - 1).add_line((side + 2) % 4)

    def IndexError_raiser(self, row_of_neigh, column_of_neigh):
        if row_of_neigh < 1 or column_of_neigh < 1:
            raise IndexError

    def get_neighbour_on_side(self, side, row, column):
        try:
            if side == 0:
                self.IndexError_raiser(row, column - 1)
                return self.__grid[row - 1][column - 2]
            if side == 1:
                self.IndexError_raiser(row - 1, column)
                return self.__grid[row - 2][column - 1]
            if side == 2:
                return self.__grid[row - 2][column - 1]
            if side == 3:
                return self.__grid[row - 1][column - 2]
        except IndexError:
            return None

    def total_point_of_user(self, user):
        tot_a, tot_b = 0, 0
        for i in range(len(self.__grid)):
            for j in range(len(self.__grid[0])):
                if self.__grid[i][j].get_user() == self.user1:
                    tot_a += 1
                elif self.__grid[i][j].get_user() == self.user2:
                    tot_b += 1
        if user == self.user1:
            return tot_a
        if user == self.user2:
            return tot_b

    def is_ended(self):
        list_ = []
        for i in range(len(self.__grid)):
            for j in range(len(self.__grid[0])):
                if not self.__grid[i][j].four_lines_placed():
                    list_.append(False)
                else:
                    list_.append(True)
        if False in list_:
            return False
        return True

    def winner(self):
        if self.total_point_of_user(self.user1) > self.total_point_of_user(self.user2):
            return self.user1
        elif self.total_point_of_user(self.user1) < self.total_point_of_user(self.user2):
            return self.user2
        else:
            return self.DRAW

    def print_score(self):
        str_ = '\n'
        str_ += 'Score:\n\n'
        n1 = self.__user_name_1 + ' (' + self.user1 + ')'
        n2 = self.__user_name_2 + ' (' + self.user1 + ')'
        str_ += '{:15s} | {:15s}'.format(n1, n2)
        str_ += '\n' + '-' * 37
        str_ += '\n{:<15d} | {:<15d}\n'.format(int(self.total_point_of_user(self.user1)),
                                               int(self.total_point_of_user(self.user2)))
        return str_

    def one_horizontal_line_in_grid(self, index_of_row):  # not working
        str_ = '  '
        print(index_of_row)
        for cell in self.__grid[index_of_row // 2]:
            if index_of_row % 2 == 0:
                str_ += 'o'
                if cell.has_line_on_side(1):
                    str_ += ' —— '
                else:
                    str_ += '    '
            else:
                if cell.has_line_on_side(0):
                    str_ += '| '
                    if cell.four_lines_placed():
                        str_ += ' {:}  '.format(cell.get_user())
                    else:
                        str_ += '   '
                else:
                    str_ += '     '
        if index_of_row % 2 == 0:
            str_ += 'o'
        str_ += '\n'
        return str_

    def __str__(self):  # not working because of one_horizontal_line_in_grid
        str_ = '  '
        for i in range(self.__grid_width):
            str_ += '    {:}'.format(i + 1)
        str_ += '\n'
        for j in range(self.__grid_height * 2):
            if j % 2 == 1:
                str_ += '{:} '.format(j // 2 + 1)
            else:
                str_ += "  "
            str_ += self.one_horizontal_line_in_grid(j)
        str_ += self.print_score()

        return str_


##############################################################################
# main program
##############################################################################
def ask_int():
    while True:
        try:
            integer = int(input())
            return integer
        except ValueError:
            print("Invalid integer! Enter an integer again:")


def ask_direction():
    print("Enter the side of the box to place the line.")
    while True:
        print("Use the following letters: l, r, u, d")
        print("(l = LEFT, r = RIGHT, u = UP, d = DOWN):")
        letter = input()
        if letter.lower() == 'l':
            return BaseGrid.LEFT
        elif letter.lower() == 'u':
            return BaseGrid.UP
        elif letter.lower() == 'r':
            return BaseGrid.RIGHT
        elif letter.lower() == 'd':
            return BaseGrid.DOWN
        else:
            print("Wrong input.")


def ask_coordinates(max_row, max_column):
    while True:
        print("Enter the coordinates separated by comma (row,column):")
        coord_string = input()
        parts = coord_string.split(",")
        try:
            row = int(parts[0])
            column = int(parts[1])
            while row > max_row or row < 1 or column > max_column or column < 1:
                print("Coordinates are out of range.")
                print(
                    "A horizontal coordinate is between 1 and {:d}, and a vertical coordinate is between 1 and {:d}.".format(
                        max_row, max_column))
                print("Enter the coordinates separated by comma (row,column):")
                coord_string = input()
                parts = coord_string.split(",")
                row = int(parts[0])
                column = int(parts[1])
            return row, column
        except ValueError:
            print("Invalid input!")
            print("You need to give numbers separated by comma.")
        except IndexError:
            print("Invalid input!")
            print("Separate the coordinates with comma.")


def main():
    print("The game begins...")
    player1 = input("Enter the name of the first player:\n")
    player2 = input("Enter the name of the second player:\n")
    print("Enter the width of the grid:")
    width = ask_int()
    while width < 1:
        print("The width has to be at least 1. Enter the width of the grid again:")
        width = ask_int()
    print("Enter the height of the grid:")
    height = ask_int()
    while height < 1:
        print("The height has to be at least 1. Enter the height of the grid again:")
        height = ask_int()

    game = FullGridLoaded(width, height, player1, player2)

    player = player1
    print(game)

    while not game.is_ended():
        print("It is {:s}'s turn.".format(player))
        row, column = ask_coordinates(height, width)
        direction = ask_direction()

        line_added, point_earned = game.add_line(row, column, direction, player)
        while not line_added:
            print("There is already a line here. Give coordinates again.")
            row, column = ask_coordinates(height, width)
            direction = ask_direction()
            line_added, point_earned = game.add_line(row, column, direction, player)
        print(game)

        if point_earned:
            if game.is_ended():
                print("{:s} got a point!".format(player))
            else:
                print("{:s} got a point and takes another move!".format(player))
        else:
            if player == player1:
                player = player2
            else:
                player = player1

    print("End of the game.")
    print(game.print_score())
    winner = game.winner()
    if winner == FullGridLoaded.DRAW:
        print("It is a draw.")
    else:
        print("The winner is {:s}, congratulations!".format(winner))


main()

##############################################################################