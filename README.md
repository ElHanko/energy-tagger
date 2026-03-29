# energy-tagger

Ein kleines CLI-Tool, das für MP3- und FLAC-Dateien einen einfachen Energy-Score von 1 bis 10 berechnet und als Tag schreibt.

## Funktionen

- Analyse von MP3 und FLAC
- heuristischer Energy-Score
- Schreiben in `COMMENT` oder `GROUPING`
- Dry-Run-Modus

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
Test
pytest
Dry Run
energy-tagger /pfad/zur/musik --recursive --dry-run
In COMMENT schreiben
energy-tagger /pfad/zur/musik --recursive --field comment
In GROUPING schreiben
energy-tagger /pfad/zur/musik --recursive --field grouping

