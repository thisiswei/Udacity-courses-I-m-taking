
POINTS = dict(A = 1, B = 3, C = 3, D = 2, E = 1, F = 4, G = 2, H = 4, I = 1,
              J = 8, K = 5, L = 1, M = 3, N = 1, O = 1, P = 3, Q = 10, R = 1,
              S = 1, T = 1, U = 1, V = 4, W = 4, X = 8, Y = 4, Z = 10, _ = 0)

class anchor(set):
    " use for isinstance(x,anchor) " 

LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
ANY = anchor(LETTERS)
a_hand = 'ABCEHKN'
mnx = anchor('MNX')
moab = anchor('MOAB')
a_row = ['|', 'A', mnx, moab, '.', '.', ANY, 'B', 'E', ANY, 'C', ANY, '.', ANY,
         'D', ANY, '|']

def is_empty(sq):
    return sq == '.' or sq == '*' or isinstance(sq, anchor)

def is_letter(sq):
    return isinstance(sq, str) and sq in LETTERS
 
def prefixes(word):
    return [word[:i] for i in range(len(word))]

def read(filename):
    words = set(file(filename).read().upper().split())
    pres = set(p for word in words for p in prefixes(word))
    return words, pres

WORDS, PREFIXES = read('words4k.txt')

def removed(letters, remove):
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters

def word_score(word):
    sum(POINTS[L] for L in word)

def topn(hand, boardletters, n=10):
    words = word_plays(hand, boardletters)
    return sorted(words, key=word_score, reverse=True)[:n]

def make_play(play, board):
    (score, (i, j), (di, dj), word) = play
    for (n, L) in enumerate(word):
        board[j + n*dj][i + n*di] = L
    return board

def best_play(hand, board):
    plays = all_plays(hand, board)
    return sorted(plays)[-1] if plays else None


def all_plays(hand, board):
    hplays = horizontal_plays(hand, board)          # ((i,j),word)
    vplays = horizontal_plays(hand, transpose(board)) #((j,i),word)
    return (set((score, (i, j), ACROSS, word) for (score, (i, j),word) in hplays) | 
            set((score, (i, j), DOWN, word) for (score, (j, i), word) in vplays))

ACROSS, DOWN = (1, 0), (0, 1)

def horizontal_plays(hand, board):
    " ((i,j), word) pairs across all rows "
    results = set()
    for (j, row) in enumerate(board[1:-1], 1):
        set_anchor(row, j, board)
        for (i, word) in row_plays(hand, row):
            score = calculate_score(board, (i, j), ACROSS, hand, word)
            results.add((score, (i, j), word))
    return results

def calculate_score(board, pos, direction, hand, word):
    total, crosstotal, word_mult = 0, 0, 1
    starti, startj = pos
    di, dj = direction
    other_direction = DOWN if direction == ACROSS else ACROSS
    for (n, L) in enumerate(word):
        i, j = starti + n*di, startj + n*dj
        sq = board[j][i]
        b = BONUS[j][i]
        word_mult *= (1 if is_letter(sq) else
                      3 if b is TW else 2 if b in (DW, '*') else 1)
        letter_mult = (1 if is_letter(sq) else
                       3 if b is TL else 2 if b is DL else 1)
        total += POINTS[L] * letter_mult
        if isinstance(sq, anchor) and sq is not ANY and direction is not DOWN:
            crosstotal += cross_word_score(board, L, (i, j), other_direction)
    return crosstotal + word_mult * total

def cross_word_score(board, L, pos, direction):
    i, j = pos
    (j2, word) = find_cross_word(board, i, j)
    return calculate_score(board, (i, j2), DOWN, L, word.replace('.', L))

def transpose(matrix):
    " [[1,2,3],[3,4,5]] => [1,3],[2,4],[3,5]"
    return map(list, zip(*matrix))

def set_anchor(row, j, board):
    for (i, sq) in enumerate(row[1:-1], 1):
        neighborlist = (N, S, E, W) = neighbors(board, i, j)
        if sq == '*' or (is_empty(sq) and any(map(is_letter, neighborlist))):
            if is_letter(N) or is_letter(S):
                "find cross word"
                (j2, word) = find_cross_word(board, i, j)
                row[i] = anchor(L for L in LETTERS if word.replace('.', L) in WORDS)
                " word = '.u' => anchor(['X', 'M', 'N']) "
            else:
                row[i] = ANY

def find_cross_word(board, i, j):
    """ find vertical word that crosses board[j][i]. 
    return (j2, w) <- j2 is starting row, w is the word """
    sq = board[j][i]
    w = sq if is_letter(sq) else '.'
    for j2 in range(j, 0, -1):
        sq2 = board[j2-1][i]
        if is_letter(sq2): w = sq2 + w
        else: break
    for j3 in range(j+1, len(board)):
        sq3 = board[j3][i]
        if is_letter(sq3): w = w + sq3
        else: break
    return j2, w

def neighbors(board, i, j):
    return [board[j-1][i], board[j+1][i],
            board[j][i+1], board[j][i-1]]

def row_plays(hand, row):
    results = set()
    for (i, sq) in enumerate(row[1:-1], 1):
        if isinstance(sq, anchor):
            pre, maxsize = legal_prefix(i, row)
            if pre:# add letter already on the board
                start = i - len(pre)
                add_suffixes(hand, pre, start, row, results, anchored=False)
            else:
                for pre in find_prefixes(hand):
                    if len(pre) <= maxsize:
                        start = i - len(pre)
                        add_suffixes(removed(hand, pre), pre, start, row,
                                     results, anchored=False)
    return results
 
def legal_prefix(i, row):
    s = i 
    while is_letter(row[s-1]): s -= 1
    if s < i:
        return ''.join(row[s:i]), i-s
    while is_empty(row[s-1]) and not isinstance(row[s-1], anchor): s -= 1
    return ('', i-s)


def word_plays(hand, boardletters):
    results = set()
    prefixes = find_prefixes(hand, '', set())
    for pre in prefixes:
        for L in boardletters:
            add_suffixes(removed(hand, pre), pre+L, results)
    return results

prev_hand , prev_result = '', set()

def find_prefixes(hand, pre='', results=None):
    global prev_hand, prev_result
    if hand == prev_hand: return prev_result
    if results is None: results = set()
    if not pre: prev_hand, prev_result = hand, results  # if pre == '', means it's top level call
    if pre in WORDS or pre in PREFIXES: results.add(pre)   # we will store the compute and store result
    if pre in PREFIXES: 
        for L in hand:
            find_prefixes(hand.replace(L, '', 1), pre+L, results)
    return results

def add_suffixes(hand, pre, start, row, results, anchored = True):
    i = start + len(pre)
    if pre in WORDS and anchored and not is_letter(row[i]): # i will be exact one right to the pre
        results.add((start,pre))                       
    if pre in PREFIXES:
        sq = row[i]
        if is_letter(sq):
            add_suffixes(hand, pre+sq, start, row, results)
        elif is_empty(sq):
            possibilities = sq if isinstance(sq, anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(hand.replace(L, '', 1), pre+L, start, row, results)
    return results

def show(board):
    "print the board"
    for j, row in enumerate(board):
        for i, sq in enumerate(row):
            print (sq if (is_letter(sq) or sq == '|') else BONUS[j][i],
        print

def bonus_template(quadrant):
    " make a board from upper-left quadrant"
    return mirror(map(mirror, quadrant.split()))

def mirror(seq): return seq + seq[-2::-1]  #wont duplicate the middle

WWF = bonus_template("""
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
BONUS = WWF
DW, TW, DL, TL = '23:;'

# thoughts on the begining...
#---------------------------------
#def find_words(letters, pre = '', results=None):
#    if results is None: results = set()
#    if pre in WORDS: results.add(pre)
#    if pre in PREFIXES:
#        for L in letters:
#            find_words(letters.replace(L, '', 1), pre+L, results)
#    return results

#def add_suffixes(hand, pre, results):
#    if pre in WORDS: results.add(pre)
#    if pre in PREFIXES:
#        for L in hand:
#            add_suffixes(hand.replace(L, '', 1), pre+L, results)
#    return results 
 

def find_longest_word(letter,boardletters):
    return sorted(word_plays(letter,boardletters), key=len, reverse=True)




#-----test-----------
def a_board():
    return map(list, ['|||||||||||||||||',
                      '|J............I.|',
                      '|A.....BE.C...D.|',
                      '|GUY....F.H...L.|',
                      '|||||||||||||||||'])
def test():
    assert len(WORDS)    == 3892
    assert len(PREFIXES) == 6475
    assert (word_plays('ADEQUAT', set('IRE')) ==
            set(['DIE', 'ATE', 'READ', 'AIT', 'DE', 'IDEA', 'RET', 'QUID',
                 'DATE', 'RATE', 'ETA', 'QUIET', 'ERA', 'TIE', 'DEAR', 'AID',
                 'TRADE', 'TRUE', 'DEE', 'RED', 'RAD', 'TAR', 'TAE', 'TEAR',
                 'TEA', 'TED', 'TEE', 'QUITE', 'RE', 'RAT', 'QUADRATE', 'EAR',
                 'EAU', 'EAT', 'QAID', 'URD', 'DUI', 'DIT', 'AE', 'AI', 'ED',
                 'TI', 'IT', 'DUE', 'AQUAE', 'AR', 'ET', 'ID', 'ER', 'QUIT',
                 'ART', 'AREA', 'EQUID', 'RUE', 'TUI', 'ARE', 'QI', 'ADEQUATE',
                 'RUT']))
    assert prefixes('hello') == ['', 'h', 'he', 'hel', 'hell']
