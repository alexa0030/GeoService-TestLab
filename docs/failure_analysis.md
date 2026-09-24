# Failure analysis

## Startup ordering risk

Tile services can start before PostGIS is able to accept connections. The
Compose file gates both services on `pg_isready`; the test runner then polls
each HTTP catalog endpoint before invoking pytest. This addresses the race at
both the container and application layers.

No runtime defect or benchmark conclusion is recorded yet because Docker and
JMeter have not been executed on the development machine. Add only observed
evidence here after a real run.

## CI import-path failure (observed)

The first GitHub Actions run failed before tests started with
`ModuleNotFoundError: No module named 'src'`. The Windows development setup had
implicitly placed the repository root on Python's import path, while the Linux
runner did not do so for direct script execution. The fix declares
`pythonpath = .` for pytest and explicitly sets `PYTHONPATH=.` for the service
readiness script. This turns an environment-dependent assumption into an
explicit, reproducible setting.

## Cross-service source IDs and high zoom (observed)

The second Actions run started all three containers and executed 29 tests. It
showed that Martin 1.16 auto-publishes the table as `sample_features`, while
pg_tileserv exposes it as `public.sample_features`. A shared URL assumption
therefore caused Martin requests to return 404. Service-specific paths are now
configuration, while the client API stays common.

The same run found that pg_tileserv returns HTTP 200 for `z=23`, whereas Martin
rejects it with 404. The boundary suite now records this behavior explicitly
instead of incorrectly assuming both products enforce the same zoom policy.
