class ModeleKraft:
    def et_liste(self, poids):
        return min(poids) if poids else 0

    def ou_liste(self, poids):
        return max(poids) if poids else 0

    def non(self, w):
        return 1 - w