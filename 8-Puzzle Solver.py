import configparser
import sliding as s
import copy
import time
import sys


def main(): # User Interface and User Input
    print('-----------------------------------------------------------------------------------------------')
    print("\n                             Welcome to an 8-Puzzle Solver                              "+'\n')
    print('-----------------------------------------------------------------------------------------------')
    val_1=input("\nSelect option (1) to use pre-load unsolved puzzle or (2) to enter new set of unsolved puzzle: ")
    config = configparser.ConfigParser()
    config.read('configfile.properties')
    if val_1=='1': # using default Pre loaded unsolved puzzle
        print("\nSelect your level of unsolved puzzle:"+'\n'+'(1) Trivial'+'\n'+'(2) VeryEasy'+'\n'+'(3) easy'+'\n'+'(4) doable'+'\n'+'(5) oh_boy')
        val_2=input("\nEnter: ")
        print("\nThe puzzle you have selected is : "+ config.get("puzzlenames",val_2))
        unsolved_puzzle = [int(x) for x in config.get("unsolvedpuzzles",val_2).split(',')]
        display(unsolved_puzzle)
        select_algorithm(unsolved_puzzle,config)
    else: # Getting unsolved puzzle from user
        unsolved_puzzle = input('\nEnter your unsolved puzzle(Number followed by space)):')
        while len(unsolved_puzzle)!=17: # infinite loop until user entering the valid puzzle
            unsolved_puzzle = input("\nEnter a valid unsolved puzzle:")
        user_list = unsolved_puzzle.split()
        user_int_list = []
        for x in user_list:
            user_int_list.append(int(x))
        display(user_int_list)
        if user_int_list == [int(x) for x in config.get("unsolvedpuzzles",'6').split(',')]:
            print("\nYou have Entered the already solved puzzle, Thank you for making my work simple!!!")
            print("\n!!! BYE BYE !!!\n")
        else:
            select_algorithm(user_int_list,config) # calling select_algorithm function and passing the unsolved puzzle with config intialized

def select_algorithm(puzzle, config): # getting the user input to select the algorithm to execute
    print("\nSelect algorithm:\n(1) Uniform Cost Search,\n(2) A* with the Misplaced Tile Heuristic,\n(3) A* with the Manhattan Distance Heuristic.")
    algorithm = input("\nEnter :")
    if algorithm == "1":
        Uniform_Cost_Search(puzzle, config)
    elif algorithm == "2":
        A_star_with_the_Misplaced_Tile_heuristic(puzzle, config, 'function_call')
    else:
        A_star_with_Manhattan_Distance_heuristic(puzzle, config, 'function_call')

def Uniform_Cost_Search(puzzle, config): # UCS algorithm and its heuristic value
    print("\nHeuristic value of Uniform Cost Search is always 0")
    heuristic_value = 0 # for Uniform cost search the heuristic value will be always zero
    Solution(puzzle, heuristic_value, config, 'Uniform Cost Search')

def A_star_with_the_Misplaced_Tile_heuristic(puzzle, config, doable): # A* with misplaced tile and finding its heuristic value
    goal_state = [int(x) for x in config.get("unsolvedpuzzles",'6').split(',')]
    heuristic_value = 0 
    for x in range(len(puzzle)): # calculating the heuristic value
        if puzzle[x]!= goal_state[x]:
            heuristic_value +=1
    if doable == 'function_call':
        Solution(puzzle, heuristic_value, config, 'A* with the misplaced tile heuristic')
    else:
        return heuristic_value

def A_star_with_Manhattan_Distance_heuristic(puzzle, config, doable): # A* with manhattan tile and finding its heuristic value
    heuristic_value=0
    for i, val in enumerate(puzzle): # calculating the heuristic value
        if val !=0:
            heuristic_value+=abs((val-1)%3 - i%3)+abs((val-1)//3 - i//3)
    if doable == 'function_call':
        Solution(puzzle, heuristic_value, config, 'A* with manhattan distance heuristic')
    else:
        return heuristic_value


def display(puzzle): # Display function is used to display the puzzle when ever the user needed
        print( '-------------')
        print( "| {0} | {1} | {2} |".format(puzzle[0], puzzle[1], puzzle[2]))
        print( "| {0} | {1} | {2} |".format(puzzle[3], puzzle[4], puzzle[5]))
        print( "| {0} | {1} | {2} |".format(puzzle[6], puzzle[7], puzzle[8]))
        print("--------------")

class status(): # It is a individual node class which act like snapshot

    def __init__(self, puzzle, heuristic_value): # when ever the object created for class init function will be started
        self.d = 0
        self.h = heuristic_value
        self.onprogress_puzzle = puzzle

def sort(q): # reference : https://realpython.com/sorting-algorithms-python/ bubble sort has been used to arrange the queue respective to heuristic and depth
    n = len(q)
    for x in range(n):
        check_if_already_sorted = True
        for y in range(n-x-1):
            if (q[y].h + q[y].d) > (q[y + 1].h + q[y + 1].d): # checking for the heuristic and depth value for the puzzle and sort according to the sum of it
                q[y], q[y + 1] = q[y + 1], q[y]
                check_if_already_sorted = False
        if check_if_already_sorted:
            break
    return q

def Solution(puzzle, heuristic_value, config, algo): # solution function is used to slide the tile and to find the goal state of the unsolved puzzle
    stageExpanded = 0 # node expanded
    maximum_queue = 0
    duplicate_check = []
    q = [] # queue to load all the possible slided puzzle
    status_intialize = status(puzzle, heuristic_value) # object created for the default or user entered unsolved puzzle
    q.append(status_intialize)
    start_time = time.time()
    while(1): # loop will execute infinitely until it reaches the goal state

        try: # handling the exception if queue value is none then it leads to excemption
            check = status(q[0].onprogress_puzzle, q[0].h) # object created for thr 1st puzzle in the queue
            check.d = q[0].d
            print("\ng(n): {0}, h(n): {1}".format(check.d,check.h))
            display(check.onprogress_puzzle)
            
            latest_time = time.time()
            if latest_time-start_time > 900: # If solution not found over 15 minutes code will be stoped
                sys.exit()
            q.pop(0) # removing the 1st value from the queue
            current_puzzle = copy.deepcopy(check.onprogress_puzzle) # reference: https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/#:~:text=Deep%20copy%20is%20a%20process,is%20copied%20in%20other%20object.

            if current_puzzle == [int(x) for x in config.get("unsolvedpuzzles",'6').split(',')]: # Checking if the Current stae is equal to the Goal state and stop the loop and function
                print('\nHurray!!!! 8-Puzzle has been solved by *** {0} *** algorithm'.format(algo))
                print("\nNumber of nodes expanded: {0}".format(stageExpanded))
                print("\nDepth to the goal node is {0}".format(check.d))
                print("\nMaximum number of nodes in the queue was : {0}".format(maximum_queue))
                print('\nTotal number of time Executed : {:.2f} Seconds'.format(time.time()-start_time))
                print("\n!!! BYE BYE !!!\n")
                return
            
            next_stage = [] # starting the sliding posibilities in all way for the puzzle
            left = s.slide_left(current_puzzle) # calling left slide function in sliding python file
            if left != None: 
                next_stage.append(left)
            right = s.slide_right(current_puzzle) # calling right slide function in sliding python file
            if right != None:
                next_stage.append(right)
            top = s.slide_up(current_puzzle) # calling left up function in sliding python file
            if top != None:
                next_stage.append(top)
            bottom = s.slide_down(current_puzzle) # calling down slide function in sliding python file
            if bottom != None:
                next_stage.append(bottom)
            for sliding_state in next_stage:
                stage_node = status(sliding_state, None) # creating object for all the possible slided puzzles
                if algo == 'A* with the misplaced tile heuristic':
                    stage_node.h = A_star_with_the_Misplaced_Tile_heuristic(stage_node.onprogress_puzzle, config, 'heuristic_value') # getting the heuristic value for misplaced tile
                    temp = (stage_node.onprogress_puzzle,stage_node.d)
                elif algo == 'A* with manhattan distance heuristic':
                    stage_node.h = A_star_with_Manhattan_Distance_heuristic(stage_node.onprogress_puzzle, config, 'heuristic_value') # getting the heuristic value for the manhattan
                    temp = (stage_node.onprogress_puzzle,stage_node.d)
                else:
                    stage_node.h = 0 # for Uniform cost search the heuristic value will be always zero
                    temp = (stage_node.onprogress_puzzle)
                
                if temp not in duplicate_check : # av0iding the repeated state to get the optimal and fast solution
                    stageExpanded+=1
                    q.append(stage_node)
                    stage_node.d = check.d + 1 
                    duplicate_check.append(temp)

                if len(q)> maximum_queue: # updating the maximum queue size
                    maximum_queue = len(q)
            q = sort(q) # calling bubble sort function to arrange the puzzle respective of heuristic and depth
        
        except: # failure handling and leads to stop the code
            print("Failure")
            sys.exit()

if __name__ == "__main__":
    main()
