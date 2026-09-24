from pathlib import Path

import pandas as pd

from analysis.analyze_results import summarize


def test_jmeter_summary_calculation(tmp_path: Path):
    result = tmp_path / "martin_10.jtl"
    pd.DataFrame({
        "timeStamp": [1000, 1100, 1200],
        "elapsed": [10, 20, 30],
        "success": [True, True, False],
        "label": ["single_tile"] * 3,
    }).to_csv(result, index=False)
    row = summarize(result)
    assert row["server"] == "martin"
    assert row["concurrency"] == 10
    assert row["samples"] == 3
    assert row["avg_latency_ms"] == 20
    assert row["error_rate_percent"] == 33.33

