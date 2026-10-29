# SalesReport — Analyse de ventes CSV

Outil en ligne de commande pour compter les unités, calculer le chiffre d’affaires et classer les produits par revenu. Données d’exemple fictives.

## Utilisation

Python 3.11+, bibliothèque standard uniquement. Depuis ce dossier :

```sh
python3 report.py example.csv
python3 report.py example.csv --output resultat.json
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Résultat attendu pour l’exemple : **6 unités, 17.10 de revenu**, dont 13.50 pour Carnet et 3.60 pour Stylo. La devise n’est pas déduite automatiquement : un fichier doit contenir une seule devise.

## Format et validation

Colonnes : `date,product,quantity,unit_price`. Les produits contenant une virgule doivent être entourés de guillemets CSV. Quantités entières positives, prix finis positifs ou nuls, au maximum deux décimales. Un fichier invalide provoque une erreur explicite avec le numéro de ligne, sans produire de rapport partiel.

`Decimal` évite les approximations binaires dans les montants. Le lecteur CSV gère les champs cités et le BOM UTF-8. Les dates sont conservées en entrée mais ne servent pas au calcul et ne sont pas validées dans cette version.

## À approfondir

Ajouter une validation des dates, des filtres par période, les retours clients et un export graphique. Les données sont traitées ligne par ligne ; les totaux par produit restent en mémoire.

Créé avec assistance IA ; à reprendre et approfondir personnellement.
