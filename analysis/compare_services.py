from pathlib import Path

import pandas as pd


summary = pd.read_csv(Path("reports/jmeter/summary.csv"))
comparison = summary.pivot_table(
    index=["scenario", "concurrency"],
    columns="server",
    values=["p95_latency_ms", "throughput_rps", "error_rate_percent"],
)
print(comparison.to_string())

