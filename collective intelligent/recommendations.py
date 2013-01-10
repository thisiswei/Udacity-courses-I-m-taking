from math import sqrt

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
      'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
      'The Night Listener': 3.0},
     'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
      'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 3.5},
     'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
      'Superman Returns': 3.5, 'The Night Listener': 4.0},
     'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
      'The Night Listener': 4.5, 'Superman Returns': 4.0,
      'You, Me and Dupree': 2.5},
     'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
      'You, Me and Dupree': 2.0},
     'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
     'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}


def sim_distance(prefs, person1, person2):
    S = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            S[item] = 1
    if len(S) == 0: return 0
    sum_of_squares = sum([pow(prefs[person1][item]-prefs[person2][item], 2)
                         for item in prefs[person1] if item in prefs[person2]])
    return 1/(1+sum_of_squares) # adding 1 dont get division Error

def sim_pearson(prefs, p1, p2):
    S = {}
    for item in prefs[p1]:
        if item in prefs[p2]: S[item] = 1
    n = len(S)
    if not n: return 0
    similars1 = [prefs[p1][k] for k in S]
    similars2 = [prefs[p2][k] for k in S]
    sum1 = sum(similars1)
    sum2 = sum(similars2)
    sum1sq = sum([pow(s, 2) for s in similars1])
    sum2sq = sum([pow(s, 2) for s in similars2])
    psum = sum(x*y for (x,y) in zip(similars1, similars2))
    num = psum - (sum1*sum2/n)
    den = sqrt((sum1sq - pow(sum1, 2)/n) * (sum2sq - pow(sum2, 2)/n))
    if not den: return 0
    return num/den

def topmatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
               for other in prefs if other != person]
    return sorted(scores, reverse=True)[:n]

def getRecommendations(prefs, person, similarity=sim_pearson):
    tm = topmatches(prefs, person, n=5, similarity=sim_pearson)
    notrated = [n for n in prefs[tm[0][1]].keys() 
                if n not in prefs[person]]
    scoreT = [([s*prefs[p].get(n, 0) for s, p in tm], n) 
              for n in notrated]
    S = [a for a, b in tm]
    simT = sum(S)
    scoreAver = [(((sum(s)+simT-S[s.index(0.0)])/(len(s)-s.count(0.0)), m) 
                  if 0.0 in s else
                  ((sum(s)+simT)/len(s), m))
                 for s, m in scoreT]
    return sorted(scoreAver, reverse=True)

def transformdicts(D):
    result = defaultdict(dict)
    for k in D:
        for val in D[k]:
            result[val][k] = D[k][val]
    return result


