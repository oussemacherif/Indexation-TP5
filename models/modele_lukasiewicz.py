class ModeleLukasiewicz:
    def et_liste(self, poids):
        if not poids:
            return 0
        r = 1
        for w in poids:
            r *= w
        return r

    def ou_liste(self, poids):
        if not poids:
            return 0
        r = 0
        for w in poids:
            r = r + w - r * w
        return r

    def non(self, w):
        return 1 - w