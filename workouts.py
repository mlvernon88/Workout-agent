print("LOADING WORKOUTS FILE")

import os
print("LOADING FILE FROM:", os.path.abspath(__file__))

import random
from exercise_library import exercise_library


# =========================
# PROGRESSION LOGIC
# =========================
def get_progression(memory, exercise):
    lifts = [
        w for w in memory["workouts"]
        if w.get("type") == "lift" and w.get("exercise") == exercise
    ]

    if not lifts:
        return None

    recent = lifts[-4:]

    top_sets = []
    dropoffs = []

    for w in recent:
        if "weights" in w:
            weights = w["weights"]
            reps = w["reps"]

            top_weight = max(weights)
            top_reps = max(
                r for i, r in enumerate(reps) if weights[i] == top_weight
            )

            dropoff = reps[0] - reps[-1]

        else:
            top_weight = w["weight"]
            top_reps = w["reps"]
            dropoff = 0

        top_sets.append((top_weight, top_reps))
        dropoffs.append(dropoff)

    last_weight, last_reps = top_sets[-1]

    avg_reps = sum(r for _, r in top_sets) / len(top_sets)
    avg_drop = sum(dropoffs) / len(dropoffs)

    if avg_reps >= 9 and avg_drop <= 2:
        return last_weight + 5
    elif avg_drop >= 3:
        return last_weight - 5
    elif avg_reps < 6:
        return last_weight - 5
    else:
        return last_weight


# =========================
# REP SCHEMES
# =========================
def get_rep_scheme(phase):
    if phase == "strength":
        return {
            "compound": "5x3-5",
            "secondary": "4x5-8",
            "accessory": "3x8-10",
            "finisher": "2 sets moderate effort"
        }

    elif phase == "cut":
        return {
            "compound": "4x8-10",
            "secondary": "3x10-12",
            "accessory": "3x12-15",
            "finisher": "2-3 sets high fatigue"
        }

    else:
        return {
            "compound": "4x6-8",
            "secondary": "3x8-10",
            "accessory": "3x12-15",
            "finisher": "2 sets"
        }


# =========================
# EXERCISE PICKING
# =========================
def pick_exercises(split, block_type, n=2):
    default_pool = ["Push-ups", "Plank", "Band Pull-Aparts"]

    try:
        if split == "chest_triceps":
            lib = exercise_library["chest"]

            if block_type == "strength":
                pool = lib["compound"]
            elif block_type in ["upper_chest", "shoulders"]:
                pool = lib["secondary"]
            elif block_type == "triceps":
                pool = ["Close-Grip Bench Press", "Overhead DB Extension", "Band Pushdowns"]
            elif block_type == "core":
                pool = ["Plank", "Dead Bug", "Side Plank"]
            elif block_type == "warmup":
                pool = ["Push-ups", "Band Pull-Aparts", "Light DB Press"]
            else:
                pool = lib["accessory"] + lib.get("bodyweight", [])

        elif split == "back_biceps":
            lib = exercise_library["back"]

            if block_type == "strength":
                pool = lib["horizontal_pull"]
            elif block_type == "rear_delts":
                pool = ["Face Pull", "Rear Delt Row"]
            elif block_type == "biceps":
                pool = ["Barbell Curl", "Hammer Curl", "Incline Curl"]
            elif block_type == "warmup":
                pool = ["Band pull-aparts", "Light rows", "Dead hangs"]
            else:
                pool = lib["vertical_pull"] + lib["horizontal_pull"]

        elif split == "legs":
            lib = exercise_library["legs"]

            if block_type == "strength":
                pool = lib["squat"]
            elif block_type == "single_leg":
                pool = lib["single_leg"]
            elif block_type == "warmup":
                pool = ["Bodyweight Squat", "Glute Bridge", "Hip Openers"]
            elif block_type == "core":
                pool = ["Plank", "Hanging Leg Raise"]
            else:
                pool = lib["hinge"] + lib["glutes"]

        else:
            pool = default_pool

    except:
        pool = default_pool

    if not pool:
        pool = default_pool

    return random.sample(pool, min(n, len(pool)))


# =========================
# WORKOUT GENERATOR
# =========================
def get_workout(split, memory=None):
    phase = memory.get("phase", "hypertrophy") if memory else "hypertrophy"
    rep_scheme = get_rep_scheme(phase)

    blocks = ["strength", "secondary", "accessory", "finisher"]


    block_sizes = {
        "strength": 2,
        "secondary": 3,
        "accessory": 3,
        "finisher": 2
    }

    blocks_output = []

    used_exercises = set()

    for block_type in blocks:
        block_text = f"[{block_type.upper()}]"

        formatted_exercises = []
        if block_type == "finisher":
            all_candidates = pick_exercises(split, block_type, n=10)
        else:
            all_candidates = pick_exercises(split, block_type, n=4)
        # ✅ remove already used ones
        exercises = [ex for ex in all_candidates if ex not in used_exercises]

        # ✅ fallback if everything filtered out
        if not exercises:
            if block_type == "finisher":
                # ✅ skip finisher if no unique movements left
                exercises = []
            else:
                exercises = all_candidates


        # ✅ limit to 2 exercises
        exercises = exercises[:block_sizes[block_type]]

        # ✅ track usage
        used_exercises.update(exercises)

        for ex in exercises:
            progressed_weight = get_progression(memory, ex)

            if block_type == "strength":
                if progressed_weight is not None:
                    formatted_exercises.append(
                        f"{ex} — {rep_scheme['compound']} @ {int(progressed_weight)} lbs"
                    )
                else:
                    formatted_exercises.append(
                        f"{ex} — {rep_scheme['compound']}"
                    )

            elif block_type == "secondary":
                if progressed_weight is not None:
                    formatted_exercises.append(
                        f"{ex} — {rep_scheme['secondary']} @ {int(progressed_weight)} lbs"
                    )
                else:
                    formatted_exercises.append(
                        f"{ex} — {rep_scheme['secondary']}"
                    )

            elif block_type == "finisher":
                formatted_exercises.append(
                    f"{ex} — 2 sets high fatigue (burnout)"
                )

            else:
                if progressed_weight is not None:
                    formatted_exercises.append(
                        f"{ex} — {rep_scheme['accessory']} @ {int(progressed_weight)} lbs"
                    )
                else:
                    formatted_exercises.append(
                        f"{ex} — {rep_scheme['accessory']}"
                    )

        exercises_text = "  \n".join([f"• {ex}" for ex in formatted_exercises])

        blocks_output.append(f"{block_text}\n{exercises_text}")

    return blocks_output

# =========================
# WEEKLY PLANNER ✅
# =========================
def generate_week(memory):

    return {
        "Monday": {
            "run": "🏃 Easy Run — 25 min",
            "lift": get_workout("chest_triceps", memory)
        },
        "Tuesday": {
            "run": "🏃 Easy Run — 30 min",
            "lift": get_workout("back_biceps", memory)
        },
        "Wednesday": {
            "run": "🏃 Long Run — 45–60 min",
            "lift": None
        },
        "Thursday": {
            "run": "🏃 Easy Run — 20 min",
            "lift": get_workout("legs", memory)
        },
        "Friday": {
            "run": "🏃 Easy Run — 20 min",
            "lift": get_workout("arms", memory)
        },
        "Saturday": {
            "run": "🏃 Moderate Run — 30 min",
            "lift": None
        },
        "Sunday": {
            "run": None,
            "lift": None
        }
    }

