# Memory Source Links

**Gardez les citations courtes de mémoire comme `f3` résolubles après la disparition du contexte source.**

[English](README.md) · Français · [Español](README.es.md)

## Voir le problème en une commande

```sh
python3 receipt.py demo --lang fr
```

La fixture résout `f1` et `o2`, puis montre que `f3` n’a pas de reçu. Le code 1 signale une citation introuvable.

## Projets voisins

- [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/issues/4876) — Signale des alias `f3/o2` introuvables dans un rapport de mémoire ; cette issue motive les reçus durables.
- [Quarktex/citegate](https://github.com/Quarktex/citegate) — Traite une provenance de citations plus large ; cet outil vérifie seulement une table d’alias fournie. Aucune affiliation.

## Utiliser vos données

```sh
python3 receipt.py build --facts fixtures/facts.json --out receipt.json
python3 receipt.py verify --report fixtures/report.md --receipt receipt.json --lang fr
```

Capturez une liste explicite `{alias,id,source_url?,text?}` pendant la création du rapport ; `build` conserve les ID et d’éventuelles empreintes, pas le texte complet. `verify` recherche les références `fN`/`oN` dans le rapport et signale les alias manquants.

## Périmètre et limites

Hindsight n’expose pas encore une table alias→ID complète pour le cas signalé ; l’appelant doit fournir cette table à la création. L’outil ne peut pas reconstruire une correspondance déjà perdue et ne revendique pas d’intégration Hindsight automatique.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. Licence MIT. La démo ne demande ni compte ni clé API.
