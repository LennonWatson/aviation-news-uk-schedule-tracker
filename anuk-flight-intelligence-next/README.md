# ANUK Flight Intelligence — connector development pack

## Work completed
- Documented Navo24 route-schedule API adapter (no scraping).
- Normalizer that refuses unknown response structures.
- Snapshot comparison with field-level diffs.
- Tests for unchanged, added, missing and changed flights.
- Provider status register.

## Important current limitation
Navo24's published docs state that the route endpoint is free without a key only for the HKG-FRA demo route; other routes require a `tmcp_` API key. Its public documentation also describes a very small free search allowance. This is not enough to operate a UK-wide monitor. No account has been created and no API key is assumed.

OpenSky is not a schedule source. Its terms require a written licence for operational REST API integration and commercial/for-profit use. It must not be used as a free production feed for this product.

OpenFlights supplies reference airport/airline/route data, not current flight timetables.

## Run tests
```bash
python -m unittest tests/test_compare_flights.py
```

## Try the Navo24 demo (optional)
```bash
python connectors/navo24_client.py HKG FRA 2026-11-16 1 > /tmp/navo24-raw.json
python scripts/normalize_navo24.py /tmp/navo24-raw.json data/flights.json
```
Do not run UK route queries without a valid API key. Do not put keys in source control.

## Status semantics
A missing flight in a later snapshot is only `Flight missing — review`. It is not automatically a cancellation. The source may have incomplete coverage, a changed query window, or temporary missing inventory.
