from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


NAME = re.compile(
    r"^(?P<server>martin|pg_tileserv)_(?P<scenario>.+)_(?P<concurrency>\d+)$"
)


def summarize(path: Path) -> dict:
    match = NAME.search(path.stem)
    if not match:
        raise ValueError(f"Expected filename like martin_10.jtl: {path.name}")
    frame = pd.read_csv(path)
    elapsed_seconds = max((frame["timeStamp"].max() - frame["timeStamp"].min()) / 1000, 0.001)
    success = frame["success"].astype(str).str.lower().eq("true")
    return {
        "server": match["server"],
        "scenario": match["scenario"],
        "concurrency": int(match["concurrency"]),
        "samples": len(frame),
        "avg_latency_ms": round(frame["elapsed"].mean(), 2),
        "p95_latency_ms": round(frame["elapsed"].quantile(0.95), 2),
        "throughput_rps": round(len(frame) / elapsed_seconds, 2),
        "error_rate_percent": round((~success).mean() * 100, 2),
    }


def analyze(input_dir: Path, output_dir: Path) -> pd.DataFrame:
    files = sorted([*input_dir.glob("*.jtl"), *input_dir.glob("*.csv")])
    rows = [summarize(path) for path in files if NAME.search(path.stem)]
    if not rows:
        raise FileNotFoundError(f"No named JMeter results found in {input_dir}")
    result = pd.DataFrame(rows).sort_values(["scenario", "server", "concurrency"])
    output_dir.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_dir / "summary.csv", index=False)
    figures = output_dir.parent / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    for metric, filename, ylabel in [
        ("p95_latency_ms", "latency_vs_concurrency.png", "P95 latency (ms)"),
        ("throughput_rps", "throughput_vs_concurrency.png", "Throughput (req/s)"),
    ]:
        figure, axis = plt.subplots(figsize=(7, 4))
        for (server, scenario), group in result.groupby(["server", "scenario"]):
            axis.plot(
                group["concurrency"], group[metric], marker="o",
                label=f"{server} / {scenario}",
            )
        axis.set(xlabel="Concurrent users", ylabel=ylabel, title=f"{ylabel} vs concurrency")
        axis.grid(alpha=0.3)
        axis.legend()
        figure.tight_layout()
        figure.savefig(figures / filename, dpi=160)
        plt.close(figure)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("reports/jmeter"))
    args = parser.parse_args()
    print(analyze(args.input_dir, args.output_dir).to_string(index=False))
