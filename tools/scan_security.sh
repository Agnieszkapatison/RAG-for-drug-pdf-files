#!/bin/bash
# Scan the src directory for security issues using Bandit
echo "Running Bandit security scan on src/ directory..."
# Run Bandit, output to both terminal and one file
bandit -r src/ -f txt | tee reports/bandit_report.txt
echo "Security scan completed. Report saved to reports/bandit_report.txt."
