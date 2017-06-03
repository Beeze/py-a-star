import a_star
from itertools import cycle
import math

class Spaces(object):
    def __init__(self, spaces):
        if isinstance(spaces, Spaces):
            self.spaces = spaces.spaces
        else:
            self.spaces = spaces

    @staticmethod
    def make_start(number_of_frogs_and_toads):
        # We have this number of frogs and toads, so we multiply the given number
        number_of_spaces = number_of_frogs_and_toads*2+1
        space_list = ["_" for i in xrange(number_of_spaces)]

        if space_list:
            for space_idx in xrange(number_of_spaces):
                if (space_idx < (math.floor(number_of_spaces/2))):
                    space_list[space_idx] = ("T")
                elif (space_idx > math.floor(number_of_spaces/2)):
                    space_list[space_idx] = ("F")

        return Spaces(space_list)

    @staticmethod
    def make_goal(number_of_frogs_and_toads):
        # We have this number of frogs and toads, so we multiply the given number, and add one for the empty space.
        number_of_spaces = number_of_frogs_and_toads*2+1
        space_list = ["_" for i in xrange(number_of_spaces)]

        if space_list:
            for space_idx in xrange(number_of_spaces):
                if (space_idx < math.floor(number_of_spaces/2)):
                    space_list[space_idx] = ("F")
                elif (space_idx > math.floor(number_of_spaces/2)):
                    space_list[space_idx] = ("T")

        return Spaces(space_list)

    def copy(self):
        return Spaces( [ space for space in self.spaces ])

    def move(self, from_index, to_index):
        new_spaces = self.copy()

        #Get items from the indexes we are coming from, and moving to.
        thing_at_space_we_are_leaving = new_spaces.spaces[ from_index ]
        thing_at_space_we_are_moving_to = new_spaces.spaces[ to_index ]

        #Swap these items, and save them to our copy of the spaces list.
        new_spaces.spaces[from_index], new_spaces.spaces[to_index] = thing_at_space_we_are_moving_to, thing_at_space_we_are_leaving

        return Spaces(new_spaces)

    def __unicode__(self):
        return repr(self.spaces)

    def __repr__(self):
        return repr(self.spaces)

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        return repr(self) == repr(other)


class FrogsAndToadsProblem(a_star.Problem):
    def __init__(self, number_of_frogs_and_toads=3):
        self.number_of_frogs_and_toads = number_of_frogs_and_toads

    def neighbor_nodes(self, spaces):
        neighbors = []
        space_list = spaces.spaces
        #Determine the numbers of spaces allocated for this problem
        number_of_spaces = self.number_of_frogs_and_toads*2+1

        #Find the current open space
        open_space_index = space_list.index('_')

        #Get the upper and lower indices from which an animal would be able to move
        upper_bound = open_space_index + 2

        #Make sure upper bound is a valid index in the array
        if upper_bound > len(spaces.spaces) - 1:
            upper_bound = open_space_index + 1 if (open_space_index + 1 <= len(space_list) - 1) else open_space_index

        lower_bound = open_space_index - 2

        #Make sure lower bound is a valid index in the array
        if lower_bound < 0:
            lower_bound = open_space_index - 1 if (open_space_index - 1 >= 0) else open_space_index

        for i in xrange(number_of_spaces):
            if (i == open_space_index):
                continue

            # Here, we think about potential states of the game
            # That would happen after a legal move.
            # For a move to be legal, you can't jump an animal of the same type
            # You can jump at most, one animal
            # and you only can move to an empty space, signified by "_"

            if lower_bound <= i <= upper_bound:
                # We know this animal can potentially be moved.
                offset = 0
                #Figure out if we are currently positioned before or after the open space.
                if i < open_space_index:
                    offset = 1
                else:
                    offset = -1

                # Check to see if we are able to move.
                # If so, figure out how many spaces we can move.
                if space_list[i] != space_list[i+offset] and space_list[i+offset] == "_":
                    neighbor = spaces.move(i, i+offset)
                    neighbors.append(neighbor)

                elif space_list[i] != space_list[i+offset]:
                    # we know we are at most, 2 spaces away from the open space
                    # so we'll try to move our animal there
                    new_offset = 2 if offset > 0 else -2
                    neighbor = spaces.move(i, i+new_offset)
                    neighbors.append(neighbor)
        return neighbors

    def heuristic(self, position, goal):
        # number of frogs and toads moved past the first 3, or last 3 indices respectively.
        number_of_spaces = len(position.spaces)
        score = 0

        for idx, space in enumerate(position.spaces):
            if idx <= math.floor(number_of_spaces/2) and space == "F":
                score += 1
            elif idx == math.floor(number_of_spaces/2) and space != "_":
                score += 1
            elif idx > math.floor(number_of_spaces/2) and space == "T":
                score += 1

        return score

if __name__ == '__main__':
    # import sys
    # # if len(sys.args) == 1:
    # #     number_of_pegs = 3
    # # else:
    # #     number_of_pegs = int(sys.args[1])

    number_of_frogs_and_toads = 6
    frogs_and_toads = FrogsAndToadsProblem(number_of_frogs_and_toads)

    # the "points" in the FrogsAndToadsProblem are of type "Spaces",
    # so the we need to instantiate Spaces for the start and ends points.
    start = Spaces.make_start(number_of_frogs_and_toads)
    goal = Spaces.make_goal(number_of_frogs_and_toads)

    # then a miracle occurs...
    solution = a_star.find_path(frogs_and_toads, start, goal)

    for position in solution:
        print position
