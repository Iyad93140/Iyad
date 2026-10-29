# FocusBoard — Tableau de tâches local

Application web en français avec trois colonnes, création et suppression de tâches, changement de statut, recherche et sauvegarde dans le navigateur. Sans framework ni service externe.

## Lancer

Depuis ce dossier :

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

Ouvrir **http://127.0.0.1:8080** dans un navigateur récent. Utiliser le serveur local plutôt qu’un double-clic sur le HTML, car le navigateur doit charger des modules JavaScript. L’identifiant des tâches utilise `crypto.randomUUID`, disponible sur localhost dans les navigateurs récents.

Tests des règles métier, avec Node.js 20+ :

```sh
node --test test_core.mjs
```

## Parcours de démonstration

1. Ajouter « Préparer mon entretien ».
2. Passer la tâche de « À faire » à « En cours », puis « Terminé ».
3. Rechercher « entretien » ; recharger la page pour vérifier la persistance.
4. Supprimer la tâche.

## Architecture

`core.mjs` porte la validation, les transitions et le filtrage ; `app.mjs` gère le DOM et le stockage. Les titres sont insérés avec `textContent`, sans interprétation HTML. Le stockage restauré est validé, avec contrôle des identifiants dupliqués. Une sauvegarde invalide n’est pas écrasée automatiquement.

Libellés de formulaire, boutons nommés, focus visible et message d’état sont présents. L’affichage est adapté aux petits écrans. Les tests automatisés couvrent les règles métier, pas une validation complète de l’interface ou de l’accessibilité.

## Limites et suites

Stockage local à ce navigateur, aucune synchronisation, pas de comptes. Une suppression est immédiate. À ajouter : annulation, édition du titre, export/import JSON et tests de navigateur.

Créé avec assistance IA ; à reprendre et approfondir personnellement.
