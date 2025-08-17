"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    stack = util.Stack()
    visited = []
    stack.push((problem.get_start_state(), []))

    while not stack.isEmpty():
        state, actions = stack.pop()

        if problem.is_goal_state(state):
            return actions

        if state not in visited:
            visited.append(state)
            for successor, action, cost in problem.get_successors(state):
                stack.push((successor, actions + [action]))

    return []  # no solution


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    visited = []
    queue.push((problem.get_start_state(), []))

    while not queue.isEmpty():
        state, actions = queue.pop()

        if problem.is_goal_state(state):
            return actions

        if state not in visited:
            visited.append(state)
            for successor, action, cost in problem.get_successors(state):
                queue.push((successor, actions + [action]))

    return []  # no solution


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    # pq = util.PriorityQueue()
    # visited = []
    # start_node = Node(problem.get_start_state(), [], None, 0, 0)
    # pq.push(start_node, 0)
    #
    # while not pq.isEmpty():
    #     node = pq.pop()
    #
    #     if problem.is_goal_state(node.state):
    #         return node.actions
    #
    #     if node.state not in visited:
    #         visited.append(node.state)
    #         for successor, action, cost in problem.get_successors(node.state):
    #             pq.push(Node(successor, node.actions + [action], node, cost + node.cost), cost + node.cost)
    #
    # return []  # no solution
    return a_star_search(problem)

def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    queue = util.PriorityQueue()
    start_state = problem.get_start_state()
    start_node = Node(start_state, [], None, 0, heuristic(start_state, problem))
    queue.push(start_node, start_node.f)  # node, cost

    visited = dict()  # Maps state to the cost to reach that state

    while not queue.isEmpty():
        node = queue.pop()

        if problem.is_goal_state(node.state):
            return node.actions

        # Check if this node has been visited with a lower cost
        if node.state in visited and visited[node.state] <= node.cost:
            continue

        visited[node.state] = node.cost

        for successor, action, cost in problem.get_successors(node.state):
            cost_so_far = cost + node.cost
            heuristic_cost = heuristic(successor, problem)
            successor_node = Node(successor, node.actions + [action], node, cost_so_far, heuristic_cost)
            queue.push(successor_node, cost_so_far + heuristic_cost)

    return []  # No solution


class Node:
    """
    :parameter state: the state of the board when reaching this node
    :parameter actions: list of actions to reach this state from the start state
    :parameter parent: the parent node
    :parameter g: the cost to reach this state
    :parameter h: the heuristic value of this state
    """
    def __init__(self, state, actions, parent=None, g=0, h=0):
        self.state = state
        self.actions = actions
        self.parent = parent
        self.cost = g
        self.f = g + h  # cost + heuristic

    def __lt__(self, other):
        return True


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search