# GeoService-TestLab

**Automated Testing & Performance Benchmarking for Geospatial Services**

[![test](https://github.com/alexa0030/GeoService-TestLab/actions/workflows/test.yml/badge.svg)](https://github.com/alexa0030/GeoService-TestLab/actions/workflows/test.yml)

Python · pytest · Docker Compose · PostGIS · JMeter · GitHub Actions

GeoService-TestLab is a reproducible test-development demo for vector-tile
services. It connects an urban–rural spatial-data use case with API automation,
regression testing, performance measurement and CI.

```text
                 pytest / JMeter
                       |
                 HTTP requests
                       |
          +------------+------------+
          |                         |
       Martin                  pg_tileserv
          |                         |
          +------------+------------+
                       |
                PostgreSQL/PostGIS
```

## Quick start

Prerequisites: Docker Desktop, Docker Compose v2, Python 3.10+.

```bash
git clone <your-repository-url>
cd GeoService-TestLab
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d
python scripts/wait_for_services.py
```

Run the complete API suite:

```bash
RUN_INTEGRATION=1 pytest -v
# PowerShell: $env:RUN_INTEGRATION=1; pytest -v
```

Without Docker, `pytest -v -m "not integration"` runs the local unit suite.

## Test design

The suite uses a shared client, pytest fixtures and parameterization. It covers:

- service/catalog availability;
- valid vector tiles at multiple zoom levels;
- status, content type and binary payload checks;
- invalid zoom/x inputs and unknown layers;
- repeatable core API responses;
- the same layer through Martin and pg_tileserv.

See [the test plan](docs/test_plan.md) and [case matrix](docs/test_cases.md).

## Performance benchmark

With Apache JMeter 5.6.3 installed:

```bash
bash scripts/run_performance.sh
```

The plans execute **24 benchmark groups**: two services × four tile scenarios
(z0, z6, z10 and four-tile z10) × three concurrency levels (1/10/50). The
Python analyzer reads real JMeter JTL/CSV output and creates:

- `reports/jmeter/summary.csv` (samples, average, P95, throughput, error rate);
- `reports/figures/latency_vs_concurrency.png`;
- `reports/figures/throughput_vs_concurrency.png`.

No benchmark number is committed until it has been measured on a real host.

## Current verification status

The verified GitHub Actions run completed both jobs successfully:

- local/unit selection: **7 passed**;
- Docker-backed complete suite: **29 passed**;
- PostGIS, Martin and pg_tileserv: started and queried successfully;
- JMeter benchmark: not yet executed, so no performance numbers are claimed.

GitHub Actions runs both suites on every push and pull request.

## Failure analysis

The first engineered risk is service startup ordering: a database container can
exist before it is ready for connections. Compose checks `pg_isready`, and the
Python runner additionally polls both HTTP catalogs. See
[failure analysis](docs/failure_analysis.md). Observed runtime issues should be
added there with logs and fixes, not invented in advance.

## Project structure

```text
config/       service and test settings
data/         publishable GeoJSON and database initialization
src/          API client, configuration and logging
tests/        unit, API, boundary and regression tests
performance/  JMeter plans and scenarios
analysis/     result summarization and comparison
scripts/      environment, test and benchmark runners
docs/         architecture, plan, cases and failure analysis
.github/      CI workflow
```

## Reference

Inspired by
[FabianRechsteiner/vector-tiles-benchmark](https://github.com/FabianRechsteiner/vector-tiles-benchmark).
This project keeps the PostGIS → vector-tile service → JMeter benchmark idea
and adds Python API automation, boundary and regression tests, CI, startup
readiness checks and automated result analysis. It is an independent testing
demo and does not copy the original benchmark implementation.

## License

MIT
