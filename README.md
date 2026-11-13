# Aviation News UK — Schedule Monitor (v2)

A free-first MVP foundation for collecting permitted airline schedule snapshots, comparing them, and publishing verified changes.

## Important scope
This does **not** claim universal or unpublished schedule coverage. A booking page showing no seats is not proof of a cancellation. Only sources whose access and reuse are permitted should be connected. Public changes should carry a source URL and verification status.

## What is included
- `index.html`: public dashboard for GitHub Pages.
- `supabase/migrations/001_initial_schema.sql`: database tables and read policy.
- `scripts/compare_schedules.py`: compares two normalized schedule snapshots.
- `scripts/ingest_snapshot.py`: validates a snapshot and writes it to Supabase.
- `data/airline_sources.csv`: starter source register; no source is assumed to be an approved automated feed.
- `.github/workflows/schedule-check.yml`: scheduled workflow scaffold. It does not scrape airline sites or invent data.
- `examples/`: normalized example snapshots.

## First setup (no paid subscription required)
1. Create a Supabase account and a **Free** project: https://supabase.com/dashboard
2. In Supabase → SQL Editor, run `supabase/migrations/001_initial_schema.sql`.
3. In Supabase → Project Settings → API, copy the Project URL and anon/public key.
4. In GitHub repo → Settings → Secrets and variables → Actions, add:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY` (secret; never put this in the website or commit it)
5. In `index.html`, replace the empty `cfg.url` and `cfg.anonKey` values with the Project URL and anon/public key. The anon key is intended for browser use; database policy limits public access to verified changes.
6. Upload the contents of this project into the existing GitHub repository, preserving the folders. GitHub Pages should continue serving `/`.

## First working test
Use the two example snapshots in `examples/` with the comparison script. They are synthetic test data, not real airline schedules:
```bash
python scripts/compare_schedules.py examples/snapshot_before.json examples/snapshot_after.json
```
This should identify the illustrative weekly frequency reduction. Do not publish this test result.

## Data contract
Each schedule record represents one operating pattern:
```json
{
  "airline": "Example Air",
  "flight_number": "EA123",
  "origin_airport": "GLA",
  "destination_airport": "LHR",
  "operating_days": ["MON", "WED", "FRI"],
  "departure_local": "08:30",
  "arrival_local": "10:00",
  "effective_from": "2027-04-01",
  "effective_to": "2027-10-31",
  "source_url": "https://example.com/timetable",
  "source_type": "official_timetable"
}
```
Only ingest records from an approved source. Keep snapshots for equivalent future date windows to avoid false comparisons.

## Next milestone
Connect one source with documented API access and permitted use. Lufthansa Group's developer portal is a candidate to investigate, but API access, authentication, coverage and reuse terms must be confirmed before enabling a collector. Do not assume this project already has API credentials.
