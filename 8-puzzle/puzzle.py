
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource
import heapq


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        i = self.blank_index
        new_state = None
        if i > 2:
            new_config = (self.config).copy()
            new_config[i] = self.config[i - self.n]
            new_config[i - self.n] = 0
            new_state = PuzzleState(new_config, self.n, parent=self, action="Up", cost=self.cost+1)
        return new_state
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        i = self.blank_index
        new_state = None
        if i < 6:
            new_config = (self.config).copy()
            new_config[i] = self.config[i + self.n]
            new_config[i + self.n] = 0
            new_state = PuzzleState(new_config, self.n, parent=self, action="Down", cost=self.cost+1)
        return new_state
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        i = self.blank_index
        new_state = None
        if i % self.n != 0:
            new_config = (self.config).copy()
            new_config[i] = self.config[i - 1]
            new_config[i - 1] = 0
            new_state = PuzzleState(new_config, self.n, parent=self, action="Left", cost=self.cost+1)
        return new_state

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        i = self.blank_index
        new_state = None
        if i % self.n != self.n - 1:
            new_config = (self.config).copy()
            new_config[i] = self.config[i + 1]
            new_config[i + 1] = 0
            new_state = PuzzleState(new_config, self.n, parent=self, action="Right", cost=self.cost+1)
        return new_state
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children
    
    def __eq__(self, x):
        return (self.cost == x.cost)

    def __ne__(self, x):
        return (self.cost != x.cost)

    def __lt__(self, x):
        return (self.cost < x.cost)

    def __le__(self, x):
        return (self.cost <= x.cost)

    def __gt__(self, x):
        return (self.cost > x.cost)

    def __ge__(self, x):
        return (self.cost >= x.cost)

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, 
                max_search_depth, running_time, max_ram_usage):
    print("path_to_goal: " + str(path_to_goal))
    print("cost_of_path: " + str(cost_of_path))
    print("nodes_expanded: " + str(nodes_expanded))
    print("search_depth: " + str(search_depth))
    print("max_search_depth: " + str(max_search_depth))
    print("running_time: " + str("%.8f" % running_time))
    print("max_ram_usage: " + str("%.8f" % (max_ram_usage/(1024*1024))))

def bfs_search(initial_state):
    """BFS search"""
    start = PuzzleState(initial_state.config, 3)
    frontier = Q.Queue() # Queue implementation for the fringe
    explored = set()
    frontier.put(start)
    
    nodes_expanded = 0
    search_depth = 0
    max_search_depth = 0
    max_ram_usage = 0
    
    start_time = time.time()
    start_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    curr_ram_usage = 0 # Keeps track of memory usage
    
    while not frontier.empty():
        state = frontier.get()
        
        curr_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram_usage
        max_ram_usage = max(curr_ram_usage, max_ram_usage)
            
        if tuple(state.config) not in explored:
            explored.add(tuple(state.config))
            if test_goal(state):
                path_to_goal = []
                cost_of_path = str(state.cost)
                while (state.action != "Initial"):
                    path_to_goal.append(state.action)
                    state = state.parent
                path_to_goal.reverse()
                search_depth = len(path_to_goal)
                running_time = time.time() - start_time
                writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, 
                            max_search_depth, running_time, max_ram_usage)
                return path_to_goal
            
            children = state.expand()
            nodes_expanded += 1
            for neighbor in children:
                if tuple(neighbor.config) not in explored:
                    frontier.put(neighbor)
                    max_search_depth = max(neighbor.cost, max_search_depth)

def dfs_search(initial_state):
    """DFS search"""
    start = PuzzleState(initial_state.config, 3)
    frontier = [] # Stack implementation for the fringe
    frontier_tracker = set() # No direct use, tracks if state has already been added to frontier
    explored = set()
    frontier.append(start)
    frontier_tracker.add(tuple(initial_state.config)) 
    
    nodes_expanded = 0
    search_depth = 0
    max_search_depth = 0
    max_ram_usage = 0
    
    start_time = time.time()
    start_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    curr_ram_usage = 0 # Keeps track of memory usage
    
    while frontier:
        state = frontier.pop()
        frontier_tracker.remove(tuple(state.config))
        
        curr_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram_usage
        max_ram_usage = max(curr_ram_usage, max_ram_usage)
            
        if tuple(state.config) not in explored:
            explored.add(tuple(state.config))
            if test_goal(state):
                path_to_goal = []
                cost_of_path = str(state.cost)
                while (state.action != "Initial"):
                    path_to_goal.append(state.action)
                    state = state.parent
                path_to_goal.reverse()
                search_depth = len(path_to_goal)
                running_time = time.time() - start_time
                writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, 
                            max_search_depth, running_time, max_ram_usage)
                return path_to_goal
            
            children = state.expand()
            children.reverse()
            nodes_expanded += 1
            for neighbor in children:
                if tuple(neighbor.config) not in (explored and frontier_tracker):
                    frontier.append(neighbor)
                    frontier_tracker.add(tuple(neighbor.config))
                    max_search_depth = max(neighbor.cost, max_search_depth)

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, cost, state):
       heapq.heappush(self.heap, (cost, state))

    def pop(self):
       return heapq.heappop(self.heap)[1]

    def empty(self):
        return len(self.heap) == 0
    
    def contains(self, state):
        if(state in self.heap):
            return True
        return False
    
def A_star_search(initial_state):
    """A * search"""
    start = PuzzleState(initial_state.config, 3)
    frontier = PriorityQueue() # Priority queue implementation for the fringe
    explored = set()
    cost = calculate_total_cost(start)
    frontier.push(cost, start)
    
    nodes_expanded = 0
    search_depth = 0
    max_search_depth = 0
    max_ram_usage = 0
    
    start_time = time.time()
    start_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    curr_ram_usage = 0 # Keeps track of memory usage
    
    while not frontier.empty():
        state = frontier.pop()
        
        curr_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram_usage
        max_ram_usage = max(curr_ram_usage, max_ram_usage)
            
        if tuple(state.config) not in explored:
            explored.add(tuple(state.config))
            if test_goal(state):
                path_to_goal = []
                cost_of_path = str(state.cost)
                while (state.action != "Initial"):
                    path_to_goal.append(state.action)
                    state = state.parent
                path_to_goal.reverse()
                search_depth = len(path_to_goal)
                running_time = time.time() - start_time
                writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, 
                            max_search_depth, running_time, max_ram_usage)
                return path_to_goal
            
            children = state.expand()
            nodes_expanded += 1
            for neighbor in children:
                if tuple(neighbor.config) not in explored and frontier.contains(neighbor.config) == False:
                    cost = calculate_total_cost(neighbor)
                    frontier.push(cost, neighbor)
                    max_search_depth = max(neighbor.cost, max_search_depth)

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    cost = state.cost
    for i in range(len(state.config)):
        cost += calculate_manhattan_dist(i, state.config[i], state.n)
    return cost

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    curr_row = int(idx / n)
    curr_col = int(idx % n)
    goal_row = int(value / n)
    goal_col = int(value % n)
    return abs(curr_row - goal_row) + abs(curr_col - goal_col)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    for i in range(9):
        if i != puzzle_state.config[i]:
            return False
    return True

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
