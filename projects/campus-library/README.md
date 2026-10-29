# Campus Library — Gestion d’emprunts en SQL

Mini-projet de modélisation relationnelle d’une bibliothèque : adhérents, livres, exemplaires physiques et emprunts. Données exclusivement fictives.

## Exécuter

Python 3.11+ inclut SQLite ; aucun serveur ni paquet supplémentaire n’est requis. Depuis ce dossier :

```sh
python3 demo.py
python3 -m unittest discover -s . -p 'test_*.py' -v
```

La démonstration utilise une base en mémoire, recréée à chaque lancement.

## Modèle

- Un livre possède plusieurs exemplaires.
- Un adhérent peut avoir plusieurs emprunts.
- Chaque emprunt concerne un exemplaire.
- Un index unique partiel interdit deux emprunts ouverts du même exemplaire.

## Requêtes proposées

1. Exemplaires disponibles : un exemplaire sans historique doit aussi apparaître.
2. Emprunts en retard au **29 octobre 2026**, date fixe pour rendre l’exemple reproductible.
3. Nombre d’emprunts par adhérent, en conservant les membres sans emprunt avec une jointure externe.

Les clés étrangères sont activées. Les dates sont du texte ISO `AAAA-MM-JJ`, et les contraintes contrôlent leur ordre, pas la validité complète du calendrier. SQLite n’est pas interchangeable sans adaptation avec tous les autres SGBD.

## À approfondir

Ajouter des réservations, une validation stricte des dates et des transactions pour gérer des opérations plus complexes.

Créé avec assistance IA ; à reprendre et approfondir personnellement.
