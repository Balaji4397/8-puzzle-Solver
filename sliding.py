import configparser
import copy # reference: https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/#:~:text=Deep%20copy%20is%20a%20process,is%20copied%20in%20other%20object.

def configuration(section,key): # initializing the config to get the values from the config property file
    config = configparser.ConfigParser()
    config.read('configfile.properties')
    return [int(x) for x in config.get(section, key).split(',')]

def slide_left(current_puzzle): # used to slide the tile left if it is possible
    altered_puzzle = copy.deepcopy(current_puzzle)
    position = altered_puzzle.index(0)
    space_index = configuration("sliding_position","left")
    if position in space_index:
        return None
    else: # if it is possible to move the tile then store the space in temporary and slide the tile to left and temporary to the tile position
        x = altered_puzzle[position - 1]
        altered_puzzle[position - 1] = altered_puzzle[position]
        altered_puzzle[position] = x
        return altered_puzzle
        


def slide_right(current_puzzle): # used to slide the tile right if it is possible
    altered_puzzle = copy.deepcopy(current_puzzle)
    position = altered_puzzle.index(0)
    space_index = configuration("sliding_position","right")
    if position in space_index:
        return None
    else: # if it is possible to move the tile then store the space in temporary and slide the tile to right and temporary to the tile position
        x = altered_puzzle[position + 1]
        altered_puzzle[position + 1] = altered_puzzle[position]
        altered_puzzle[position] = x
        return altered_puzzle
        


def slide_up(current_puzzle): # used to slide the tile up if it is possible
    altered_puzzle = copy.deepcopy(current_puzzle)
    position = altered_puzzle.index(0)
    space_index = configuration("sliding_position","up")
    if position in space_index:
        return None
    else: # if it is possible to move the tile then store the space in temporary and slide the tile to up and temporary to the tile position
        x = altered_puzzle[position - 3]
        altered_puzzle[position - 3] = altered_puzzle[position]
        altered_puzzle[position] = x
        return altered_puzzle
        


def slide_down(current_puzzle): # used to slide the tile down if it is possible
    altered_puzzle = copy.deepcopy(current_puzzle)
    position = altered_puzzle.index(0)
    space_index = configuration("sliding_position","down")
    if position in space_index:
        return None
    else: # if it is possible to move the tile then store the space in temporary and slide the tile to down and temporary to the tile position
        x = altered_puzzle[position + 3]
        altered_puzzle[position + 3] = altered_puzzle[position]
        altered_puzzle[position] = x
        return altered_puzzle
        