#
# Given a list L of n numbers, find the mode 
# (the number that appears the most times).  
# Your algorithm should run in Theta(n).
# If there are ties - just pick one value to return 



def mode(L):
    l = list(set(L))
    mode = l[0]
    max_count = 1
    for element in l:
        count = L.count(element)
        if count > max_count:
            max_count = count
            mode = element
    return mode
