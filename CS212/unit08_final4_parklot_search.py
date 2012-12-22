""" 
| | | | | | | |  |  |  |  |  |  |  |  |
| G G . . . Y |  |  9 10 11 12 13 14  |
| P . . B . Y |  | 17 18 19 20 21 22  |
| P * * B . Y @  | 25 26 27 28 29 30 31
| P . . B . . |  | 33 34 35 36 37 38  |
| O . . . A A |  | 41 42 43 44 45 46  |
| O . . . . . |  | 49 50 51 52 53 54  |
| | | | | | | |  |  |  |  |  |  |  |  | 

puzzle1 = (
 ('G', (9, 10)),
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('@', (31,)),
 ('*', (26, 27)), 
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

GG(9,10)->GG(10,11),..<-AA(44,45)<-AA(45,46),** can only move left right, YYY,PPP,OO,BBB updown
each car either occupy two spot or three.

mission: move the car(**) to @ 
"""
import doctest

N = 8 
def solve_parking_puzzle(start, N=N):
    "find_spots finds all the possible state,action return as a dict" 
    return shortest_path_search(start, find_spots, is_goal) 

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def find_spots(state): 
    succ = {}
    dicts = dict(state)
    cars = [k for k in dicts.keys() if k not in '@|'] 
    for car in cars: 
        carspot = dicts.get(car) # A => (45, 46)
        distance = carspot[1] - carspot[0] # move B(20, 28, 36) up(20+dist..)
        around_spots = is_movable(carspot, distance, dicts)# A=>(42,46) 
        if around_spots:            #originalA(45,46) => frontspace = 45-42
            frontspace, backspace = calculate_space(carspot, around_spots)
            if frontspace:
                for i in range(int(frontspace/distance)): #A: 3/1, B: 8/8
                    succ[replace(dicts, car, -distance*(i+1))] = (car,-distance*(i+1)) 
                    # new_state: action  {..,'A': (44,45).. } :('A', -1)
            if backspace:
                for i in range(int(backspace/distance)):
                    succ[replace(dicts, car, distance*(i+1))] = (car, distance*(i+1)) 
    return succ 

def is_movable(carspot, distance, dicts):
    car_front, car_back = carspot[0], carspot[-1] 
    front, back = empties(car_front, -distance, dicts), empties(car_back, distance, dicts)
    if front != car_front or back != car_back: # fn(empties) will return farthest empty spot it can reach
        return front, back                     # if not will return original params 
    else: 
        return False  

def empties(location, distance, dicts): 
    wall_and_occupied_spots = [i for k, v in dicts.items() if k != '@' for i in v]
    empty_spots = [i for i in range(N**2) if i not in wall_and_occupied_spots] 
    if location + distance not in empty_spots:
        return location
    else:
        return empties(location + distance, distance, dicts) 

def is_goal(state):
    s = dict(state)  
    return set(s['*']) & set(s['@'])  # when '*' and '@' have the same value.


def calculate_space(carspot, around_spots):
    return min(carspot)-min(around_spots), max(around_spots)-max(carspot) 
 
def replace(dicts, key, diff):
    new_d = dicts.copy()
    new_val = tuple([val+diff for val in dicts[key]])
    new_d[key] = new_val
    return tuple((k, v) for k, v in new_d.items()) 
       #return as key for dictionary,gotta be hashable


def locs(start, n, incr=1):
    " locs(13,2) => (13, 14), locs(8, 3, 8) == (8, 16, 24) "
    return tuple(start + incr*i for i in range(n))



def grid(cars, N=N):
    """take (car, spot) tuples, automaticlly determine will walls are and goal, 
       add them, return the tuple as seen in puzzle1"""

    goal = N*(N/2) - 1 
    top_walls = locs(0, N)
    side_walls = tuple(locs(N*i, 2, N-1) for i in range(1,N-1))
    bottom_walls = locs((N-1)*N, N)
    walls_with_goal = top_walls + tuple(i for y in side_walls for i in y) + bottom_walls 
    return cars + (('|', tuple(i for i in walls_with_goal if i is not goal)), ('@', (goal,))) 

def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print


puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]  
 
class Test:"""
>>> path_actions(solve_parking_puzzle(puzzle1))
[('A', -3), ('Y', 24), ('B', 16), ('*', 4)]
>>> path_actions(solve_parking_puzzle(puzzle2))
[('B', -8), ('P', 1), ('O', -24), ('Y', -2), ('P', -1), ('B', 24), ('*', 4)]
>>> path_actions(solve_parking_puzzle(puzzle3))
[('B', -8), ('P', -3), ('O', -32), ('P', 3), ('Y', 3), ('B', 24), ('*', 5)]
"""
"""
    puzzle3         puzzle2         puzzle1
| | | | | | | | | | | | | | | | | | | | | | | |
| . . . . . . | | . . . . . . | | G G . . . Y |
| . . B . . . | | . . . B . . | | P . . B . Y |
| * * B . . . @ | . * * B . . @ | P * * B . Y @
| . . B P P P | | P P P B . . | | P . . B . . |
| . . . . O . | | O . . . . . | | O . . . A A |
| Y Y Y . O . | | O . Y Y Y . | | O . . . . . |
| | | | | | | | | | | | | | | | | | | | | | | |
"""
print doctest.testmod()


