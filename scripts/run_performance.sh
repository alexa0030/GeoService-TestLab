#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports/jmeter
for service in martin pg_tileserv; do
  for concurrency in 1 10 50; do
    jmeter -n -t "performance/${service}.jmx" \
      -Jthreads="$concurrency" -Jloops=20 \
      -l "reports/jmeter/${service}_${concurrency}.jtl"
  done
done
python analysis/analyze_results.py reports/jmeter

