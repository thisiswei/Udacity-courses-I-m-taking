









def anagrams(phrase, previous='', shortest=2):
    return find_ana(phrase.replace(' ',''), '', shortest)


def find_ana(phrase, previous, shortest):
    results = set()
    for w in find_words(phrase): 
        if len(w) >= shortest and w > previous:
            remainder = removed(phrase, w)
            if not remainder:
                results.add(w)
            else:
                for rest in find_ana(remainder, w, shortest):
                    results.add(w+ ' ' + rest) 
    return results  



            

