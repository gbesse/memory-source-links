# Memory Source Links

**Mantenga citas breves de memoria como `f3` resolubles cuando desaparezca el contexto original.**

[English](README.md) · [Français](README.fr.md) · Español

## Ver el problema con un comando

```sh
python3 receipt.py demo --lang es
```

El ejemplo resuelve `f1` y `o2`, y muestra que `f3` no tiene recibo. El código 1 indica una cita sin resolver.

## Proyectos cercanos

- [vectorize-io/hindsight](https://github.com/vectorize-io/hindsight/issues/4876) — Informa de alias `f3/o2` sin resolver en un informe de memoria; motiva recibos duraderos.
- [Quarktex/citegate](https://github.com/Quarktex/citegate) — Trata procedencia de citas más amplia; esta herramienta solo verifica un mapa de alias proporcionado. Sin afiliación.

## Usarlo con sus datos

```sh
python3 receipt.py build --facts fixtures/facts.json --out receipt.json
python3 receipt.py verify --report fixtures/report.md --receipt receipt.json --lang es
```

Capture una lista explícita `{alias,id,source_url?,text?}` al crear el informe; `build` guarda ID y hashes opcionales, no el texto completo. `verify` busca referencias `fN`/`oN` y señala los alias ausentes.

## Alcance y límites

Hindsight aún no expone una tabla completa de alias a ID para el caso comunicado; el llamante debe aportar la tabla al crear el informe. No puede reconstruir una correspondencia ya perdida ni afirma integración automática con Hindsight.

## Pruebas

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+. Licencia MIT. La demo no requiere cuenta ni clave API.
