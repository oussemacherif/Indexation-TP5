import math

class ModeleVectoriel:
    def __init__(self, methode="cosine"):
        self.methode = methode  # cosine, dice, jaccard, overlap, euclidean, dot

    def score(self, poids_doc, poids_requete):
        d = poids_doc
        q = poids_requete

        if self.methode == "cosine":
            dot = sum(d[t] * q.get(t, 0) for t in d)
            norm_d = math.sqrt(sum(v**2 for v in d.values()))
            norm_q = math.sqrt(sum(v**2 for v in q.values()))
            return dot / (norm_d * norm_q) if norm_d * norm_q else 0

        elif self.methode == "dot":
            return sum(d.get(t, 0) * q.get(t, 0) for t in q)

        elif self.methode == "dice":
            dot = sum(d.get(t, 0) * q.get(t, 0) for t in q)
            norm_d = sum(v**2 for v in d.values())
            norm_q = sum(v**2 for v in q.values())
            return (2 * dot) / (norm_d + norm_q) if (norm_d + norm_q) else 0

        elif self.methode == "jaccard":
            dot = sum(d.get(t, 0) * q.get(t, 0) for t in q)
            norm_d = sum(v**2 for v in d.values())
            norm_q = sum(v**2 for v in q.values())
            denom = norm_d + norm_q - dot
            return dot / denom if denom else 0

        elif self.methode == "overlap":
            dot = sum(d.get(t, 0) * q.get(t, 0) for t in q)
            min_norm = min(
                sum(v**2 for v in d.values()),
                sum(v**2 for v in q.values())
            )
            return dot / min_norm if min_norm else 0

        elif self.methode == "euclidean":
            dist = math.sqrt(sum((d.get(t, 0) - q.get(t, 0))**2 for t in q))
            return 1 / (1 + dist)

        return 0