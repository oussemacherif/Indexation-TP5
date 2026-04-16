class BooleenClassique:
    """
    Parses simple queries like: 'python ET (data OU machine) NON spam'
    Returns 1.0 or 0.0 per document.
    """
    def score(self, tokens_doc, query_terms, operator="OU"):
        present = set(tokens_doc)
        if operator == "ET":
            return 1.0 if all(t in present for t in query_terms) else 0.0
        elif operator == "OU":
            return 1.0 if any(t in present for t in query_terms) else 0.0
        elif operator == "NON":
            return 1.0 if not any(t in present for t in query_terms) else 0.0
        return 0.0