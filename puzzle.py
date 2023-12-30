from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import heapq
import resource



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


        self.a = cost

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def __gt__(self, node):
        if self.a > node.a:
            return True
        else:
            return False


    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index > 2:
            temp_config = self.config.copy()
            swapped_tile = temp_config[self.blank_index - 3]
            temp_config[self.blank_index] = swapped_tile
            temp_config[self.blank_index - 3] = 0
            name = self.action + " Up"
            child = PuzzleState(temp_config, 3, parent=self, action=name, cost=self.cost+1)
            #print("Move up: ")
            #print(child.config)
            #print("a:", child.a, "  total cost:", calculate_total_cost(child))
            return child
        else:
            return None

        pass

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index < 6:
            temp_config = self.config.copy()
            swapped_tile = temp_config[self.blank_index + 3]
            temp_config[self.blank_index] = swapped_tile
            temp_config[self.blank_index + 3] = 0
            name = self.action + " Down"
            child = PuzzleState(temp_config, 3, parent=self, action=name, cost=self.cost+1)
            #print("Move down: ")
            #print(child.config)
            #print("a:", child.a, "  total cost:", calculate_total_cost(child))
            return child
        else:
            return None

        pass

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index == 0:
            return None
        elif self.blank_index == 3:
            return None
        elif self.blank_index == 6:
            return None
        else:
            temp_config = self.config.copy()
            swapped_tile = temp_config[self.blank_index - 1]
            temp_config[self.blank_index] = swapped_tile
            temp_config[self.blank_index - 1] = 0
            name = self.action + " Left"
            child = PuzzleState(temp_config, 3, parent=self, action=name, cost=self.cost+1)
            #print("Move left: ")
            #print(child.config)
            #print("a:", child.a, "  total cost:", calculate_total_cost(child))
            return child


    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index == 2:
            return None
        elif self.blank_index == 5:
            return None
        elif self.blank_index == 8:
            return None
        else:
            temp_config = self.config.copy()
            swapped_tile = temp_config[self.blank_index + 1]
            temp_config[self.blank_index] = swapped_tile
            temp_config[self.blank_index + 1] = 0
            name = self.action + " Right"
            child = PuzzleState(temp_config, 3, parent=self, action=name, cost=self.cost+1)
            #print("Move right: ")
            #print(child.config)
            #print("a:", child.a, "total cost:", calculate_total_cost(child))
            return child

        pass

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

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth,
                max_search_depth, running_time, ram_usage):
    ### Student Code Goes here
    #path to goal: [‘Up’, ‘Left’, ‘Left’]
    #cost of path: 3
    #nodes expanded: 181437
    #search depth: 3
    #max search depth: 66125
    #running time: 5.01608433
    #max ram usage: 4.23940217

    f = open("output.txt", "w")

    x = len(path_to_goal)
    i = 0
    path_line = ["path_to_goal: ["]
    for item in path_to_goal:
        path_line.append("'")
        path_line.append(item)
        path_line.append("'")
        if i < x-1:
            path_line.append(", ")
        i += 1
    path_line.append("]")
    f.writelines(path_line)

    f.write("\n")

    cost_line = ["cost_of_path: ", str(cost_of_path)]
    f.writelines(cost_line)

    f.write("\n")

    nodes_expanded_line = ["nodes_expanded: ", str(nodes_expanded)]
    f.writelines(nodes_expanded_line)

    f.write("\n")

    search_depth_line = ["search_depth: ", str(search_depth)]
    f.writelines(search_depth_line)

    f.write("\n")

    max_search_depth_line = ["max_search_depth: ", str(max_search_depth)]
    f.writelines(max_search_depth_line)

    f.write("\n")

    running_time_line = ["running_time: ", str(running_time)]
    f.writelines(running_time_line)

    f.write("\n")

    max_ram_usage_line = ["max_ram_usage: ", str(ram_usage)]
    f.writelines(max_ram_usage_line)



    f.close()

    pass

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time  = time.time()
    dfs_start_ram=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


    nodes_expanded = 0
    max_search_depth = 0

    visited_nodes = set()
    visited_nodes.add(tuple(initial_state.config))

    if test_goal(initial_state) == True:
        return initial_state


    initial_state.expand()
    print("")


    nodelist = Q.Queue();
    nodelist.put(initial_state)


    while nodelist.empty() == False:
        currentNode = nodelist.get()

        if test_goal(currentNode) == True:
            end_time = time.time()
            print("")
            print("FOUND:")
            print(currentNode.config)
            print(currentNode.action)
            print("Nodes expanded: ", nodes_expanded)
            print("Depth: ", currentNode.cost)
            print("Max search depth:", max_search_depth)

            path = currentNode.action.split(" ")
            path.remove("Initial")

            running_time = round((end_time - start_time), 8)
            dfs_ram = round((resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - dfs_start_ram)/(2**20), 8)

            print("Ram usage:", dfs_ram)


            writeOutput(path, currentNode.cost, nodes_expanded,
                        currentNode.cost, max_search_depth, running_time,
                        dfs_ram)

            return currentNode

        else:
            #print(nodes_expanded)
            nodes_expanded += 1
            if currentNode.cost >= (max_search_depth):
                max_search_depth = currentNode.cost + 1
            currentNode.expand()
            for node in currentNode.children:
                if tuple(node.config) not in visited_nodes:
                    nodelist.put(node)
                    visited_nodes.add(tuple(node.config))



def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    counter = 0

    start_time  = time.time()
    dfs_start_ram=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    max_search_depth = 0
    nodes_expanded = 0
    visited_nodes = set()
    visited_nodes.add(tuple(initial_state.config))

    if test_goal(initial_state) == True:
        return initial_state

    initial_state.expand()
    #print("")


    nodelist = Q.deque();
    nodelist.append(initial_state)

    while len(nodelist) > 0:
    #& (counter < 11):

        #print("Nodelist:")
        #for node in nodelist:
            #print(node.config, " ", node.action)

        currentNode = nodelist.pop()
        #print("selected Node: ", currentNode.config, " ", currentNode.action)
        if test_goal(currentNode) == True:
            end_time = time.time()
            print("")
            print("FOUND:")
            print(currentNode.config)
            print(currentNode.action)
            print("Nodes expanded: ", nodes_expanded)
            print("Max search depth: ", max_search_depth)

            path = currentNode.action.split(" ")
            path.remove("Initial")

            running_time = round((end_time - start_time), 8)
            dfs_ram = round((resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - dfs_start_ram)/(2**20), 8)

            print("Ram usage:", dfs_ram)



            writeOutput(path, currentNode.cost, nodes_expanded,
                        currentNode.cost, max_search_depth, running_time,
                        dfs_ram)

            return currentNode

        else:
            nodes_expanded += 1
            counter +=1
            #print("Depth: ", currentNode.cost)
            if currentNode.cost >= (max_search_depth):
                max_search_depth = currentNode.cost + 1
            currentNode.expand()
            #print("Children:")
            childlist = []
            for node in currentNode.children:
                #print(node.config, " ", node.action)
                if tuple(node.config) not in visited_nodes:
                    childlist.append(node)
                    visited_nodes.add(tuple(node.config))
            childlist.reverse()
            for node in childlist:
                nodelist.append(node)


    #if you can't find the goal node ever
    return None


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    nodes_expanded = 0
    max_search_depth = 0
    visited_nodes = set()
    visited_nodes.add(tuple(initial_state.config))

    start_time  = time.time()
    dfs_start_ram=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    nodes = [initial_state]
    heapq.heapify(nodes)


    while len(nodes) > 0:
        #print()
        #print("Nodes:")
        #for node in nodes:
            #print(node.action)

        currentNode = heapq.heappop(nodes)
        #print("selectedNode:", currentNode.action)

        if test_goal(currentNode) == True:
            end_time = time.time()
            print("")
            print("FOUND:")
            print(currentNode.config)
            print(currentNode.action)
            print("Nodes expanded:", nodes_expanded)
            print("Depth:", currentNode.cost)
            print("Max Search Depth:", max_search_depth)

            path = currentNode.action.split(" ")
            path.remove("Initial")

            running_time = round((end_time - start_time), 8)
            dfs_ram = round((resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - dfs_start_ram)/(2**20), 8)

            print("Ram usage:", dfs_ram)


            writeOutput(path, currentNode.cost, nodes_expanded,
                        currentNode.cost, max_search_depth, running_time,
                        dfs_ram)


            return currentNode

        else:
            nodes_expanded += 1
            #print(nodes_expanded)
            if currentNode.cost >= (max_search_depth):
                max_search_depth = currentNode.cost + 1
            currentNode.expand()
            #print("nodes before adding to heap")
            for node in currentNode.children:
                if tuple(node.config) not in visited_nodes:
                    node.a = node.cost + calculate_total_cost(node)
                    #print(node.action, "  ", node.config)
                    #print("g: ", node.cost, "h:", calculate_total_cost(node), "a: ", node.a)
                    heapq.heappush(nodes, node)
                    visited_nodes.add(tuple(node.config))
            heapq.heapify(nodes)
            #print("nodes after heapify")
            #for node in nodes:
                #print(node.action)

    pass

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    totalcost = 0
    for item in state.config:
        x = calculate_manhattan_dist(state.config.index(item), item, 3)
        totalcost += x

    return totalcost

    pass

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###

    idxrow = int(idx/3)
    idxcolumn = int(idx%3)

    valuerow = int(value/3)
    valuecolumn = int(value%3)

    distance = 0

    distance += abs(idxrow - valuerow)
    distance += abs(idxcolumn - valuecolumn)

    return distance

    pass

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    if puzzle_state.config == [0,1,2,3,4,5,6,7,8]:
        return True
    else:
        return False
    pass

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = "ast" #sys.argv[1].lower()
    begin_state = ("8,6,4,2,1,3,5,7,0").split(",")#sys.argv[2].split(",")
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
