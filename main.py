from indexation.indexeur import Indexeur
from interface.app import Interface


def main():
    print("Démarrage du système SRI...")

    # Build the index
    index = Indexeur(dossier="collections")
    index.construire()

    print(f"{len(index.docs)} documents indexés.")

    # Launch the interface
    Interface(index)


if __name__ == "__main__":
    main()