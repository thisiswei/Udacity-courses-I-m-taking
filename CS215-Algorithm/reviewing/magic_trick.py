
#            animal       speed   weight lifespan brain
#                          (mph)   (kg)  (years) mass (g)
animals = [("dog",          46,   35,     13,  280    ),
           ("elephant",     30, 3500,     50, 6250    ),
           ("frog",          5,    0.5,    8,    3    ),
           ("hippopotamus", 45, 1600,     45,  573    ),
           ("horse",        40,  385,     30, 642     ),
           ("human",        27,   80,     78, 2000    ),
           ("lion",         50,  250,     30,  454    ),
           ("mouse",         8,    0.025,  2,    0.625),
           ("rabbit",       25,    4,     12,   40    ), 
           ("shark",        26,  230,     20,   92    ),
           ("sparrow",      16,    0.024,  7,    2    )]
answer = importance_rank(animals, (1.3,.2,.5,2))

def importance_rank(items, weights):
    names = [i[0] for i in items]
    scores = [sum([a*b for (a, b) in zip(item[1:], weights)]) for item in items]
    results = zip(scores, names)
    return sorted(results)

