#!/usr/bin/env bash

# Ustawienie katalogu z kodem źródłowym jako ścieżki dla Pythona
export PYTHONPATH=src

# Uruchomienie testów z mierzeniem pokrycia kodu
coverage run -m pytest tests/

# Generowanie raportów pokrycia
coverage xml -o "reports/coverage.xml"
coverage html -d "reports/coverage_html"
coverage report
