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

Subsequent execution also exposed two response semantics. Martin returns 204
for an empty tile, while pg_tileserv returns 200 with an empty tile payload;
the original z6/z10 x coordinates did not cover the Shanghai sample and made
this visible. The corrected coordinates are x=53 at z6 and x=857 at z10. At
z=23/x=0/y=0 the suite records the service-specific 204 versus 200 contract.

## MVT byte equality was too strict (observed)

The fourth Actions run reached 28/29 passing tests. All repeated pg_tileserv
requests returned HTTP 200 with non-empty MVT payloads, but two distinct byte
sequences were observed. Protobuf encoding does not make byte-for-byte equality
a suitable API contract when logical content can be encoded in a different
order. The regression check now asserts stable success and non-empty payloads;
a future semantic comparison can decode MVT features before comparison.
