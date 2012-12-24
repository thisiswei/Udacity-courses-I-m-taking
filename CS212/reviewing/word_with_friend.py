#each letter's points
POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10, _=0)
X, Y = (1, 0), (0, 1) # horizontal, vertical

class anchor(set):
    " squares where word can be place, is either right next to a word, or * in the middle "

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
mnx, moab = anchor(list('MNX')), anchor(list('MOAB'))
ANY = anchor(LETTERS)
DW, TW, DL, TL = '23:;' #Bonus: Double word, Tre_letter

def removed(letters, remove):
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters 
 
def transpose(board): return map(list, zip(*board)) 

def is_letter(sq): return isinstance(sq, str) and sq in LETTERS 

def is_empty(sq): return sq == '.' or sq == '*'  or isinstance(sq, anchor)
 
def prefixes(word): return [word[:i] for i in range(len(word))]

def read_words(name):
    words = set(file(name).read().upper().split())
    pres = set(p for word in words for p in prefixes(word))
    return words, pres

WORDS, PREFIXES = read_words('words4k.txt')

prev_hand, prev_results = '', set()  # cache
# find all possible prefixes from this hand
def find_prefixes(hand, pre='', results=set()):
    global prev_hand, prev_results
    if hand == prev_hand: return prev_results
    if pre == '': prev_hand, prev_results = hand, results
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes(removed(hand, L), pre+L, results)
    return results 

# return prefix, maxsize_of_pre. pre can be letters before it or ''. 
#(we restrict prefix can't include any anchors)
def legal_prefixes(row, index):
    s = index
    while is_letter(row[s-1]): s -= 1
    if s < index:
        return ''.join(row[s:index]), index - s
    while is_empty(row[s-1]) and not isinstance(row[s-1], anchor):
        s -= 1
    return '', index - s  

# word = prefixes + suffixes, pre can form from hand, or from letters on board
def add_suffixes(hand, pre, start, row, results, anchored=True):
    i = start + len(pre) #first we set it to false so wont return letters already on board
    if pre in WORDS and anchored and not is_letter(row[i]): #i is one to the right of pre
        results.add((start, pre))
    if pre in PREFIXES: # if not a pre, it's not a word, otherwise, continue search
        sq = row[i]
        if is_letter(sq): # pick prefix from the board
            add_suffixes(hand, pre+sq, start, row, results)
        elif is_empty(sq):# from prefix from hand
            possibilities = sq if isinstance(sq, anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(removed(hand, L), pre+L, start, row, results)
    return results

"""     ---> X dirction 
| | | | | | | | | | | | | | | | |  
| J . . 3 . . ; . ; . . 3 . I . | 
| A . : . . 2 B E . C . . : D . | 
| G U Y . : . . F . H : . . L . | 
| | | | | | | | | | | | | | | | | 
: means double letter, ; tre letter, 2 -> double word score, 3-> tre..
these are bonus from BONUS template, original board the empties represented
as '.'
""" 
def row_plays(hand, row):
    "Return a set of legal plays in a row. (start, word) pairs "
    results = set()
    # to each allowable prefix, add all suffixes, keeping the words
    for index, sq in enumerate(row[1:-1], 1): 
        if isinstance(sq, anchor):
            pre, maxsize = legal_prefixes(row, index)
            if pre: # to his left are letters, gotta use them as prefix
                start = index - len(pre)
                add_suffixes(hand, pre, start, row, results, anchored=False)
            else:
                for pre in find_prefixes(hand):
                    #wont fit otherwise
                    if len(pre) <= maxsize:
                        start = index - len(pre)
                        add_suffixes(removed(hand, pre), pre, start, row,
                                     results, anchored=False)

    return results

def calculate_score(board, pos, direction, word):
    x, y = pos
    xi, yi = direction
    total, crosstotal, word_multi = 0, 0, 1
    other_direction = Y if direction == X else X
    for i, L in enumerate(word):
        xnow, ynow = x + (xi)*i, y + (yi)*i
        sq = board[ynow][xnow]
        b = BONUS[ynow][xnow]
        letter_multi = (1 if is_letter(sq) else  # if it's already a letter 
                        3 if b == TL else    #means someone else place it, I dont get
                        2 if b == DL else    #bonus only original points
                        1)
        word_multi *= (1 if is_letter(sq) else 
                       3 if b == TW else
                       2 if b in (DW, '*') else
                       1)
        total += POINTS[L] * letter_multi     # cross_word_score recursive call calculate score 
        if isinstance(sq, anchor) and sq != ANY and direction != Y: #so restrict direction,wont get  infinite loop
            crosstotal += cross_word_score(board, L, (x, y), other_direction) 
    return total * word_multi + crosstotal
"""
0 1 2 3 4 5 6 7 8 9 10 ..........(x->)
| | | | | | | | | | | | | | | | | 0
| J . . 3 . . ; . ; . . 3 . I . | 1
| A . : . . 2 B E . C . . : D . | 2 # if we place letter at *, we score xdirction
| G U Y . : . * F . H : . . L . | 3 # and Y direction
| | | | | | | | | | | | | | | | | 4  """ 
                                # Y

def cross_word_score(board, L, pos, direction):
    x, y = pos
    ynow, w = find_cross_words(board, x, y)#this return '.letter', or 'letters'
    return calculate_score(board, (x, ynow), direction, w.replace('.', L))

# from the board above (x=1, y=2) => JAG, (x=2, y=2) => '.U' 
def find_cross_words(board, x, y):
    sq = board[y][x]
    word = sq if is_letter(sq) else '.'
    for y1 in range(y, 0, -1):
        sq1 = board[y1-1][x]
        if is_letter(sq1): word = sq1 + word
        else: break
    for y2 in range(y+1, len(board)):
        sq2 = board[y2][x]
        if is_letter(sq2): word = word + sq2
        else: break
    return y1, word  

def xplays(hand, board):    #each row -> horizontal -> xplays
    results = set()         #each column -> y 
    for (y, row) in enumerate(board[1:-1], 1):
        set_anchors(row, y, board)
        for x, word in row_plays(hand, row):
            score = calculate_score(board, (x, y), X, word)
            results.add((score, (x, y), word)) 
    return results

def xyplays(hand, board):
    xs = xplays(hand, board)
    ys = xplays(hand, tranpose(board))
    return (set((score, (x, y), X, word) for score, (x, y), word in xs) |
            set((score, (y, x), Y, word) for score, (x, y), word in ys))
     # X horizontal = (1, 0), Y = Vertical = (0, 1)

"""
transpose([[1,2,3,4,5],        [[1, 6, 3, 12, 20],
          [6,7,8,9,10],        [2, 7, 6, 13, 21],
          [3,6,4,0,9],         [3, 8, 4, 14, 22],
          [12,13,14,15,16],     [4, 9, 0, 15, 23],
         [20,21,22,23,24]])    [5, 10, 9, 16, 24]] """ 
# letter only allow to be place at json of letters on board
# we call it anchors
def set_anchors(row, y, board):
    for x, sq in enumerate(row[1:-1], 1):
        if is_empty(sq):
            neighborlists = (N, S, E, W) = neighbors(board, x, y)
            if any(map(is_letter, neighborlists)): 
                if is_letter(N) or is_letter(S):
                    y2 ,w = find_cross_words(board, x, y)
                    row[x] = anchor(L for L in LETTERS if w.replace('.', L) in WORDS)
                else:
                    row[x] = ANY 

def neighbors(board, x, y):
    return [board[y-1][x], board[y+1][x],
            board[y][x+1], board[y][x-1]]

#put word on the board
def make_play(play, board):
    ((score, (x, y), (xi, yi), word)) = play
    for (n, L) in enumerate(word):
        board[y+n*yi][x+n*xi] = L
    return board

def best_play(hand, board):
    plays = xyplays(hand, board)
    return sorted(plays)[-1] if plays else None

#-------draw boards and bonus template---------

def bonus_template(quad):
    return mirror(map(mirror, quad.split()))
          #mirrow upside down   (#mirror to the right)

def mirror(seq): return seq + seq[-2::-1]   # middle piece is the same
# [1,2,3,4,5] => [1,2,3,4,5,4,3,2,1]
"""
||||||||| |
|...3..;.
|..:..2..
|.:..:...
|3..;...2 |mirror => to the right,
|..:...:.
|.2...;..
|;...:... |
"""      

#------------------ thoughts ---------------------
def old_add_suffixes(hand, pre='', results=set()):
    if pre in WORDS: results.add(pre)
    if pre in PREFIXES:
        for L in hand:
            old_add_suffixes(removed(hand, L), pre+L, results)
    return results

def word_plays(hand, board_letters, results=set()):
    for pre in find_prefixes(hand): 
        for L in board_letters:
            old_add_suffixes(removed(hand, pre), pre+L, results)
    return results

def longest(hand, board_letters):
    words = word_plays(hand, board_letters)
    return sorted(words, key=len, reverse=True)

def word_score(word):
    return sum(POINTS.get(L) for L in word)

def top_score_words(hand, board_letters, n=10):
    words = word_plays(hand, board_letters)
    return sorted(words, reverse=True, key=word_score)[n:]
#------------------thoughts end------------------------------ 

# tests

a_hand = 'ABCEHKN'

def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])
def show(board):
    print ('\n'.join(
          ' '.join([sq if (is_letter(sq) or sq is '|') else BONUS[y][x]
                   for x, sq in enumerate(rows)])
           for y, rows in enumerate(board)))

def show_best_hand(hand, board):
    print 'Current board: '
    show(board)
    play = best_play(hand, board)
    if play:
        print '\n  TALA! %r scores %d' % (play[-1], play[0])
        show(make_play(play, board)) 
    else:
        print 'no.....dude'

""" show_best_hand(a_hand, a_board())
Current board: 
| | | | | | | | | | | | | | | | |
| J . . 3 . . ; . ; . . 3 . I . |
| A . : . . 2 B E . C . . : D . |
| G U Y . : . . F . H : . . L . |
| | | | | | | | | | | | | | | | |

  TALA! 'BACKBENCH' scores 64
| | | | | | | | | | | | | | | | |
| J . . 3 . . ; . ; . . 3 . I . |
| A . B A C K B E N C H . : D . |
| G U Y . : . . F . H : . . L . |
| | | | | | | | | | | | | | | | |
""" 
word_with_friends = bonus_template(
"""
|||||||||
|...3..;.
|..:..2..
|.:..:...
|3..;...2
|..:...:.
|.2...;..
|;...:...
|...2...*
""")

BONUS = word_with_friends

a_row = ['|', 'A', mnx, moab, '.', '.', ANY, 'B', 'E', ANY, 'C', ANY, '.', ANY,
         'D', ANY, '|']
    




