#!/usr/bin/env python3
"""Insert a normalized snapshot using Supabase service-role credentials."""
import json, os, sys, urllib.request

def main(path):
    url=os.environ["SUPABASE_URL"].rstrip("/")
    key=os.environ["SUPABASE_SERVICE_ROLE_KEY"]
    with open(path,encoding="utf-8") as f: payload=json.load(f)
    required={"source_id","airline","payload","source_url","source_type"}
    missing=required-set(payload)
    if missing: raise SystemExit("Missing fields: "+", ".join(sorted(missing)))
    body=json.dumps(payload).encode()
    req=urllib.request.Request(url+"/rest/v1/schedule_snapshots",data=body,method="POST",
        headers={"apikey":key,"Authorization":"Bearer "+key,"Content-Type":"application/json","Prefer":"return=minimal"})
    with urllib.request.urlopen(req,timeout=30) as res:
        print("Snapshot stored:",res.status)

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("Usage: python scripts/ingest_snapshot.py snapshot.json")
    main(sys.argv[1])
