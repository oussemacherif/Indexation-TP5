import tkinter as tk
from tkinter import ttk
import os
import sys

from indexation.indexeur import Indexeur
from models.modele_classique import BooleenClassique
from models.modele_etendu import ModeleEtendu
from models.modele_lukasiewicz import ModeleLukasiewicz
from models.modele_kraft import ModeleKraft
from models.vectoriel import ModeleVectoriel


def open_document(filepath):
    if sys.platform == "win32":
        os.startfile(filepath)
    elif sys.platform == "darwin":
        os.system(f"open '{filepath}'")
    else:
        os.system(f"xdg-open '{filepath}'")


class Interface:
    def __init__(self, index):
        self.index = index

        # Initialize all models
        self.modeles = {
            "Booléen Classique": BooleenClassique(),
            "Booléen Étendu":    ModeleEtendu(),
            "Lukasiewicz":       ModeleLukasiewicz(),
            "Kraft":             ModeleKraft(),
            "Cosine":            ModeleVectoriel("cosine"),
            "Dice":              ModeleVectoriel("dice"),
            "Jaccard":           ModeleVectoriel("jaccard"),
            "Overlap":           ModeleVectoriel("overlap"),
            "Euclidienne":       ModeleVectoriel("euclidean"),
            "Produit Scalaire":  ModeleVectoriel("dot"),
        }

        # Build the window
        self.root = tk.Tk()
        self.root.title("SRI - Système de Recherche d'Information")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2e")

        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        # ── Title ──────────────────────────────────────────────
        tk.Label(
            self.root, text="🔍 SRI Recherche",
            font=("Arial", 22, "bold"),
            bg="#1e1e2e", fg="white"
        ).pack(pady=15)

        # ── Search bar ─────────────────────────────────────────
        frame_search = tk.Frame(self.root, bg="#1e1e2e")
        frame_search.pack(pady=5)

        self.entry = tk.Entry(
            frame_search, width=55,
            font=("Arial", 13),
            bg="#2e2e3e", fg="white",
            insertbackground="white"
        )
        self.entry.pack(side=tk.LEFT, padx=5, ipady=6)
        self.entry.bind("<Return>", lambda e: self.chercher())

        tk.Button(
            frame_search, text="Chercher",
            font=("Arial", 12, "bold"),
            bg="#7c3aed", fg="white",
            relief="flat", padx=10,
            command=self.chercher
        ).pack(side=tk.LEFT)

        # ── Model selector ─────────────────────────────────────
        tk.Label(
            self.root, text="Modèle de recherche :",
            font=("Arial", 11),
            bg="#1e1e2e", fg="#aaaaaa"
        ).pack(pady=(10, 2))

        self.modele_var = tk.StringVar(value="Booléen Étendu")
        frame_modeles = tk.Frame(self.root, bg="#1e1e2e")
        frame_modeles.pack()

        for nom in self.modeles:
            tk.Radiobutton(
                frame_modeles, text=nom,
                variable=self.modele_var, value=nom,
                bg="#1e1e2e", fg="white",
                selectcolor="#7c3aed",
                font=("Arial", 10)
            ).pack(side=tk.LEFT, padx=5)

        # ── Status bar ─────────────────────────────────────────
        self.status_var = tk.StringVar(value="")
        tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 10, "italic"),
            bg="#1e1e2e", fg="#888888"
        ).pack(pady=5)

        # ── Results area ───────────────────────────────────────
        frame_results = tk.Frame(self.root, bg="#1e1e2e")
        frame_results.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        scrollbar = tk.Scrollbar(frame_results)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt = tk.Text(
            frame_results,
            font=("Courier", 11),
            bg="#13131f", fg="#e0e0e0",
            relief="flat", padx=10, pady=10,
            yscrollcommand=scrollbar.set,
            cursor="arrow"
        )
        self.txt.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.txt.yview)

        # Text tags
        self.txt.tag_config("title",     foreground="#7c3aed", font=("Courier", 12, "bold"))
        self.txt.tag_config("score",     foreground="#22c55e", font=("Courier", 10))
        self.txt.tag_config("excerpt",   foreground="#cccccc", font=("Courier", 10))
        self.txt.tag_config("highlight", foreground="#facc15", font=("Courier", 10, "bold"))
        self.txt.tag_config("link",      foreground="#60a5fa", font=("Courier", 10, "underline"))
        self.txt.tag_config("separator", foreground="#333355")

    # ── Search logic ───────────────────────────────────────────
    def chercher(self):
        req = self.entry.get().strip()
        if not req:
            return

        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)

        query_terms = req.lower().split()
        modele_nom  = self.modele_var.get()
        modele      = self.modeles[modele_nom]

        resultats = []

        for doc in self.index.docs:
            score = self._calculer_score(modele, modele_nom, doc, query_terms)
            if score > 0:
                resultats.append((doc, score))

        resultats.sort(key=lambda x: -x[1])

        self.status_var.set(
            f"{len(resultats)} résultat(s) — Modèle : {modele_nom}"
        )

        if not resultats:
            self.txt.insert(tk.END, "Aucun résultat trouvé.\n")
            return

        for i, (doc, score) in enumerate(resultats, 1):
            # Document title (clickable)
            filepath = os.path.join(self.index.dossier, doc)
            tag_name = f"link_{i}"
            self.txt.tag_config(
                tag_name,
                foreground="#60a5fa",
                font=("Courier", 11, "underline")
            )
            self.txt.tag_bind(
                tag_name, "<Button-1>",
                lambda e, p=filepath: open_document(p)
            )

            self.txt.insert(tk.END, f"\n{i}. ", "score")
            self.txt.insert(tk.END, doc, (tag_name,))
            self.txt.insert(tk.END, f"  •  Score : {score*100:.1f}%\n", "score")

            # Excerpt
            extrait = self.index.get_extrait(doc, query_terms)
            self.txt.insert(tk.END, f"{extrait}\n", "excerpt")

            # Highlight query terms in the excerpt
            self._highlight_terms(query_terms)

            self.txt.insert(tk.END, "─" * 60 + "\n", "separator")

    def _calculer_score(self, modele, modele_nom, doc, query_terms):
        if modele_nom == "Booléen Classique":
            return modele.score(self.index.tokens.get(doc, []), query_terms, "OU")

        elif modele_nom == "Booléen Étendu":
            poids = [self.index.get_poids(t, doc) for t in query_terms]
            return (modele.ou(poids) + modele.et(poids)) / 2

        elif modele_nom in ("Lukasiewicz", "Kraft"):
            poids = [self.index.get_poids(t, doc) for t in query_terms]
            return (modele.et_liste(poids) + modele.ou_liste(poids)) / 2

        else:
            # Vectoriel models
            poids_doc     = self.index.tfidf.get(doc, {})
            poids_requete = {t: self.index.idf.get(t, 0) for t in query_terms}
            return modele.score(poids_doc, poids_requete)

    def _highlight_terms(self, query_terms):
        for term in query_terms:
            start = "1.0"
            while True:
                pos = self.txt.search(term, start, stopindex=tk.END, nocase=True)
                if not pos:
                    break
                end = f"{pos}+{len(term)}c"
                self.txt.tag_add("highlight", pos, end)
                start = end