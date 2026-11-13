create extension if not exists pgcrypto;

create table if not exists public.schedule_snapshots (
  id uuid primary key default gen_random_uuid(),
  source_id text not null,
  airline text not null,
  captured_at timestamptz not null default now(),
  window_start date,
  window_end date,
  payload jsonb not null,
  source_url text,
  source_type text not null default 'official',
  created_at timestamptz not null default now()
);

create index if not exists schedule_snapshots_airline_captured_idx
on public.schedule_snapshots (airline, captured_at desc);

create table if not exists public.schedule_changes (
  id uuid primary key default gen_random_uuid(),
  airline text not null,
  change_type text not null check (change_type in ('New route','Route withdrawn','Frequency increase','Frequency reduction','Timetable change')),
  origin_airport text,
  destination_airport text,
  summary text not null,
  detected_at timestamptz not null default now(),
  effective_from date,
  source_url text not null,
  verification_status text not null default 'under_review' check (verification_status in ('under_review','verified','rejected')),
  before_snapshot_id uuid references public.schedule_snapshots(id),
  after_snapshot_id uuid references public.schedule_snapshots(id),
  created_at timestamptz not null default now()
);

create index if not exists schedule_changes_public_idx
on public.schedule_changes (verification_status, detected_at desc);

alter table public.schedule_snapshots enable row level security;
alter table public.schedule_changes enable row level security;

-- Public visitors can read verified changes only.
drop policy if exists "Public can read verified schedule changes" on public.schedule_changes;
create policy "Public can read verified schedule changes"
on public.schedule_changes for select
to anon, authenticated
using (verification_status = 'verified');

-- Snapshots and writes remain private. Service role is used only by trusted automation.
grant select on public.schedule_changes to anon, authenticated;
