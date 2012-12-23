



singles = range(1, 21) + [25]
doubles = range(2, 41, 2) + [50]
points = range(3,61,3) + singles + doubles 
points = [0] + sorted(points, reverse=True)

#20  => [0,  0,  20] => [D10]
#100 => [0,  60, 40] => [T20, D20]
#170 => [60, 60, 50] => [T20, T20, DB]

def double_out(total):
    if total > 170 or not find(total): return None
    return filter(lambda s: s, find(total))
    
def find(target):
    try:
        return next([name(x), name(y), name(target-(x+y), 1)] 
                    for x in points 
                    for y in points 
                    if target-(x+y) in doubles) 
    except StopIteration:
        return None

def name(n, last=0): 
    if n: return (['D%s' % (n/2), 'DB'][n == 50]) if last else sdt(n)

def sdt(n): #single, double, tre
    if n in singles: return 'S%s' % n if n < 21 else 'SB'
    return (('DB') if n == 50 else
            ('D%s' % (n/2)) if n in doubles else 
            ('T%s' % (n/3)))




