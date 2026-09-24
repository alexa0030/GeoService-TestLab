#!/usr/bin/env bash
set -euo pipefail
export RUN_INTEGRATION=1
python scripts/wait_for_services.py
pytest -v --html=reports/pytest/report.html --self-contained-html

