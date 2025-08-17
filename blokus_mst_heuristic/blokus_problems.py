import math

from board import Board
from search import SearchProblem, ucs
import util
import numpy as np
import heapq

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
    targets = [(0, 0), (state.board_h - 1, 0), (0, state.board_w - 1), (state.board_h - 1, state.board_w - 1)]
    return generic_heuristic(state, problem, targets)


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
    """
    """
    return generic_heuristic(state, problem, problem.targets)

def generic_heuristic(state, problem, targets):
    """
    The heuristic finds the minimal amount of steps to cover all targets by finding the minimum spanning tree
    between all targets on the board and adding the distance from the closest target to an already occupied tile.
    """
    uncovered_targets = find_uncovers_targets(state, targets)

    if not uncovered_targets:
        return 0  # All targets are covered

    # Get all occupied tiles on the board
    occupied_tiles = find_occupied_tiles(state)
    min_dist = float('inf')

    # Find the closest uncovered target to an occupied tile
    for tile in occupied_tiles:
        for target in uncovered_targets:
            cur_dist = chebyshev_distance(tile, target)
            if cur_dist < min_dist:
                min_dist = cur_dist

    # Find the minimum spanning tree of the uncovered targets
    mst_len = find_mst(uncovered_targets)

    return min_dist + mst_len

# Helper functions:

def find_mst(positions):
    """
    Find the minimum spanning tree weight for the given positions using Prim's algorithm.
    """
    if not positions:
        return 0

    start = positions[0]
    visited = set()
    total_weight = 0
    min_heap = [(0, start)]

    while min_heap:
        cost, u = heapq.heappop(min_heap)
        if u in visited:
            continue
        visited.add(u)
        total_weight += cost
        for v in positions:
            if v not in visited:
                heapq.heappush(min_heap, (chebyshev_distance(u, v), v))

    return total_weight

def find_occupied_tiles(state):
    """
    Find all the occupied tiles on the board.
    """
    occupied_tiles = []

    for y in range(state.board_h):
        for x in range(state.board_w):
            if state.get_position(x, y) != -1:
                occupied_tiles.append((x, y))

    return occupied_tiles

def find_uncovers_targets(state, targets):
    """
    Finds the targets that are not covered by a piece.
    """
    uncovered_targets = []

    for target in targets:
        if state.get_position(target[1], target[0]) == -1:
            uncovered_targets.append(target)

    return uncovered_targets

def chebyshev_distance(first_pos, second_pos):
    """
    Calculates the Chebyshev distance between two points.
    """
    return max(abs(first_pos[0] - second_pos[0]), abs(first_pos[1] - second_pos[1]))


###############################
# previously used heuristics: #
###############################

# Corners:

# def blokus_corners_heuristic(state, problem):
#     """
#     Your heuristic for the BlokusCornersProblem goes here.
#
#     This heuristic must be consistent to ensure correctness.  First, try to come up
#     with an admissible heuristic; almost all admissible heuristics will be consistent
#     as well.
#
#     If using A* ever finds a solution that is worse uniform cost search finds,
#     your heuristic is *not* consistent, and probably not admissible!  On the other hand,
#     inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
#     """
#     # number of uncovered targets:
#     bottom_left = (0, 0)
#     bottom_right = (0, state.board_w - 1)
#     top_left = (state.board_h - 1, 0)
#     top_right = (state.board_h - 1, state.board_w - 1)
#     corners = [top_left, top_right, bottom_right, bottom_left]  # (h, w) / (y,x)
#
#     uncovered = 0
#     for corner in corners:
#         if state.get_position(corner[1], corner[0]) == -1:
#             uncovered += 1
#
#     # distance from the farthest target:
#     max_dist = 0
#     for corner in corners:
#         dist = find_min_dist(state, corner)  # Find the minimum distance to the corner
#         if dist == float('inf'):
#             return float('inf')
#         if dist > max_dist:
#             max_dist = dist
#
#     return uncovered + max_dist - 1

# Cover:

# def find_min_dist(state, target):
#     """
#     Find the minimum distance between an occupied tile on the board to the given target
#     """
#     if state.get_position(target[1], target[0]) > -1:   # if target is occupied distance is 0
#         return 0
#
#     min_dist = float('inf')
#
#     for h in range(state.board_h):
#         for w in range(state.board_w):
#             if state.get_position(w, h) == -1:
#                 continue  # if tile is not occupied
#             dist = max(abs(w - target[1]), abs(h - target[0]))  # chebyshev distance
#             if dist < min_dist:
#                 min_dist = dist
#
#     return min_dist


# def blokus_cover_heuristic_(state, problem):
#     "*** YOUR CODE HERE ***"
#     # number of uncovered targets:
#     uncovered = 0
#
#     for target in problem.targets:
#         if state.get_position(target[1], target[0]) == -1:
#             uncovered += 1
#
#     # distance from the farthest target:
#     max_dist = 0
#     for target in problem.targets:
#         dist = find_min_dist(state, target)  # Find the minimum distance to the target
#         if dist == float('inf'):
#             return float('inf')
#         if dist > max_dist:
#             max_dist = dist
#
#     return max(max_dist, uncovered)
#     # return max_dist
#     #return uncovered
