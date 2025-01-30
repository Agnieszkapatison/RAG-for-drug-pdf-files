#!/bin/bash
# Scan the src directory for security issues using Bandit
echo "Running Bandit security scan on src/ directory..."
bandit -r src/ -o reports/bandit_report.txt
echo "Security scan completed. Report saved to reports/bandit_report.txt."
