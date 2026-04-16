import math

class ModeleEtendu:
    def __init__(self, p=2):
        self.p = p

    def ou(self, poids):
        if not poids:
            return 0
        return (sum(w ** self.p for w in poids) / len(poids)) ** (1/self.p)

    def et(self, poids):
        if not poids:
            return 0
        return 1 - (sum((1 - w) ** self.p for w in poids) / len(poids)) ** (1/self.p)

    def non(self, w):
        return 1 - w