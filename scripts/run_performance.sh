#!/usr/bin/env bash
set -euo pipefail
mkdir -p reports/jmeter
for service in martin pg_tileserv; do
  for scenario in single_z0 single_z6 single_z10 multi_z10; do
    for concurrency in 1 10 50; do
      jmeter -n -t "performance/${service}.jmx" \
        -Jthreads="$concurrency" -Jloops=20 \
        -Jscenario="$scenario" \
        -Jdatafile="performance/data/${scenario}.csv" \
        -l "reports/jmeter/${service}_${scenario}_${concurrency}.jtl"
    done
  done
done
python analysis/analyze_results.py reports/jmeter
