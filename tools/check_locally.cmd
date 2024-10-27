@echo off
pre-commit run --all-files
call tools\run_tests.cmd
