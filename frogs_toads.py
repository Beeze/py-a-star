import a_star
import math

# Spaces is an class which holds all the logic for altering each space in our puzzle.
class Spaces(object):
    def __init__(self, spaces):
        if isinstance(spaces, Spaces):
            self.spaces = spaces.spaces
        else:
            self.spaces = spaces

    # Defines what the start state of our game is
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

    # Defines what the goal state of our game is
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

    # Creates a copy of our classes spaces array for use in functions.
    def copy(self):
        return Spaces( [ space for space in self.spaces ])

    # Glorified swap function that swaps two elements in our array of spaces.
    def move(self, from_index, to_index):
        new_spaces = self.copy()

        #Get items from the indexes we are coming from, and moving to.
        thing_at_space_we_are_leaving = new_spaces.spaces[ from_index ]
        thing_at_space_we_are_moving_to = new_spaces.spaces[ to_index ]

        #Swap these items, and save them to our copy of the spaces list.
        new_spaces.spaces[from_index], new_spaces.spaces[to_index] = thing_at_space_we_are_moving_to, thing_at_space_we_are_leaving

        return Spaces(new_spaces)

    # used to print data to the console
    def __unicode__(self):
        return repr(self.spaces)

    # used to print data to the console
    def __repr__(self):
        return repr(self.spaces)

    # used for internal memory management
    def __hash__(self):
        return hash(repr(self))

    # checks to see if two nodes are equal
    def __eq__(self, other):
        return repr(self) == repr(other)

# This class builds the tree and sets up the hueristic function for our problem.
class FrogsAndToadsProblem(a_star.Problem):
    def __init__(self, number_of_frogs_and_toads=3):
        self.number_of_frogs_and_toads = number_of_frogs_and_toads

    # This is how we determine the neighbors of a given node.
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

    # This is how we measure the effectiveness of each potential move to a neighbor.
    # For ours, we'll far frogs and toads have moved towards their goal position.
    # Two points if a toad/frog has moved pass the initial empty space
    # One point if a toad/frog is on the initial empty space
    def heuristic(self, position, goal):
        number_of_spaces = len(position.spaces)
        score = 0

        for idx, space in enumerate(position.spaces):
            if idx <= math.floor(number_of_spaces/2) and space == "F":
                score += 2
            elif idx == math.floor(number_of_spaces/2) and space != "_":
                score += 1
            elif idx > math.floor(number_of_spaces/2) and space == "T":
                score += 2

        return score

#__main__ runs when we do `python frogs_toads.py`
if __name__ == '__main__':
    # import sys
    # # if len(sys.args) == 1:
    # #     number_of_pegs = 3
    # # else:
    # #     number_of_pegs = int(sys.args[1])

    # Works for any number of frogs and toads, although anything greater than 5 takes a bit to complete.
    number_of_frogs_and_toads = 4
    frogs_and_toads = FrogsAndToadsProblem(number_of_frogs_and_toads)

    # the "points" in the FrogsAndToadsProblem are of type "Spaces",
    # so the we need to instantiate Spaces for the start and ends points.
    start = Spaces.make_start(number_of_frogs_and_toads)
    goal = Spaces.make_goal(number_of_frogs_and_toads)

    # Find the path using our a_star method.
    solution = a_star.find_path(frogs_and_toads, start, goal)

    for position in solution:
        print position
