singles = range(1, 21) + [25]
doubles = range(2, 41, 2) + [50]
points = range(3,61,3) + singles + doubles 
points = [0] + sorted(points, reverse=True)

#20  => [0,  0,  20] => [D10]
#100 => [0,  60, 40] => [T20, D20]
#170 => [60, 60, 50] => [T20, T20, DB]

def double_out(total):
    if total > 170 or not find(total): 
        return None
    return filter(lambda s: s, find(total))
    
def find(target):
    return next([name(x), name(y), name(target-(x+y), 1)] 
                for x in points 
                for y in points 
                if target-(x+y) in doubles, None) 

def name(n, last=0): 
    if n: return (['D%s' % (n/2), 'DB'][n == 50]) if last else sdt(n)

def sdt(n): #single, double, tre
    if n in singles: return 'S%s' % n if n < 21 else 'SB'
    return (('DB') if n == 50 else
            ('D%s' % (n/2)) if n in doubles else 
            ('T%s' % (n/3)))


n = '20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5'.split()

def outcome1(target, miss):
    results = {}
    if not miss:
        return dict(target=1.0)

    miss = (min(miss*3, 1) if target == 'DB' else
            miss/5. if 'S' in target and 'B' not in target else
            miss) 

    hit = 1-miss
    right_on = hit**2
    results[target] = right_on     

    if 'B' in target:
        keys = ['S'+str(i) for i in range(1, 21)]
        bkeys =(keys + ['DB'] if target == 'SB' else
                keys + ['SB'])
        for key in bkeys:
            hit_b = (miss * 1/4. * hit if target == 'SB' else
                     miss * 1/3. * hit)
            if 'B' in key:
                results[key] = hit_b
            else: results[key] = ((1-right_on)-hit_b)/20
        return results

    rs, sr, both = find_miss(target, miss)
    miss_one, miss_both = miss * hit, miss**2 

    for x in rs:
        if 'OFF' not in x: results[x] = miss_one/len(rs) #miss ring, not section
    for y in sr: 
        if 'OFF' not in y: results[y] = miss_one/len(sr) #miss section,not ring
    for z in both:
        if 'OFF' not in z: results[z] = miss_both/len(both)     #miss both section,and ring:
    if 'D' in target:
        results['OFF'] = miss/2.
    return results

def find_miss(target, miss): 
    R, S = target[0], target[1:] 

    rings = (['S'] if R == 'T' else
             ['S', 'OFF'] if R == 'D' else
             ['D', 'T']) 
    sections = find_neighbor(''.join(S))

    got_section =[r+s for r in rings for s in [S]]
    got_ring = [r+s for r in [R] for s in sections]
    miss_both = [r+s for r in rings for s in sections]

    return (got_section, got_ring, miss_both)

def find_neighbor(s): 
    pos = n.index(s)
    left = (pos - 1) % 20
    right = (pos + 1) % 20
    return n[left], n[right]



