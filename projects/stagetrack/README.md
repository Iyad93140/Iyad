# StageTrack — API de suivi de candidatures

API HTTP/JSON locale : créer, consulter, modifier le statut et supprimer une candidature. Les données restent dans SQLite après redémarrage.

## Lancement

Python 3.11+, sans installation de dépendances. Depuis ce dossier :

```sh
python3 app.py --port 8000
```

Dans un autre terminal :

```sh
curl -X POST http://127.0.0.1:8000/applications -H 'Content-Type: application/json' -d '{"company":"Atelier","role":"Stage développement"}'
curl http://127.0.0.1:8000/applications
curl -X PATCH http://127.0.0.1:8000/applications/1 -H 'Content-Type: application/json' -d '{"status":"entretien"}'
curl -X DELETE http://127.0.0.1:8000/applications/1
python3 -m unittest discover -s . -p 'test_*.py' -v
```

Sous PowerShell, utiliser `curl.exe` et adapter les guillemets, ou un client HTTP tel que Postman.

## Architecture et choix

- `Store` isole les requêtes SQLite de la couche HTTP.
- Requêtes paramétrées pour traiter les valeurs comme des données.
- Validation des champs, statuts et taille du corps ; erreurs JSON en 400/404.
- Connexion SQLite par opération pour éviter de partager une connexion entre threads.

Les tests couvrent le parcours HTTP complet, la persistance, les erreurs et un texte ressemblant à une injection SQL.

## Limites et prochaines étapes

Projet pédagogique **local**, sans authentification ni interface web. Le serveur standard Python n’est pas prévu pour une mise en production. Améliorations proposées : filtres, historique des statuts, pagination, interface et authentification.

Créé avec assistance IA ; à reprendre et approfondir personnellement.
