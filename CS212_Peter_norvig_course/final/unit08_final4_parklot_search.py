"""
this is final exam problem 4 from udacity CS212 
simple description from me ( below have a more throughout explaination from
udacity offical) 

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

-------------------------------------------------------------------------------------------------------- 
complicated description from udacity: 

    Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this: 

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
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


