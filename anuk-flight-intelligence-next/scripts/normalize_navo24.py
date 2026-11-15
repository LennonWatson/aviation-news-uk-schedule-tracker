#!/usr/bin/env python3
"""Convert Navo24 response records to ANUK's normalized flight format.

Provider response shapes can evolve during beta. Unknown shapes fail loudly
instead of silently creating misleading records.
"""
import json, sys
from datetime import datetime, timezone

def pick(obj, *names):
    for n in names:
        v=obj.get(n)
        if v not in (None,""): return v
    return None

def normalize(payload):
    root=payload.get("response",payload)
    data=root.get("data",root) if isinstance(root,dict) else root
    if isinstance(data,dict):
        for k in ("flights","items","results"):
            if isinstance(data.get(k),list):
                data=data[k]; break
    if not isinstance(data,list):
        raise ValueError("Unrecognised provider response: expected a flight list; inspect raw response before adapting.")
    out=[]
    for f in data:
        if not isinstance(f,dict): continue
        airline=pick(f,"operating_airline","airline","carrier")
        number=pick(f,"flight_number","flight_no","number")
        origin=pick(f,"origin","departure_airport","from")
        destination=pick(f,"destination","arrival_airport","to")
        dep=pick(f,"departure_local","departure_time_local","departure_time","scheduled_departure")
        arr=pick(f,"arrival_local","arrival_time_local","arrival_time","scheduled_arrival")
        if not all((airline,number,origin,destination,dep,arr)):
            continue
        days=pick(f,"operating_days","days_of_week","days") or []
        if isinstance(days,str): days=[days]
        out.append({
          "airline":airline,"flight_number":number,"origin":origin,"destination":destination,
          "departure_local":dep,"arrival_local":arr,"operating_days":days,
          "effective_from":pick(f,"effective_from","start_date","date"),
          "effective_to":pick(f,"effective_to","end_date"),
          "aircraft_type":pick(f,"aircraft_type","aircraft","equipment"),
          "source_name":"Navo24 Flight Schedules API",
          "source_url":"https://flight.navo24.com/docs",
          "captured_at":payload.get("retrieved_at") or datetime.now(timezone.utc).isoformat(),
          "provider_updated_at":pick(f,"updated_at")
        })
    return out

if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("Usage: python scripts/normalize_navo24.py RAW.json NORMALIZED.json")
    raw=json.load(open(sys.argv[1],encoding="utf-8"))
    rows=normalize(raw)
    json.dump(rows,open(sys.argv[2],"w",encoding="utf-8"),indent=2)
    print(f"Normalized {len(rows)} flight records")
