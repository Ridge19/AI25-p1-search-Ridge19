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

import util

from util import PriorityQueue # for priority queue

import heapq # for heap queue

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

# source: pseudocode diagram (Q1)
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # DFS implementation following the Best-First-Search pseudocode pattern
    # Uses a Stack (LIFO) instead of a priority queue for frontier (visited)

    # Testing: to find the best Data Structure to use, i have implemented both Queue, Priority Queue, and Stack. 
    # from this testing, i can conclude that the stack is the most efficient data structure for depth-first search.
    # this was done as in the README specification, it mentioned *if i* decided to use stack as the data strucuture, so i thought 
    # id do more reasearch. 

    # "If you use a Stack as your data structure, the solution found by your DFS algorithm for mediumMaze should have 
    # a length of 130 (provided you push successors onto the fringe in the order provided by getSuccessors; 
    # you might get 246 if you push them in the reverse order). Is this a least cost solution? 
    # If not, think about what depth-first search is doing wrong." - From README

    start_state = problem.getStartState() # Get start state
    stack = util.Stack()  # Stack for DFS (Last In, First Out)
    visited = set()  # Set to track visited states

    # Initialize frontier with start state
    stack.push((start_state, []))  # (state, path_to_state)
    visited.add(start_state)
    
    while not stack.isEmpty():
        # Pop from stack
        current_state, actions = stack.pop()
        
        # Goal test when expanding the node
        if problem.isGoalState(current_state):
            return actions
            
        # Expand current state
        for successor, action, step_cost in problem.getSuccessors(current_state):
            # Check if successor is not in reached
            if successor not in visited:
                visited.add(successor)
                new_actions = actions + [action]
                stack.push((successor, new_actions))
    
    # Return failure (empty list)
    return []


# Source: pseudocode diagram (Q2)
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** IMPLEMENTATION COMPLETE ***"
    # The breadth-first search (BFS) algorithm explores the search tree level by level,
    # starting from the root node and expanding all nodes at the present depth prior to moving on to nodes at the next depth level.
    # In this implementation, we use a queue to keep track of the nodes to be explored.
    # The queue is implemented using the util.Queue class, which provides a first-in-first-out (FIFO) structure.
    # The algorithm starts by initializing the queue with the start state and an empty path.
    # It then enters a loop where it pops the front of the queue, checks if the current state is the goal state, and if not, expands the current state by getting its successors.
    # For each successor, it checks if it has been visited before. If not, it adds the successor to the queue and marks it as visited.

    # Get the start state from the problem instance
    start = problem.getStartState()

    # if the start state = goal state, algrorithm returns an empty list
    if problem.isGoalState(start):
        return []
    
    # Initialize the queue with the start state and an empty path
    queue = util.Queue()
    queue.push((start, []))  # (state, path) 
    visited = set()  # To keep track of visited states

    # Loop until the queue is empty
    while not queue.isEmpty():
        # Pop the front of the queue 
        current_state, path = queue.pop() 

        # Check if the current state has been visited. if so, skip it - otherwise add it to the visited set
        if current_state in visited:
            continue
        visited.add(current_state)

        # Goal test when expanding the node (after popping)
        # If the current state is the goal state, return the path to reach it
        if problem.isGoalState(current_state):
            return path

        # Get successors of the current state
        # For each successor, check if it has been visited
        # If not, add it to the queue and mark it as visited
        # The path is updated by appending the action taken to reach the successor
        for successor, action, step_cost in problem.getSuccessors(current_state):
            if successor not in visited:
                queue.push((successor, path + [action]))
                
    # If no solution is found, return an empty list
    return []


# source: https://www.geeksforgeeks.org/artificial-intelligence/uniform-cost-search-ucs-in-ai/
# source: pseudocode diagram (Q3)
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # UCS or Uniform Cost Search is a Search Algorithm used in AI (Artificial Intelligence) for finding the 
    # least cost path in a given graph network. Being a variant of Dijkstra's algorithm, its useful when 
    # all edges of the graph have different weights and the goal is to find the path with the 
    # minimum total cost from start to goal node.

    start = problem.getStartState()  # Get the start state
    pqueue = PriorityQueue()  # Priority queue for UCS
    pqueue.push((start, [], 0), 0)  # (state, path, cost)
    visited = set()  # To keep track of visited states

    while not pqueue.isEmpty():
        current_state, path, cost = pqueue.pop()
        if current_state in visited:
            continue
        visited.add(current_state)
        if problem.isGoalState(current_state):
            return path
        for successor, action, step_cost in problem.getSuccessors(current_state):
            if successor not in visited:
                new_cost = cost + step_cost
                pqueue.push((successor, path + [action], new_cost), new_cost)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

# source: pseudocode diagram (Q4)
def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** IMPLEMENTATION COMPLETE ***"
    # The A* Search algorithm is a popular pathfinding and graph traversal algorithm 
    # which finds the path with the lowest cost from a start node to a goal node. 
    # in this implementation, we use a priority queue to explore nodes based on their total cost, 
    # and we use a heuristic to estimate the cost to reach the goal from each node.
    #  the priority queue is implemented using the util.PriorityQueue class with a min-heap, where the priority
    # is the total cost (g(n) + h(n)) of the node, where g(n) is the cost to reach the node and h(n) is the heuristic estimate of the 
    # cost to reach the goal from the node. 
    # the algorithm expands nodes in order of their total cost, which ensures that the path found is the most optimal. 

    start_state = problem.getStartState()
    priority_queue = PriorityQueue()
    reached = {}  # Dictionary to track best cost to reach each state
    
    # Initialize with start state
    priority_queue.push((start_state, [], 0), heuristic(start_state, problem))
    reached[start_state] = 0

    while not priority_queue.isEmpty():
        current_state, actions, cost = priority_queue.pop()  
        
        # Skip if we've already found a better path to this state
        if current_state in reached and cost > reached[current_state]:
            continue

        if problem.isGoalState(current_state):
            return actions 
        
        for successor, action, step_cost in problem.getSuccessors(current_state):
            new_cost = cost + step_cost
            
            # Only add if we haven't seen this state or found a better path
            if successor not in reached or new_cost < reached[successor]:
                reached[successor] = new_cost
                f_cost = new_cost + heuristic(successor, problem)
                priority_queue.push((successor, actions + [action], new_cost), f_cost)

    # If no solution is found, return an empty list
    return []


    util.raiseNotDefined()


#####################################################
# EXTENSIONS TO BASE PROJECT
#####################################################

# Extension Q1e
def depthLimitedSearch(problem, limit=1000):
    """Depth-Limited Search (DLS) from pseudocode in spec"""
    # store node states in a tuple 
    from collections import namedtuple 
    Node = namedtuple('Node', ['state', 'actions', 'depth'])

    # use stack data structure due to LIFO nature
    stack = util.Stack()

    # set start state to initial node and push onto stack
    start_state = problem.getStartState()
    stack.push(Node(start_state, [], 0))

    # Initialize result and visited set
    result = 'failure'
    visited = set()

    while not stack.isEmpty():
        # Pop the next node, which contains the state, actions, and depth
        node = stack.pop()
        state, actions, depth = node.state, node.actions, node.depth

        # Goal test
        # if problem is goal state, return actions, otherwise continue
        if problem.isGoalState(state):
            return actions
        # Depth limit check
        # if depth is greater than limit, return 'cutoff' 
        if depth > limit:
            result = 'cutoff'
            continue
        # Cycle check
        # If the state has already been visited, skip it
        # otherwise, add it to the visited set
        if state in visited:
            continue
        visited.add(state)

        # loops through all successor states of current state.
        # each successor creates a new node:
            # push the new node onto the stack
            # increment depth (one deeper than current node) so it can be explored later
        for successor, action, step_cost in problem.getSuccessors(state):
            stack.push(Node(successor, actions + [action], depth + 1))
    return result

def iterativeDeepeningSearch(problem):
    """Iterative Deepening Search (IDS) from pseudocode in spec."""
    # set initial depth
    depth = 0

    # Iteratively deepen the search
    while True:
        # Call depthLimitedSearch with the current depth
        result = depthLimitedSearch(problem, limit=depth)
        # if result is not 'cutoff' and not 'failure', then return result. otherwise,
        # return an empty list
        if result != 'cutoff' and result != 'failure':
            return result
        elif result == 'failure':
            return []

        # Increment the depth for the next iteration
        depth += 1

#####################################################
# Abbreviations
#####################################################
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
ids = iterativeDeepeningSearch
