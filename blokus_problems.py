import math

from board import Board
from search import SearchProblem, ucs
import util
import numpy as np


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        "*** YOUR CODE HERE ***"
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        "*** YOUR CODE HERE ***"
        h = state.board_h - 1
        w = state.board_w - 1
        return ((state.get_position(w, h) > -1) and (state.get_position(0, h) > -1) and
                (state.get_position(w, 0) > -1) and (state.get_position(0, 0) > -1))

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        return sum(action.piece.get_num_tiles() for action in actions)


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    # number of uncovered targets:
    bottom_left = (0, 0)
    bottom_right = (0, state.board_w - 1)
    top_left = (state.board_h - 1, 0)
    top_right = (state.board_h - 1, state.board_w - 1)
    corners = [top_left, top_right, bottom_right, bottom_left]  # (h, w) / (y,x)

    uncovered = 0
    for corner in corners:
        if state.get_position(corner[1], corner[0]) == -1:
            uncovered += 1

    # distance from the farthest target:
    max_dist = 0
    for corner in corners:
        dist = find_min_dist(state, corner)  # Find the minimum distance to the corner
        if dist == float('inf'):
            return float('inf')
        if dist > max_dist:
            max_dist = dist

    if uncovered == 0 and max_dist == 0:
        return 0

    return uncovered + max_dist - 1

def find_min_dist(state, target):
    """
    Find the minimum distance between an occupied tile on the board to the given target
    """
    if state.get_position(target[1], target[0]) > -1:   # if target is occupied distance is 0
        return 0

    min_dist = float('inf')

    for h in range(state.board_h):
        for w in range(state.board_w):
            if state.get_position(w, h) == -1:
                continue  # if tile is not occupied
            dist = max(abs(w - target[1]), abs(h - target[0]))  # chebyshev distance
            if dist < min_dist:
                min_dist = dist

    return min_dist

class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        "*** YOUR CODE HERE ***"
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        "*** YOUR CODE HERE ***"
        for target in self.targets:
            if state.get_position(target[1], target[0]) == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        return sum(action.piece.get_num_tiles() for action in actions)


def blokus_cover_heuristic(state, problem):
    "*** YOUR CODE HERE ***"
    # number of uncovered targets:
    uncovered = 0

    for target in problem.targets:
        if state.get_position(target[1], target[0]) == -1:
            uncovered += 1

    # distance from the farthest target:
    max_dist = 0
    for target in problem.targets:
        dist = find_min_dist(state, target)  # Find the minimum distance to the target
        if dist == float('inf'):
            return float('inf')
        if dist > max_dist:
            max_dist = dist

    return max(max_dist, uncovered)
    # return max_dist
    #return uncovered