import random


class DotsAndBoxes:
    def __init__(self, n):
        self.n = n
        self.hor_links = [False] * (n * (n + 1))  # Defining horizontal link connections(now all False)
        self.ver_links = [False] * (n * (n + 1))  # Defining vertical link connections(now all False)
        self.owners = [' '] * (n ** 2)  # defining the owners of created boxes(now blank)
        self.alphabets = list('abcdefghijklmnopqrstuvwxyz')[0:(n + 1)]
        self.numbers = list('0123456789')[0:(n + 1)]
        self.dots = []  # List for points ID
        for num in self.numbers:
            for i in self.alphabets:
                self.dots.append(i + num)
        self.score1 = 0
        self.score2 = 0
        self.player1 = 'P'
        self.player2 = 'C'
        self.prev_text = ""
        self.player = self.player1

    def is_linked(self, pos1, pos2, hor_links, ver_links):
        if pos1 > pos2:
            pos1, pos2 = pos2, pos1
        if (pos1 + 1) % (self.n + 1) == 0 and pos2 % (self.n + 1) == 0:
            return False
        if pos2 - pos1 == self.n + 1:
            return ver_links[pos1]
        elif pos2 - pos1 == 1:
            return hor_links[pos1 - ((pos1 + 1) // (self.n + 1))]
        else:
            return False

    # part of the following printer function : Helps in same line printing
    def part_print(self, new_text, end=""):
        self.prev_text = self.prev_text + new_text
        if end == "\n":
            print(self.prev_text)
            self.prev_text = ""
        else:
            self.prev_text = self.prev_text + end

    # Prints the dots and links and scores in a user friendly manner
    def printer(self, hor_links, ver_links, owners):
        new_hor_links = []
        for i in hor_links:
            if i:
                new_hor_links.append('___')
            else:
                new_hor_links.append('   ')
        new_ver_links = []
        for i in ver_links:
            if i:
                new_ver_links.append('|   ')
            else:
                new_ver_links.append('    ')
        char = '+'
        hor_index = 0
        ver_index = 0
        owner_index = 0
        row_index = 0
        print('-' * (((self.n + 1) * 4) + 8) + '\n')
        print("    a   b   c   d   e   f   g   h   i   j   "[0:((self.n + 1) * 4) + 1] + '\n')
        while True:
            print(" " + str(row_index) + ' ', end=' ')
            for i in range(self.n):
                self.part_print(char, "")
                self.part_print(new_hor_links[hor_index], "")
                hor_index += 1
            self.part_print(char, "\n")
            row_index += 1
            if (hor_index) == len(new_hor_links):
                break
            print("   ", end=' ')
            for i in range(self.n + 1):
                self.part_print(new_ver_links[ver_index], "")
                ver_index += 1
            self.part_print("", "\n")
            ver_index -= (self.n + 1)
            print("   ", end=' ')
            for i in range(self.n):
                if ver_links[ver_index]:
                    self.part_print("| " + owners[owner_index] + " ", "")
                else:
                    self.part_print("  " + owners[owner_index] + " ", "")
                owner_index += 1
                ver_index += 1
            if ver_links[ver_index]:
                self.part_print("|", "\n")
            else:
                self.part_print(" ", "\n")
            ver_index += 1
        print('\n\n' + '-' * (((self.n + 1) * 4) + 8))
        print("\nscore of player one (", self.player1, ") : " + str(self.score1))
        print("score of player two (", self.player2, ") : " + str(self.score2))

    # Checks if the given four points are joined correctly so that a box is formed
    def is_box_completed(self, pos1, pos2, pos3, pos4, hor_links, ver_links):
        all = [pos1, pos2, pos3, pos4]
        all.sort()
        for i in all:
            if i < 0 or i > (((self.n + 1) ** 2) - 1):
                return False
        if (self.is_linked(all[0], all[1], hor_links, ver_links) and self.is_linked(all[2], all[3], hor_links,
                                                                                    ver_links)) and (
                self.is_linked(all[0], all[2], hor_links, ver_links) and self.is_linked(all[1], all[3], hor_links,
                                                                                        ver_links)):
            return True
        else:
            return False

    # checks if the given points are joined and returns a list of topmost left points of the box created .
    # if no box is formed, returns [].
    # raises error if the points cannot be joined !
    def create_link(self, pos1, pos2, hor_links, ver_links):
        e = Exception("Error")
        if self.is_linked(pos1, pos2, hor_links, ver_links):
            raise RuntimeError("already present")
        if pos1 > pos2:
            pos1, pos2 = pos2, pos1
        if (pos1 + 1) % (self.n + 1) == 0 and pos2 % (self.n + 1) == 0:
            raise e
        if pos2 - pos1 == self.n + 1:
            ver_links[pos1] = True
            box_id = []
            check = self.is_box_completed(pos1, pos2, pos1 - 1, pos2 - 1, hor_links, ver_links)
            if check:
                box_id.append(pos1 - 1)
            check = self.is_box_completed(pos1, pos2, pos1 + 1, pos2 + 1, hor_links, ver_links)
            if check:
                box_id.append(pos1)
            return box_id
        elif pos2 - pos1 == 1:
            hor_links[pos1 - ((pos1 + 1) // (self.n + 1))] = True
            box_id = []
            check = self.is_box_completed(pos1, pos2, pos1 - (self.n + 1), pos2 - (self.n + 1), hor_links, ver_links)
            if check:
                box_id.append(pos1 - (self.n + 1))
            check = self.is_box_completed(pos1, pos2, pos1 + (self.n + 1), pos2 + (self.n + 1), hor_links, ver_links)
            if check:
                box_id.append(pos1)
            return box_id
        else:
            raise e

    # removes a link from the given points by making the joining index False in the hor_links or ver_links
    # does nothing if the link is absent
    def remove_link(self, pos1, pos2, hor_links, ver_links):
        e = Exception("Error")
        if pos1 > pos2:
            pos1, pos2 = pos2, pos1
        if (pos1 + 1) % (self.n + 1) == 0 and pos2 % (self.n + 1) == 0:
            raise e
        if (pos2 - pos1) == self.n + 1:
            ver_links[pos1] = False
        elif (pos2 - pos1) == 1:
            hor_links[pos1 - ((pos1 + 1) // (self.n + 1))] = False
        else:
            raise e

    # receives the corner(left topmost point of the box) value and changes its ownership to player name
    def change_owner(self, corner, owners, player):
        if corner:
            owners[corner - ((corner + 1) // (self.n + 1))] = player
            return True
        else:
            return False

    # reverses the current player
    def change_player(self):
        if self.player == self.player1:
            self.player = self.player2
        else:
            self.player = self.player1

    # joins every links and checks if a box is created, if not : Deletes the link , else: Keeps it
    def comp_complete_box(self, virtual_hor_links, virtual_ver_links):
        link_joined = []
        box_count = 0
        for i in range((self.n + 1) ** 2):
            try:
                flag = self.create_link(i, i + 1, virtual_hor_links, virtual_ver_links)
                if flag == []:
                    self.remove_link(i, i + 1, virtual_hor_links, virtual_ver_links)
                else:
                    link_joined.append((i, i + 1))
                box_count += len(flag)
            except:
                pass
            try:
                flag = self.create_link(i, i + self.n + 1, virtual_hor_links, virtual_ver_links)
                if flag == []:
                    self.remove_link(i, i + self.n + 1, virtual_hor_links, virtual_ver_links)
                else:
                    link_joined.append((i, i + self.n + 1))
                box_count += len(flag)
            except:
                pass
        return link_joined, box_count, virtual_hor_links, virtual_ver_links

    # calls the comp_complete_box untill the is a slightest chance of gaining a box
    def comp_try_box(self, hor_links, ver_links):
        virtual_hor_links = list(hor_links)
        virtual_ver_links = list(ver_links)
        link_joined = []
        box_count = 0
        while True:
            prev_length = box_count
            new_links, count, virtual_hor_links, virtual_ver_links = self.comp_complete_box(virtual_hor_links,
                                                                                            virtual_ver_links)
            link_joined = link_joined + new_links
            box_count += count
            if box_count == prev_length:
                break
        return link_joined, box_count, virtual_hor_links, virtual_ver_links

    # final Turns generator! comes into play when all chances of gaining a box is gone! joins all not joined lines
    # one by one and counts the possibility of gaining a box by the opponent, then remove the joining the least box
    # gaining possibility is selected takes a random chance from the least possibilities and appends to the
    # link_joined list ,hence generates the final turn chances
    def get_comp_turns(self, link_joined, virtual_hor_links, virtual_ver_links):
        if (False not in virtual_hor_links) and (False not in virtual_ver_links):
            least_gainable_box_count = 0
        else:
            least_gainable_box_count = (self.n + 1) ** 2
        link_available = []
        count = 0
        for link in virtual_hor_links:
            if not link:
                virtual_hor_links[count] = True
                new_link, new_count, H, V = self.comp_try_box(virtual_hor_links, virtual_ver_links)
                for link in new_link:
                    self.remove_link(link[0], link[1], virtual_hor_links, virtual_ver_links)
                if new_count < least_gainable_box_count:
                    least_gainable_box_count = new_count
                    link_available = []
                    link_available.append(((count // self.n) + count, (count // self.n) + (count + 1)))
                elif new_count == least_gainable_box_count:
                    link_available.append(((count // self.n) + count, (count // self.n) + (count + 1)))
                virtual_hor_links[count] = False
            count += 1
        count = 0
        for link in virtual_ver_links:
            if not link:
                virtual_ver_links[count] = True
                new_link, new_count, H, V = self.comp_try_box(virtual_hor_links, virtual_ver_links)
                for link in new_link:
                    self.remove_link(link[0], link[1], virtual_hor_links, virtual_ver_links)
                if new_count < least_gainable_box_count:
                    least_gainable_box_count = new_count
                    link_available = [(count, count + self.n + 1)]
                elif new_count == least_gainable_box_count:
                    link_available.append((count, count + self.n + 1))
                virtual_ver_links[count] = False
            count += 1

        if len(link_joined) >= 3 and least_gainable_box_count >= 2:  # a special winning trick is special cases only!
            del link_joined[-2]
            return link_joined
        else:
            if link_available:
                link_joined.append(random.choice(link_available))  # general case
            return link_joined

    # calls the comp_try_box and get_comp_turns one by one and joins the links(returned from get_comp_turns) and
    # changes the ownership!
    def comp_play(self, hor_links, ver_links):
        box_link_list, box_count, new_hor_links, new_ver_links = self.comp_try_box(hor_links, ver_links)
        turn_list = self.get_comp_turns(box_link_list, new_hor_links, new_ver_links)
        for turn in turn_list:
            box_id = self.create_link(turn[0], turn[1], hor_links, ver_links)
            flag = False
            for corner in box_id:
                flag = self.change_owner(corner, self.owners, "C")
                if flag:
                    self.score2 += len(box_id)
            print("\nline created between", self.dots[turn[0]], "and", self.dots[turn[1]], '\n')


def start_game(obj, point1, point2):
    dont_change = False
    if point1 != 0 and point2 != 0:
        pos1 = obj.dots.index(point1)
        pos2 = obj.dots.index(point2)
        box_id = obj.create_link(pos1, pos2, obj.hor_links, obj.ver_links)
        for corner in box_id:
            dont_change = obj.change_owner(corner, obj.owners, obj.player)

        if dont_change:  # if true the current player will continue the game
            if obj.player == 'P':
                obj.score1 += len(box_id)
            else:
                obj.score2 += len(box_id)
        else:
            if obj.player2 == 'C':  # checks if computer will play
                obj.comp_play(obj.hor_links, obj.ver_links)
            else:
                obj.change_player()  # changes the player

        obj.printer(obj.hor_links, obj.ver_links, obj.owners)  # prints the boxes
    else:
        obj.printer(obj.hor_links, obj.ver_links, obj.owners)  # prints the boxes
        print("Select the points please!")

    if ' ' not in obj.owners:
        # Actions after game is over
        print("\nGame over!!\n")
        obj.printer(obj.hor_links, obj.ver_links, obj.owners)
        diff = obj.score1 - obj.score2
        # prints the score difference and the owners name
        if diff < 0:
            print("\nPlayer 2" + "(" + obj.player2 + ")" + " has won the match with " + str(abs(diff)) + " points")
        elif diff > 0:
            print("\nPlayer 1" + "(" + obj.player1 + ")" + " has won the match with " + str(abs(diff)) + " points")
        else:
            print("\nThe game is draw!")
