def Dj(G,a):
    first_entry = (0,a)
    heap = [first_entry]
    dist_so_far = {a:first_entry}
    final_dist = {}
    location ={first_entry:0}
    while len(dist_so_far)>0:
        dist,node = heap_pop_min(heap,location)
        final_dist[node] = dist
        del dist_so_far[node]
        for x in G[node]:
            if x in final_dist:
                continue
            new_dist = G[node][x] + final_dist[node][0]
            new_entry = (new_dist,x)
            if x not in dist_so_far:
                insert_heap(heap,new_entry,location)
                dist_so_far[x] = new_entry
            elif new_entry < dis_so_far[x]:
                decrease_val(heap,location,dist_so_far[x],new_entry)
                dist_so_far[x] = new_entry
    return final_list

def left(i):  return 2*i + 1
def right(i): return 2*i + 2. 

def swap(heap, old, new, location):
    location[heap[old]] = new
    location[heap[new]] = old
    (heap[old], heap[new]) = (heap[new], heap[old])

def down_heap(heap,i,location):
    while True:
        l = left(i)
        r = right(i)
        if l > len(heap):
            break
        lv = heap[l][0]
        iv = heap[i][0]

        if r == len(heap):
            if iv>lv:
                swap(heap,i,l,location)
            break
        rv = heap[r][0]
        if min(rv,lv) >= iv:
            break
        if lv<rv: 
            swap(heap,i,l,location)
            i = l
        else:
            swap(heap,i,r,location)
            i = r
        
def up_heap(heap,i,location):
    while i>0:
        p = (i-1)/2
        if heap[i][0]<heap[p][0]:
            swap(heap,i,p,location)
            i=p
        else:
            break

def heap_pop_min(heap,location):
    v = heap[0]
    new_top = heap.pop()
    heap[0] = new_top
    location[v] = None
    if len(heap) == 0:
        return v
    location[new_top] = 0
    down_heap(heap,0,location)
    return v

def insert_heap(heap,v,location):
    heap.append(v)
    location[v] = len(heap) -1
    up_heap(heap, location[v], location)

def decrease_val(heap,locatino,old_val,new_val):
    i = location[old_val]
    heap[i] = new_val
    location[old_val] = None
    location[new_val] = i 
    up_heap(heap,i,location)
