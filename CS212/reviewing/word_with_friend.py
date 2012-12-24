POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1, J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1, S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10, _=0)
X, Y = (1, 0), (0, 1)

class anchor(set):
    " where word can be place"

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
mnx, moab = anchor(list('MNX')), anchor(list('MOAB'))
ANY = anchor(LETTERS)
a_row = ['|', 'A', mnx, moab, '.', '.', ANY, 'B', 'E', ANY, 'C', ANY, '.', ANY,
         'D', ANY, '|']

a_hand = 'ABCEHKN' 

def is_letter(sq): return isinstance(sq, str) and sq in LETTERS 

def is_empty(sq): return sq == '.' or sq == '*'  or isinstance(sq, anchor)
 
def prefixes(word):
    return [word[:i] for i in range(len(word))]
                                          
def read_words(name):
    words = set(file(name).read().upper().split())
    pres = set(p for word in words for p in prefixes(word))
    return words, pres

WORDS, PREFIXES = read_words('words4k.txt')

prev_hand, prev_results = '', set()  # cache
def find_prefixes(hand, pre='', results=set()):
    global prev_hand, prev_results
    if hand == prev_hand: return prev_results
    if pre == '': prev_hand, prev_results = hand, results
    if pre in PREFIXES:
        results.add(pre)
        for L in hand:
            find_prefixes(removed(hand, L), pre+L, results)
    return results

def removed(letters, remove):
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

def add_suffixes(hand, pre, start, row, results, anchored=True):
    i = start + len(pre)
    if pre in WORDS and anchored and not is_letter(row[i]): 
        results.add((start, pre))
    if pre in PREFIXES:
        sq = row[i]
        if is_letter(sq):
            add_suffixes(hand, pre+sq, start, row, results)
        elif is_empty(sq):
            possibilities = sq if isinstance(sq, anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(removed(hand, L), pre+L, start, row, results)
    return results
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

def row_plays(hand, row):
    "Return a set of legal plays in a row. (start, word) pairs "
    results = set()
    # to each allowable prefix, add all suffixes, keeping the words
    for index, sq in enumerate(row[1:-1], 1): 
        if isinstance(sq, anchor):
            pre, maxsize = legal_prefixes(row, index)
            if pre:
                start = index - len(pre)
                add_suffixes(hand, pre, start, row, results, anchored=False)
            else:
                for pre in find_prefixes(hand):
                    if len(pre) <= maxsize:
                        start = index - len(pre)
                        add_suffixes(removed(hand, pre), pre, start, row,
                                     results, anchored=False)

    return results

def xplays(hand, board):    #each row -> horizontal -> xplays
    results = set()         #each column -> y 
    for (y, row) in enumerate(board[1:-1], 1):
        set_anchors(row, y, board)
        for x, word in row_plays(hand, row):
            results.add(((x, y), word)) 
    return results

def xyplays(hand, board):
    xs = xplays(hand, board)
    ys = xplays(hand, tranpose(board))
    return (set(((x, y), X, word) for (x, y), word in xs) |
            set(((y, x), Y, word) for (x, y), word in ys))
     # X horizontal = (1, 0), Y = Vertical = (0, 1)

def transpose(board):
    return map(list, zip(*board))

"""
transpose([[1,2,3,4,5],        [[1, 6, 3, 12, 20],
          [6,7,8,9,10],        [2, 7, 6, 13, 21],
          [3,6,4,0,9],         [3, 8, 4, 14, 22],
          [12,13,14,15,16],     [4, 9, 0, 15, 23],
         [20,21,22,23,24]])    [5, 10, 9, 16, 24]] """

def legal_prefixes(row, index):
    s = index
    while is_letter(row[s-1]): s -= 1
    if s < index:
        return ''.join(row[s:index]), index - s
    while is_empty(row[s-1]) and not isinstance(row[s-1], anchor):
        s -= 1
    return '', index - s

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

def neighbors(board, x, y):
    return [board[y-1][x], board[y+1][x],
            board[y][x+1], board[y][x-1]]





def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])






