import os, math
from .extracteur import extract_text
from .preprocesseur import preprocess

EXTENSIONS = {".pdf", ".txt", ".html", ".docx"}

class Indexeur:
    def __init__(self, dossier="collections"):
        self.dossier = dossier
        self.docs = {}       # filename -> raw text (for excerpts)
        self.tokens = {}     # filename -> [words]
        self.tf = {}
        self.idf = {}
        self.tfidf = {}

    def construire(self):
        for fname in os.listdir(self.dossier):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in EXTENSIONS:
                continue
            path = os.path.join(self.dossier, fname)
            try:
                text = extract_text(path)
                self.docs[fname] = text          # keep raw for excerpts
                words = preprocess(text)
                if words:
                    self.tokens[fname] = words
                    self.tf[fname] = self._compute_tf(words)
            except Exception as e:
                print(f"Erreur {fname}: {e}")

        self.idf = self._compute_idf()
        for doc in self.tokens:
            self.tfidf[doc] = {
                t: self.tf[doc][t] * self.idf.get(t, 0)
                for t in self.tf[doc]
            }

    def _compute_tf(self, words):
        tf = {}
        for w in words:
            tf[w] = tf.get(w, 0) + 1
        total = len(words)
        return {w: c/total for w, c in tf.items()}

    def _compute_idf(self):
        N = len(self.tokens)
        idf = {}
        all_terms = set(t for doc in self.tokens.values() for t in doc)
        for t in all_terms:
            df = sum(1 for doc in self.tokens.values() if t in doc)
            idf[t] = math.log(N / (1 + df))
        return idf

    def get_poids(self, terme, doc):
        return self.tfidf.get(doc, {}).get(terme, 0)

    def get_extrait(self, doc, query_terms, nb_lines=2):
        """Return a short excerpt containing query terms"""
        text = self.docs.get(doc, "")
        sentences = text.replace("\n", " ").split(".")
        relevant = [s.strip() for s in sentences
                    if any(t in s.lower() for t in query_terms)]
        excerpt = ". ".join(relevant[:nb_lines])
        return excerpt[:300] if excerpt else text[:300]