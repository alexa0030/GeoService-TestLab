# Architecture

```text
pytest / JMeter / result analyzer
              |
          HTTP requests
              |
    +---------+----------+
    |                    |
 Martin              pg_tileserv
    |                    |
    +---------+----------+
              |
       PostgreSQL/PostGIS
```

Both servers read the same spatial table. This makes cross-service functional
checks and like-for-like performance runs possible.

