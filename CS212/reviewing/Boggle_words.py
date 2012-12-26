
B = '|'

def boggle_words(board, mini=3):
    results = set()
    N = size(board)
    
    def extend_path(pre, path):
        if pre in WORDS and len(pre) >= mini:
            results.add(pre)
        if pre in PREFIXES:
            for nindex in neighbors(path[-1], N):
                if nindex not in path and board[nindex] != B:
                    extend_path(pre+board[nindex], path+[nindex])

    for (i, w) in enumerate(board):
        if w != B:
            extend_path(w, [i])
    return results


