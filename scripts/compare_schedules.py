#!/usr/bin/env python3
"""Compare normalized schedule snapshots. Example data is synthetic."""
import json, sys
from collections import Counter, defaultdict

def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"{path}: expected a JSON array")
    return data

def route_key(x):
    return (x["airline"], x["origin_airport"], x["destination_airport"])

def pattern_key(x):
    return (x.get("flight_number",""), tuple(sorted(x.get("operating_days",[]))),
            x.get("departure_local",""), x.get("arrival_local",""),
            x.get("effective_from",""), x.get("effective_to",""))

def main(a, b):
    before, after = load(a), load(b)
    old, new = defaultdict(list), defaultdict(list)
    for x in before: old[route_key(x)].append(x)
    for x in after: new[route_key(x)].append(x)
    changes=[]
    for k in sorted(set(old)|set(new)):
        if k not in old:
            changes.append({"type":"New route","airline":k[0],"origin":k[1],"destination":k[2],
                            "summary":"Route appears in the newer snapshot."})
        elif k not in new:
            changes.append({"type":"Route withdrawn","airline":k[0],"origin":k[1],"destination":k[2],
                            "summary":"Route is absent from the newer snapshot; requires source verification."})
        else:
            old_days=Counter(d for x in old[k] for d in x.get("operating_days",[]))
            new_days=Counter(d for x in new[k] for d in x.get("operating_days",[]))
            old_freq=sum(old_days.values()); new_freq=sum(new_days.values())
            if new_freq < old_freq:
                typ="Frequency reduction"
            elif new_freq > old_freq:
                typ="Frequency increase"
            else:
                typ="Timetable change" if sorted(map(pattern_key,old[k])) != sorted(map(pattern_key,new[k])) else None
            if typ:
                changes.append({"type":typ,"airline":k[0],"origin":k[1],"destination":k[2],
                    "summary":f"Weekly operating-day count changed from {old_freq} to {new_freq}." if typ.startswith("Frequency") else "Operating pattern or timetable differs; review required."})
    print(json.dumps(changes, indent=2))

if __name__=="__main__":
    if len(sys.argv)!=3:
        raise SystemExit("Usage: python scripts/compare_schedules.py BEFORE.json AFTER.json")
    main(sys.argv[1],sys.argv[2])
