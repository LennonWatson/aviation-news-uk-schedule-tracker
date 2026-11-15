#!/usr/bin/env python3
"""Navo24 flight schedule adapter.

Uses the documented Navo24 Flight Schedules API only. No scraping.
A key is optional only for the provider's documented HKG-FRA demo route.
For UK routes, the provider currently requires an API key; this adapter will
not invent or substitute data when a request is unavailable.
"""
from __future__ import annotations
import json, os, sys, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone

BASE = os.getenv("NAVO24_BASE_URL", "https://api.navo24.com/v1/flight")

def fetch_route(origin: str, destination: str, date: str, days: int = 7) -> dict:
    params = urllib.parse.urlencode({"from": origin.upper(), "to": destination.upper(),
                                     "date": date, "days": max(1, min(int(days), 14))})
    req = urllib.request.Request(f"{BASE}/flights?{params}", headers={"Accept":"application/json"})
    key = os.getenv("NAVO24_API_KEY")
    if key:
        req.add_header("Authorization", f"Bearer {key}")
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            payload=json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail=e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Navo24 returned HTTP {e.code}: {detail[:500]}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Could not reach Navo24: {e}") from e
    return payload

def main():
    if len(sys.argv) < 4:
        raise SystemExit("Usage: python connectors/navo24_client.py ORIGIN DESTINATION YYYY-MM-DD [DAYS]")
    origin,destination,date=sys.argv[1:4]
    days=int(sys.argv[4]) if len(sys.argv)>4 else 7
    result=fetch_route(origin,destination,date,days)
    print(json.dumps({"provider":"Navo24","retrieved_at":datetime.now(timezone.utc).isoformat(),
                      "query":{"origin":origin.upper(),"destination":destination.upper(),"date":date,"days":days},
                      "response":result},indent=2))
if __name__=="__main__": main()
