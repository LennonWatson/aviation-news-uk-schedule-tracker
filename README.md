# Aviation News UK — Airline Schedule Tracker

A public schedule-change dashboard starter project.

## Current state
- Responsive public dashboard UI.
- Search and filters for airline, airport, destination, change type and season.
- Empty-state behaviour until verified records are supplied.
- Supabase schema for schedule snapshots and detected changes.
- Hourly GitHub Actions workflow scaffold.

**This repository starter does not yet contain a live airline data feed.** It must not publish illustrative or unverified schedule changes as facts.

## Intended architecture
- GitHub: source control and CI.
- GitHub Pages (or another static host): public dashboard.
- Supabase: persistent schedule snapshots and change records.
- Scheduled collector: retrieves permitted official airline timetable data or licensed schedule data, normalises it, compares equivalent travel periods and writes verified changes.
- Public API: serves published changes to the dashboard.

## Important data requirements
A reliable frequency comparison needs comparable date windows, operating-day patterns, codeshare handling, seasonal boundaries and duplicate-flight rules. Airline websites may restrict automated access; use official feeds, published timetable files or licensed data where available and respect each provider's terms. Do not treat a booking search result or a single unavailable date as proof that a route was withdrawn.

## GitHub setup
1. Create a private repository initially, e.g. `aviation-news-uk-schedule-tracker`.
2. Upload this project.
3. Enable GitHub Pages after confirming the dashboard path and hosting arrangement.
4. Create a Supabase project and apply `supabase/migrations/001_initial_schema.sql`.
5. Add required secrets only after the collector is implemented and tested:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`
6. Configure a permitted schedule-data source and implement its adapter before enabling hourly collection.

## Local preview
Open `index.html` directly in a browser. Without `/api/changes`, it safely shows an empty state.

## Planned change record fields
Airline, origin, destination, season, previous/current frequency, operating days, departure/arrival times, aircraft (where sourced), effective dates, detected timestamp, source URL, verification status and snapshot references.
