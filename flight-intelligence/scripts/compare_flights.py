#!/usr/bin/env python3
"""Compare two normalized flight schedule snapshots. Output is review-required, not proof of cancellation."""
import json, sys
from collections import defaultdict

def load(path):
    with open(path, encoding="utf-8") as f:
        rows=json.load(f)
    if not isinstance(rows,list): raise ValueError(f"{path}: expected a JSON array")
    return rows

def key(x):
    return (x.get("airline",""),x.get("flight_number",""),x.get("origin",""),x.get("destination",""),x.get("effective_from",""))

def main(before_path, after_path):
    before={key(x):x for x in load(before_path)}
    after={key(x):x for x in load(after_path)}
    changes=[]
    for k in sorted(set(before)|set(after)):
        old,new=before.get(k),after.get(k)
        if old is None:
            typ="Flight added"; fields=["new flight record detected"]
        elif new is None:
            typ="Flight missing"; fields=["record absent from newer snapshot; verify before calling cancelled"]
        else:
            fields=[]
            for field,label in [("departure_local","departure time"),("arrival_local","arrival time"),("operating_days","operating days"),("aircraft_type","aircraft type"),("effective_to","season end")]:
                if old.get(field)!=new.get(field): fields.append(f"{label}: {old.get(field)} -> {new.get(field)}")
            typ="Schedule changed" if fields else None
        if typ:
            rec=new or old
            changes.append({"change_type":typ,"airline":rec.get("airline"),"flight_number":rec.get("flight_number"),
             "origin":rec.get("origin"),"destination":rec.get("destination"),"effective_from":rec.get("effective_from"),
             "details":fields,"verification_status":"review_required","source_name":rec.get("source_name"),
             "source_url":rec.get("source_url"),"before_captured_at":old.get("captured_at") if old else None,
             "after_captured_at":new.get("captured_at") if new else None})
    print(json.dumps(changes,indent=2))

if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("Usage: python scripts/compare_flights.py BEFORE.json AFTER.json")
    main(*sys.argv[1:])
