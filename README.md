# Ateliers de développement — Iyad Ben Azzoun

Quatre projets pédagogiques exécutables, pour travailler le développement web, Python et SQL pendant ma deuxième année de BUT Informatique.

> Ces bases ont été créées avec une assistance IA en octobre 2026. Elles sont proposées comme supports de pratique à comprendre, modifier et approfondir. Ce ne sont ni des missions clients, ni des travaux universitaires évalués.

| Projet | Technologies | Ce qu’il permet de pratiquer |
| --- | --- | --- |
| [StageTrack](projects/stagetrack) | Python, SQLite, HTTP/JSON | API CRUD, validation des entrées, persistance |
| [FocusBoard](projects/focusboard) | HTML, CSS, JavaScript | Gestion de tâches, filtres, stockage local |
| [SalesReport](projects/salesreport) | Python, CSV, Decimal | Analyse de données, validation, ligne de commande |
| [Campus Library](projects/campus-library) | SQL, SQLite | Modèle relationnel, contraintes, jointures, agrégations |

Chaque dossier contient son code, un README, des exemples et des tests. Aucun service payant ni clé API n’est requis. Python 3.11+ et Node.js 20+ suffisent pour exécuter tous les contrôles.

## Veltrades — projet personnel en cours

Un [aperçu open source du module de replay](projects/veltrades-preview) expose une petite partie du prototype réel : créneaux horaires, fuseaux et agrégation OHLC. Sa licence MIT est limitée à ce dossier ; le reste de Veltrades n’est pas publié ici.

## Vérification globale

Depuis la racine du dépôt :

```sh
python3 -m unittest discover -s projects/stagetrack -p 'test_*.py' -v
python3 -m unittest discover -s projects/salesreport -p 'test_*.py' -v
python3 -m unittest discover -s projects/campus-library -p 'test_*.py' -v
node --test projects/focusboard/test_core.mjs
node projects/veltrades-preview/tests/replay-core.cjs
```

## Pour aller plus loin

1. Lancer un projet et suivre son parcours de démonstration.
2. Lire son architecture et expliquer un choix technique.
3. Réaliser une amélioration de la liste proposée.
4. Ajouter un test de régression puis documenter cette contribution.

## Contact

Étudiant à l’IUT de Villetaneuse — Université Sorbonne Paris Nord. Recherche de stage de **8 à 10 semaines à partir du 8 février 2027**.

[iyad.pro@outlook.fr](mailto:iyad.pro@outlook.fr)
