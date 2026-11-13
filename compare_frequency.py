#!/usr/bin/env python3
"""Small pure function for comparing equivalent route-frequency snapshots."""
def classify(old_frequency: int, new_frequency: int) -> dict:
    delta = new_frequency - old_frequency
    if delta < 0:
        kind = "Frequency reduction"
    elif delta > 0:
        kind = "Frequency increase"
    else:
        kind = "No frequency change"
    pct = (delta / old_frequency * 100) if old_frequency else None
    return {
        "change_type": kind,
        "previous_value": f"{old_frequency} weekly",
        "current_value": f"{new_frequency} weekly",
        "weekly_delta": delta,
        "percentage_change": round(pct, 1) if pct is not None else None,
    }

if __name__ == "__main__":
    import json
    print(json.dumps(classify(4, 3), indent=2))
