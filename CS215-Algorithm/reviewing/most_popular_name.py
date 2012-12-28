

def most_popular_name():
    f = open('names.txt')
    return max([(int(line.split(',')[2]), line.split(',')[0]) 
               for line in f if line.split(',')[1] == 'F'])

#Aadam,M,6
#Aadil,M,14
#Aailiyah,F,5

#----------
#
# Write partition to return a new array with 
# all values less then `v` to the left 
# and all values greater then `v` to the right
#

def partition(L, v):
    p = [v]
    for l in L:
        if l < v:
            p = [l] + p
        elif l > v:
            p.append(l)
    # your code here
    return p

# top n element from list in big(N)
def topk(L, k):
    middle = L[random.randint(0, len(L)-1)]
    left, mid, right = partition(L, middle)
    if len(left) == k:
        return left
    if len(left) > k:
        return topk(left, k)
    if len(left) == k - 1:
        return left + [middle]
    return return left + [middle] + topk(right, k-pos-1)
