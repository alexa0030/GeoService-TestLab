# Failure analysis

## Startup ordering risk

Tile services can start before PostGIS is able to accept connections. The
Compose file gates both services on `pg_isready`; the test runner then polls
each HTTP catalog endpoint before invoking pytest. This addresses the race at
both the container and application layers.

No runtime defect or benchmark conclusion is recorded yet because Docker and
JMeter have not been executed on the development machine. Add only observed
evidence here after a real run.

