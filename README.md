# 📄 SRI — Système de Recherche d'Information
### Mini-Projet TP5 · Département Informatique

### Aperçu de l'interface
![Capture d'écran de l'application](https://i.imgur.com/3d6xxoO.png)
---

## 1. Objectif du Projet

L'objectif est d'implémenter un système complet de recherche d'information (SRI) capable d'indexer plusieurs types de documents et d'appliquer divers modèles de recherche pour répondre aux requêtes utilisateur via une interface graphique interactive.

---

## 2. Fonctionnalités Principales

- **Gestion multi-formats** : Indexation de documents PDF, DOCX, TXT et HTML.
- **Prétraitement complet** : Extraction du texte, mise en minuscules, suppression des mots vides (stopwords) et calcul des poids TF-IDF.
- **Modèles de recherche implémentés** :
  - Booléen classique : ET, OU, NON
  - Booléen étendu : p-norme (p = 2)
  - Booléen flou : Lukasiewicz et Kraft
  - Modèle vectoriel : Cosinus, Dice, Jaccard, Overlap, Euclidienne, Produit scalaire
- **Interface Graphique** : Interface interactive développée avec Tkinter.

---

## 3. Structure du Projet

```
TP5_MINI_PROJET/
├── indexation/               # Modules de traitement des documents
│   ├── extracteur.py         # Extraction texte (PDF, TXT, HTML, DOCX)
│   ├── preprocesseur.py      # Stopwords, stemming
│   └── indexeur.py           # TF-IDF, gestion de l'index
├── modeles/                  # Implémentation des algorithmes de recherche
│   ├── booleen_classique.py  # Modèle booléen : ET, OU, NON
│   ├── booleen_etendu.py     # Modèle booléen étendu (p-norme)
│   ├── flou_lukasiewicz.py   # Modèle flou de Lukasiewicz
│   ├── flou_kraft.py         # Modèle flou de Kraft
│   └── vectoriel.py          # Cosinus, Jaccard, Dice, etc.
├── interface/                # Code de l'interface graphique
│   └── app.py                # Interface Tkinter
├── collections/              # Collection de documents (min. 40)
├── main.py                   # Point d'entrée de l'application
└── README.md                 # Documentation du projet
```

---

## 4. Modèles de Recherche

| Catégorie | Méthodes disponibles |
|---|---|
| Booléen Classique | ET (AND), OU (OR), NON (NOT) |
| Booléen Étendu | p-norme (p = 2) |
| Booléen Flou | Lukasiewicz, Kraft |
| Vectoriel | Cosinus, Dice, Jaccard, Overlap, Euclidienne, Produit scalaire |

---

## 5. Installation et Prérequis

**Python** : Version 3.8 ou supérieure.

**Bibliothèques nécessaires** :

```bash
pip install PyPDF2 pdfminer.six nltk python-docx
```

| Bibliothèque | Rôle |
|---|---|
| `PyPDF2` / `pdfminer` | Lecture des fichiers PDF |
| `nltk` | Stopwords et stemming |
| `tkinter` | Interface graphique (inclus avec Python) |
| `python-docx` | Lecture des fichiers `.docx` |

---

## 6. Utilisation

1. Placez vos documents dans le dossier `collections/`.
2. Lancez l'application :
   ```bash
   python main.py
   ```
3. Dans l'interface :
   - Saisissez votre requête dans le champ de recherche.
   - Sélectionnez le modèle de recherche souhaité.
   - Cliquez sur **Rechercher**.
   - Cliquez sur un résultat pour ouvrir directement le document.


