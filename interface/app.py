import tkinter as tk
from tkinter import ttk
import os
import sys

# These imports depend on your local folder structure
try:
    from indexation.indexeur import Indexeur
    from models.modele_classique import BooleenClassique
    from models.modele_etendu import ModeleEtendu
    from models.modele_lukasiewicz import ModeleLukasiewicz
    from models.modele_kraft import ModeleKraft
    from models.vectoriel import ModeleVectoriel
except ImportError:
    # Fallbacks for demonstration if imports are missing
    pass


def open_document(filepath):
    """Opens the document with the system's default application."""
    if sys.platform == "win32":
        os.startfile(filepath)
    elif sys.platform == "darwin":
        os.system(f"open '{filepath}'")
    else:
        os.system(f"xdg-open '{filepath}'")


class Interface:
    def __init__(self, index):
        self.index = index

        # Color Palette - Modern White Theme
        self.COLORS = {
            "bg_main": "#F8F9FA",  # Light gray background
            "bg_card": "#FFFFFF",  # Pure white for content
            "primary": "#4F46E5",  # Indigo/Blue for buttons
            "primary_hover": "#4338CA",
            "text_main": "#1F2937",  # Near black for readability
            "text_light": "#6B7280",  # Gray for secondary info
            "accent": "#10B981",  # Green for scores
            "border": "#E5E7EB"  # Light border
        }

        self.modeles = {
            "Booléen Classique": BooleenClassique(),
            "Booléen Étendu": ModeleEtendu(),
            "Lukasiewicz": ModeleLukasiewicz(),
            "Kraft": ModeleKraft(),
            "Cosine": ModeleVectoriel("cosine"),
            "Dice": ModeleVectoriel("dice"),
            "Jaccard": ModeleVectoriel("jaccard"),
            "Overlap": ModeleVectoriel("overlap"),
            "Euclidienne": ModeleVectoriel("euclidean"),
            "Produit Scalaire": ModeleVectoriel("dot"),
        }

        self.root = tk.Tk()
        self.root.title("SRI - Engine")
        self.root.geometry("1000x800")
        self.root.configure(bg=self.COLORS["bg_main"])

        # Configure TTK styles for a flatter, modern look
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TCombobox", fieldbackground="white", background=self.COLORS["border"])

        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        # ── Header ─────────────────────────────────────────────
        header = tk.Frame(self.root, bg=self.COLORS["bg_card"], height=80,
                          highlightthickness=1, highlightbackground=self.COLORS["border"])
        header.pack(side=tk.TOP, fill=tk.X)
        header.pack_propagate(False)

        tk.Label(
            header, text="RECHERCHE D'INFORMATION",
            font=("Segoe UI", 16, "bold"),
            bg=self.COLORS["bg_card"], fg=self.COLORS["primary"]
        ).pack(side=tk.LEFT, padx=30)

        # ── Search Section ─────────────────────────────────────
        search_container = tk.Frame(self.root, bg=self.COLORS["bg_main"])
        search_container.pack(pady=30, padx=50, fill=tk.X)

        # Search Bar Wrapper (for rounded look effect)
        search_frame = tk.Frame(search_container, bg="white", padx=10, pady=5,
                                highlightthickness=1, highlightbackground=self.COLORS["border"])
        search_frame.pack(fill=tk.X)

        self.entry = tk.Entry(
            search_frame, width=50,
            font=("Segoe UI", 14),
            bg="white", fg=self.COLORS["text_main"],
            relief="flat", borderwidth=0
        )
        self.entry.pack(side=tk.LEFT, padx=10, pady=5, expand=True, fill=tk.X)
        self.entry.bind("<Return>", lambda e: self.chercher())

        btn_search = tk.Button(
            search_frame, text="Rechercher",
            font=("Segoe UI", 11, "bold"),
            bg=self.COLORS["primary"], fg="white",
            activebackground=self.COLORS["primary_hover"],
            activeforeground="white",
            relief="flat", padx=25, pady=8,
            cursor="hand2", command=self.chercher
        )
        btn_search.pack(side=tk.RIGHT)

        # ── Model Selection (Dropdown for cleaner UI) ──────────
        options_frame = tk.Frame(search_container, bg=self.COLORS["bg_main"])
        options_frame.pack(fill=tk.X, pady=15)

        tk.Label(
            options_frame, text="Modèle de calcul : ",
            font=("Segoe UI", 10), bg=self.COLORS["bg_main"], fg=self.COLORS["text_light"]
        ).pack(side=tk.LEFT)

        self.modele_var = tk.StringVar(value="Cosine")
        model_dropdown = ttk.Combobox(
            options_frame, textvariable=self.modele_var,
            values=list(self.modeles.keys()), state="readonly", width=25
        )
        model_dropdown.pack(side=tk.LEFT, padx=5)

        # ── Status ─────────────────────────────────────────────
        self.status_var = tk.StringVar(value="Prêt pour la recherche")
        tk.Label(
            self.root, textvariable=self.status_var,
            font=("Segoe UI", 9), bg=self.COLORS["bg_main"], fg=self.COLORS["text_light"]
        ).pack(anchor="w", padx=55)

        # ── Results Area ───────────────────────────────────────
        results_frame = tk.Frame(self.root, bg="white", highlightthickness=1,
                                 highlightbackground=self.COLORS["border"])
        results_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=(10, 40))

        scrollbar = ttk.Scrollbar(results_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.txt = tk.Text(
            results_frame,
            font=("Segoe UI", 11),
            bg="white", fg=self.COLORS["text_main"],
            relief="flat", padx=20, pady=20,
            yscrollcommand=scrollbar.set,
            wrap=tk.WORD,
            spacing1=5,  # spacing between paragraphs
            spacing3=5
        )
        self.txt.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.txt.yview)

        # Refined Tags
        self.txt.tag_config("title", foreground=self.COLORS["primary"], font=("Segoe UI", 12, "bold"))
        self.txt.tag_config("score", foreground=self.COLORS["accent"], font=("Segoe UI", 10, "bold"))
        self.txt.tag_config("excerpt", foreground=self.COLORS["text_light"], font=("Segoe UI", 10))
        self.txt.tag_config("highlight", background="#FEF08A", foreground="#854D0E")  # Yellow highlight
        self.txt.tag_config("separator", foreground=self.COLORS["border"])

    def chercher(self):
        req = self.entry.get().strip()
        if not req: return

        self.txt.config(state=tk.NORMAL)
        self.txt.delete(1.0, tk.END)

        query_terms = req.lower().split()
        modele_nom = self.modele_var.get()
        modele = self.modeles[modele_nom]

        resultats = []
        for doc in self.index.docs:
            score = self._calculer_score(modele, modele_nom, doc, query_terms)
            if score > 0:
                resultats.append((doc, score))

        resultats.sort(key=lambda x: -x[1])
        self.status_var.set(f"{len(resultats)} document(s) trouvé(s) avec {modele_nom}")

        if not resultats:
            self.txt.insert(tk.END, "\n   Aucun document ne correspond à votre requête.", "excerpt")
            self.txt.config(state=tk.DISABLED)
            return

        for i, (doc, score) in enumerate(resultats, 1):
            filepath = os.path.join(self.index.dossier, doc)
            tag_name = f"link_{i}"

            # Title Link
            self.txt.insert(tk.END, f"{doc}\n", ("title", tag_name))
            self.txt.tag_bind(tag_name, "<Button-1>", lambda e, p=filepath: open_document(p))
            self.txt.tag_bind(tag_name, "<Enter>", lambda e: self.txt.config(cursor="hand2"))
            self.txt.tag_bind(tag_name, "<Leave>", lambda e: self.txt.config(cursor="arrow"))

            # Score bar / Value
            self.txt.insert(tk.END, f"Pertinence : {score * 100:.1f}% \n", "score")

            # Excerpt
            extrait = self.index.get_extrait(doc, query_terms)
            self.txt.insert(tk.END, f"{extrait}\n", "excerpt")

            self.txt.insert(tk.END, "─" * 80 + "\n", "separator")

        self._highlight_terms(query_terms)
        self.txt.config(state=tk.DISABLED)

    def _calculer_score(self, modele, modele_nom, doc, query_terms):
        # (Logic remains same as your provided backend)
        try:
            if modele_nom == "Booléen Classique":
                return modele.score(self.index.tokens.get(doc, []), query_terms, "OU")
            elif modele_nom == "Booléen Étendu":
                poids = [self.index.get_poids(t, doc) for t in query_terms]
                return (modele.ou(poids) + modele.et(poids)) / 2
            elif modele_nom in ("Lukasiewicz", "Kraft"):
                poids = [self.index.get_poids(t, doc) for t in query_terms]
                return (modele.et_liste(poids) + modele.ou_liste(poids)) / 2
            else:
                poids_doc = self.index.tfidf.get(doc, {})
                poids_requete = {t: self.index.idf.get(t, 0) for t in query_terms}
                return modele.score(poids_doc, poids_requete)
        except Exception:
            return 0

    def _highlight_terms(self, query_terms):
        for term in query_terms:
            if len(term) < 2: continue
            start = "1.0"
            while True:
                pos = self.txt.search(term, start, stopindex=tk.END, nocase=True)
                if not pos: break
                end = f"{pos}+{len(term)}c"
                self.txt.tag_add("highlight", pos, end)
                start = end

# Note: To run this, you need to instantiate it with your Indexeur object:
# if __name__ == "__main__":
#    idx = Indexeur("path/to/docs")
#    Interface(idx)