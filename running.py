def get_running_plan(phase="base", intensity="normal", memory=None):
    
    base_low = memory.get("easy_pace_range", {}).get("low", 9.75)
    base_high = memory.get("easy_pace_range", {}).get("high", 10.0)

    def format_range(low, high):
        return f"{round(low,2)}–{round(high,2)}"

    runs = [
        {
            "type": "Easy Run",
            "time": "35-45 min",
            "pace": format_range(base_low, base_high),
            "effort": "3-4",
            "note": "Baseline aerobic run"
        },
        {
            "type": "Tempo Run",
            "time": "25-30 min",
            "pace": format_range(base_low - 1.0, base_high - 0.7),
            "effort": "6-7",
            "note": "Controlled hard effort"
        },
        {
            "type": "Recovery Run",
            "time": "20-30 min",
            "pace": format_range(base_low + 0.5, base_high + 0.8),
            "effort": "2-3",
            "note": "Very easy recovery"
        },
        {
            "type": "Easy Run",
            "time": "30-40 min",
            "pace": format_range(base_low, base_high),
            "effort": "3-4",
            "note": "Maintain aerobic base"
        },
        {
            "type": "Long Run",
            "time": "45-60 min",
            "pace": format_range(base_low + 0.2, base_high + 0.5),
            "effort": "4-5",
            "note": "Build endurance"
        }
    ]

    # Adjust for fatigue/adaptation
    if intensity == "reduce":
        for r in runs:
            r["pace"] = format_range(base_low + 0.4, base_high + 0.8)
            r["effort"] = "2-3"
            r["note"] = "Reduced intensity due to fatigue"

    elif intensity == "increase":
        for r in runs:
            r["pace"] = format_range(base_low - 0.2, base_high - 0.4)
            r["effort"] = "5-7"
            r["note"] = "Progression week"

    return runs
