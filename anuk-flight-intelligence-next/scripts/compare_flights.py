#!/usr/bin/env python3
"""Compare snapshots using flight identity and report changed fields."""
import json,sys
FIELDS=("departure_local","arrival_local","operating_days","aircraft_type","effective_from","effective_to")
def load(p):
    x=json.load(open(p,encoding="utf-8"))
    if not isinstance(x,list): raise ValueError(f"{p}: expected JSON array")
    return x
def key(f):
    return tuple(f.get(k,"") for k in ("airline","flight_number","origin","destination","effective_from"))
def compare(old,new):
    a={key(x):x for x in old}; b={key(x):x for x in new}; out=[]
    for k in sorted(a.keys()|b.keys()):
        x,y=a.get(k),b.get(k); record=y or x; changes=[]
        if x is None: kind="Flight added"
        elif y is None: kind="Flight missing — review"
        else:
            changes=[{"field":f,"before":x.get(f),"after":y.get(f)} for f in FIELDS if x.get(f)!=y.get(f)]
            if not changes: continue
            kind="Schedule changed"
        out.append({"change_type":kind,"airline":record.get("airline"),"flight_number":record.get("flight_number"),
          "origin":record.get("origin"),"destination":record.get("destination"),"changes":changes,
          "verification_status":"review_required","source_name":record.get("source_name"),
          "source_url":record.get("source_url"),"before_captured_at":x.get("captured_at") if x else None,
          "after_captured_at":y.get("captured_at") if y else None})
    return out
if __name__=="__main__":
    if len(sys.argv)!=3: raise SystemExit("Usage: python scripts/compare_flights.py BEFORE.json AFTER.json")
    print(json.dumps(compare(load(sys.argv[1]),load(sys.argv[2])),indent=2))
