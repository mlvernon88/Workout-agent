
import json
from workouts import get_workout
from running import get_running_plan

def load_memory():
    with open("memory.json", "r") as f:
        return json.load(f)

def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)

def analyze_workouts(memory):
    workouts = memory["workouts"]
    
    if not workouts:
        return {"missed": 0, "completed": 0}

    completed = sum(1 for w in workouts[-7:] if w["completed"])
    missed = sum(1 for w in workouts[-7:] if not w["completed"])

    return {
        "completed": completed,
        "missed": missed
    }

def adjust_plan(memory):
    stats = analyze_workouts(memory)
    fatigue = memory["fatigue"]

    adjustment = {}
    
    if stats["missed"] >= 2 or fatigue >= 7:
        adjustment["intensity"] = "reduce"
        adjustment["reason"] = "High fatigue or missed workouts"
    elif stats["completed"] >= 5 and fatigue <= 5:
        adjustment["intensity"] = "increase"
        adjustment["reason"] = "Strong consistency and manageable fatigue"
    else:
        adjustment["intensity"] = "maintain"
        adjustment["reason"] = "Balanced performance"

    return adjustment

def generate_plan(memory):
    adjustment = adjust_plan(memory)

    week_structure = [
        ("Mon", "chest_triceps"),
        ("Tue", "back_biceps"),
        ("Wed", "arms"),
        ("Thu", "shoulders"),
        ("Fri", "legs"),
        ("Sat", "optional"),
        ("Sun", "rest")
    ]

    plan_output = []

    run_analysis = analyze_runs(memory)

    run_intensity = adjustment["intensity"]

    if run_analysis["adjustment"] == "reduce":
        run_intensity = "reduce"

    running_plan = get_running_plan(
        memory.get("phase", "base"),
        run_intensity,
        memory
    )

    run_index = 0

    for day, split in week_structure:

        if split == "rest":
            plan_output.append(f"{day}: Rest")

        elif split == "optional":
            run = running_plan[run_index % len(running_plan)]
            run_index += 1

            run_text = (
                f"{run['type']} — {run['time']}\n"
                f"      Pace: {run['pace']}\n"
                f"      Effort: {run['effort']}\n"
                f"      Note: {run['note']}"
            )

            plan_output.append(f"{day}:\n   🏃 {run_text} (optional recovery day)")
        else:
            run = running_plan[run_index % len(running_plan)]
            run_index += 1

            workout = get_workout(split, adjustment["intensity"], memory)            
            workout_text = "\n   ".join(workout)

            run_text = (
                f"{run['type']} — {run['time']}\n"
                f"      Pace: {run['pace']}\n"
                f"      Effort: {run['effort']}"
            )

            plan_output.append(
                f"{day}:\n"
                f"   🏃 {run_text}\n"
                f"   🏋️ {workout_text}"
            )

    return plan_output

def analyze_runs(memory):
    runs = [w for w in memory["workouts"] if w["type"] == "run" and w["completed"]]

    if not runs:
        return {"adjustment": "none"}

    recent = runs[-3:]  # last 3 runs
    high_effort_runs = [r for r in recent if r.get("effort", 0) >= 6]

    if len(high_effort_runs) >= 2:
        return {"adjustment": "reduce"}
    
    return {"adjustment": "maintain"}

def analyze_runs(memory):
    runs = [w for w in memory["workouts"] if w["type"] == "run" and w["completed"]]

    if not runs:
        return {"adjustment": "none"}

    recent = runs[-3:]  # last 3 runs
    high_effort_runs = [r for r in recent if r.get("effort", 0) >= 6]

    if len(high_effort_runs) >= 2:
        return {"adjustment": "reduce"}
    
    return {"adjustment": "maintain"}