@echo off
set PYTHONPATH=src
coverage run --source=src -m pytest tests --log-cli-level=debug --junitxml="reports/junit.xml"
coverage xml -o "reports/coverage.xml"
rem coverage html -d "reports/coverage_html"
coverage report
