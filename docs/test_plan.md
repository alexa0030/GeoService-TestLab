# Test plan

## Scope

Validate availability, vector-tile responses, input handling, repeatability and
relative performance of Martin and pg_tileserv against one PostGIS dataset.

## Strategy

- Unit tests cover URL construction, configuration and analysis logic.
- Integration tests cover catalog discovery, valid tiles, boundaries, invalid
  layers, repeatability and the two service implementations.
- JMeter runs each service at 1, 10 and 50 concurrent users.
- The analyzer reports average/P95 latency, throughput and error rate.

## Entry and exit criteria

Docker services must be healthy before integration tests begin. A release is
acceptable when unit and integration suites pass and performance runs contain
no unexplained errors. Performance is reported, not used as a fixed pass/fail
gate, because host capacity varies.

