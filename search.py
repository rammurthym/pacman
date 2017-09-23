# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

# Group Information
# Rammurthy Mudimadugula (rxm163730)
# Juhitha Potluri (jxp161330)

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

# Method to enumerate trace back path to reach from goal state to start state.
def result(goalState, parents, actions):
    # list to hold the actions to reach goal state
    actionsList = []
    p = goalState

    # loop through parent states from goal state till we reach the start state.
    while p in parents:
        # insert action at the beginning of the list since we are tracing back the path.
        actionsList.insert(0, actions[p])
        p = parents[p]

    return actionsList

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    visited = [] # list to track visited states.
    parents = {} # dict to track parents of current state.
    actions = {} # dict to track actions to get to parent state from current state

    startState = problem.getStartState()

    # stack to implement DFS.
    stack = util.Stack()
    stack.push(startState)

    # iterate till the stack is empty or goal state is found.
    while not stack.isEmpty():
        currState = stack.pop()

        if currState in visited:
            continue

        visited.append(currState)

        if problem.isGoalState(currState):
            return result(currState, parents, actions)

        successors = problem.getSuccessors(currState)

        for s in successors:
            if s[0] not in visited:
                parents[s[0]] = currState
                actions[s[0]] = s[1]
                stack.push(s[0])

    util.pathNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    visited = [] # list to track visited states.
    parents = {} # dict to track parents of current state.
    actions = {} # dict to track actions to get to parent state from current state

    # queue to implement DFS.
    queue = util.Queue()
    startState = problem.getStartState()
    queue.push(startState)
    visited.append(startState)

    # iterate till the queue is empty or goal state is found.
    while not queue.isEmpty():
        currState = queue.pop()

        if problem.isGoalState(currState):
            return result(currState, parents, actions)

        successors = problem.getSuccessors(currState)

        for s in successors:
            if s[0] not in visited:
                visited.append(s[0])
                parents[s[0]] = currState
                actions[s[0]] = s[1]
                queue.push(s[0])

    util.pathNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    visited = [] # list to track visited states.
    parents = {} # dict to track parents of current state.
    actions = {} # dict to track actions to get to parent state from current state

    startState = problem.getStartState()

    # return empty list if cuurent state is the goal state.
    if problem.isGoalState(startState):
        return []

    currDistance = {} # dict to store the distance from start state to the visiting node.

    # priority queue to implement UCS.
    pq = util.PriorityQueue()
    pq.push(startState, 0)
    currDistance[startState] = 0

    # iterate till the queue is empty or goal state is found.
    while not pq.isEmpty():
        (priority, count, currState) = pq.pop()

        if priority > currDistance[currState]:
            continue
        if problem.isGoalState(currState):
            return result(currState, parents, actions)

        visited.append(currState)

        successors = problem.getSuccessors(currState)

        for s in successors:
            if s[0] in visited:
                continue
            if s[0] not in currDistance or priority + s[2] < currDistance[s[0]]:
                pq.push(s[0], priority+s[2])
                currDistance[s[0]] = priority+s[2]
                parents[s[0]] = currState
                actions[s[0]] = s[1]

    util.pathNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    def h(curr):
        return problem.getCostOfActions(curr[1]) + heuristic(curr[0], problem)

    startState=problem.getStartState()
    pq = util.PriorityQueueWithFunction(h)
    pq.push((startState, []))
    visited = []
    while not pq.isEmpty():
        priority, count, temp = pq.pop()
        currState, actionsList = temp

        if problem.isGoalState(currState):
            return actionsList

        if currState not in visited:
            visited.append(currState)
            
            successors = problem.getSuccessors(currState)
            for s in successors:
                if s[0] not in visited:
                    pq.push((s[0], actionsList+[s[1]]))

    util.pathNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
