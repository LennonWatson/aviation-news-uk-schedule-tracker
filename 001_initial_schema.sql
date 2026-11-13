create extension if not exists pgcrypto;

create table if not exists public.schedule_snapshots (
  id uuid primary key default gen_random_uuid(),
  airline text not null,
  origin text not null,
  destination text not null,
  season text not null,
  travel_date date,
  flight_number text,
  departure_local time,
  arrival_local time,
  operating_days text[],
  aircraft text,
  source_url text not null,
  source_name text,
  captured_at timestamptz not null default now(),
  raw_reference text
);

create index if not exists schedule_snapshots_route_idx
  on public.schedule_snapshots (airline, origin, destination, season, captured_at desc);

create table if not exists public.schedule_changes (
  id uuid primary key default gen_random_uuid(),
  airline text not null,
  origin text not null,
  destination text not null,
  season text not null,
  change_type text not null check (change_type in (
    'Frequency reduction','Frequency increase','New route',
    'Route withdrawal','Timetable change','Operating-day change','Aircraft change'
  )),
  previous_value text,
  current_value text,
  effective_from date,
  effective_to date,
  detected_at timestamptz not null default now(),
  source_url text not null,
  verification_status text not null default 'pending'
    check (verification_status in ('pending','verified','provisional','rejected')),
  previous_snapshot_id uuid references public.schedule_snapshots(id),
  current_snapshot_id uuid references public.schedule_snapshots(id),
  public_note text,
  created_at timestamptz not null default now()
);

create index if not exists schedule_changes_public_idx
  on public.schedule_changes (verification_status, detected_at desc);

alter table public.schedule_snapshots enable row level security;
alter table public.schedule_changes enable row level security;

-- Public visitors may read verified change records only.
create policy "Public can read verified schedule changes"
  on public.schedule_changes for select
  using (verification_status = 'verified');

-- No public write policies. Collector writes using a server-side service key.
