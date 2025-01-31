#!/usr/bin/env bash

mkdir -p reports

pytest tests/ \
    --cov=src \
    --cov-report=xml:reports/coverage.xml \
    --cov-report=html:reports/coverage_html \
    --cov-report=term \
    --log-cli-level=debug \
    --junitxml=reports/junit.xml \
    "$@"  # Akceptujemy dodatkowe argumenty, np. --ignore=tests/performance/
