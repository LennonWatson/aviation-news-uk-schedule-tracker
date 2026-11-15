# Aviation News UK — Flight Intelligence starter

This is a free-first extension for the existing ANUK schedule tracker. It adds a flight-level data model, a snapshot comparison engine, a source register and a static flight search dashboard.

## Important data-access boundary
This project does **not** scrape private airline systems, bypass login, defeat bot controls, or assume consumer booking pages may be automated. Airline APIs often require approval and credentials. A connector remains disabled until ANUK has permission and valid credentials.

## What works now
- Normalises flight schedule records into a consistent JSON format.
- Compares two dated snapshots and flags additions, removals, time changes, aircraft changes and operating-day changes.
- Provides a browser-based search over a locally published `data/flights.json` file.
- Includes a registry describing known candidate sources and their access status.

## What is not connected yet
- No live airline schedule source is enabled.
- No booking-class inventory / seat availability feed is connected.
- No airline credentials are included.
- Demo data is explicitly synthetic and must never be presented as real flights.

## Standard flight record
Each record in `data/flights.json` should use:
`airline`, `flight_number`, `origin`, `destination`, `departure_local`, `arrival_local`, `operating_days`, `effective_from`, `effective_to`, `aircraft_type`, `source_name`, `source_url`, `captured_at`.

`operating_days` uses ISO weekday numbers: Monday=1 through Sunday=7.

## Local test
```bash
python scripts/compare_flights.py examples/before.json examples/after.json
```

## Next connection
1. Request approved API access from an airline or data provider.
2. Add its documented authentication and query logic in `connectors/`.
3. Store credentials as GitHub Actions repository secrets — never in source files.
4. Run the connector on a conservative schedule and save dated snapshots.
5. Review removals before marking them as cancellations: missing data can be a query/window/inventory issue.

## Cost
The code is designed for GitHub Actions + GitHub Pages. Usage must remain within GitHub's free allowance. This does not make proprietary schedule data free; access/licensing is separate.
