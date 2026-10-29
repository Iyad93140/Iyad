# Veltrades — Aperçu open source du replay

Un petit extrait du **véritable prototype Veltrades**, mon projet personnel en cours de plateforme de journal de trading et d’entraînement sur graphiques historiques.

Ce dossier publie uniquement les fonctions temporelles du replay, leurs tests et un exemple autonome. Il ne contient pas le produit complet.

## Ce qui est partagé

- `dist/replay-core.js` : module original, extrait sans modification de l’export v17.
- `tests/replay-core.cjs` : tests d’origine, conservés sans modification.
- `example.cjs` : exemple ajouté pour rendre cet extrait facile à essayer.
- `LICENSE` : licence MIT applicable uniquement au contenu de ce dossier.

L’interface complète, le journal, le moteur d’ordres et les autres composants de Veltrades ne sont pas inclus et ne sont pas placés sous cette licence.

## Lancer en moins d’une minute

Node.js 18 ou plus récent, aucune dépendance à installer. Depuis ce dossier :

```sh
npm test
npm run demo
```

Sans npm :

```sh
node tests/replay-core.cjs
node example.cjs
```

La démo affiche deux bougies de 5 minutes à partir de sept bougies source de 1 minute. La seconde bougie agrégée est donc encore partielle. Les valeurs sont **synthétiques**, pas des données de marché ni des résultats de trading.

## Fonctions proposées

| Fonction | Rôle |
| --- | --- |
| `localParts(time, zone)` | Jour de la semaine et minute locale depuis un instant UTC |
| `minute("09:50")` | Conversion d’une heure en minutes depuis minuit |
| `matches(time, window, zone)` | Test d’appartenance à un créneau local avec jours configurés |
| `aggregate(bars, timeframe)` | Agrégation OHLC sur les bougies fournies |
| `demo()` | Génération déterministe de 600 bougies synthétiques |

Les timestamps sont exprimés en **secondes Unix**. Les jours vont de 0 (dimanche) à 6 (samedi). Les créneaux incluent leur début et excluent leur fin. Un créneau nocturne est rattaché au jour de son début. Un créneau dont début et fin sont identiques est désactivé.

## Choix techniques et limites

Les instants UTC restent inchangés. `Intl.DateTimeFormat` applique le fuseau pour le calcul des créneaux, y compris lors des changements d’heure. Les tests vérifient notamment New York en heure d’été et en heure d’hiver, les bornes et les créneaux nocturnes.

L’agrégation utilise des blocs alignés sur UTC. Elle conserve l’ouverture initiale, le maximum, le minimum et la dernière clôture. Elle n’interpole pas les trous et ne calcule pas de volume.

**Le code appelant doit fournir seulement les bougies déjà révélées au replay.** La fonction d’agrégation n’impose pas cette règle : passer toute la série révélerait le futur. Les tests utilisent un préfixe et vérifient que les données source ne sont pas modifiées.

Ce petit module suppose des bougies triées, des OHLC valides, une unité positive et des paramètres horaires corrects. La validation du prototype complet est située dans d’autres composants, non publiés ici. Ce n’est pas un moteur d’exécution d’ordres ni un composant prêt à exposer à des entrées non fiables sans validation.

## Provenance

Extrait de `Veltrades_Code_Complet_v17.zip`, export du prototype v17, dont le manifeste indique le commit source `c251059a4ecc7f876d66bace05c3605c8da1c2cb`. Le développement du prototype utilise une assistance IA. Cet aperçu n’implique aucune affiliation avec TradingView, une bourse ou un broker.

[Profil d’Iyad](https://github.com/Iyad93140) · [Index des projets](../../README.md)
