#!/usr/bin/env bash
export PYTHONPATH=src

coverage xml -o "reports/coverage.xml"
coverage html -d "reports/coverage_html"
coverage report
