# Test cases

| Area | Case | Expected result |
|---|---|---|
| Health | Catalog endpoint | HTTP 200 and non-empty body |
| Functional | z0/z6/z10 tiles | HTTP 200 and vector-tile content type |
| Interface | Tile payload | Binary response |
| Boundary | Negative zoom | Explicit 4xx/5xx rejection |
| Boundary | Zoom 23 | Explicit service-specific status contract |
| Boundary | Negative x | Explicit rejection |
| Invalid | Unknown layer | HTTP 400/404 |
| Regression | Three identical requests | Stable status and payload |
| Cross-service | Layer discovery | Expected table exposed by both services |
| Performance | 1/10/50 users | JTL result collected and analyzed |
