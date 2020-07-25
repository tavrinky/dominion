

class Logger(object):
    
    def __init__(self):
        self.log = []

    def add(self, t):
        self.log.append(t)

    def addMany(self, *ts):
        self.log.extend(ts)

    def __str__(self):
        "".join(map(str, self.log))


    def attemptBuy(p, card):
        self.addMany(p.name, " is attempting to buy ", str(card), "\n")

    def beginAction(p, card):
        self.addMany(p.name, " is attempting to use ", str(card), "\n") 
