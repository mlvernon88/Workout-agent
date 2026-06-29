from agent import load_memory, save_memory, generate_plan

def log_workout(memory):
    day = input("Day: ")
    workout_type = input("Workout type (run/lift): ")
    completed = input("Completed? (y/n): ") == "y"

    entry = {
        "day": day,
        "type": workout_type,
        "completed": completed
    }

    if workout_type == "run" and completed:
        run_type = input("Run type (easy/tempo/long/recovery): ")
        time = input("Time (minutes): ")
        pace = input("Average pace (e.g. 9:30): ")
        effort = int(input("Effort (1-10): "))

        entry.update({
            "run_type": run_type,
            "time": time,
            "pace": pace,
            "effort": effort
        })

    elif workout_type == "lift" and completed:
        print("\nEnter all lifts (one per line). Format: Exercise WeightxReps")
        print("Example: Flat Bench Press 185x10")
        print("Type 'done' when finished\n")

        while True:
            line = input("> ")

            if line.lower() == "done":
                save_memory(memory)
                print("✅ Workout logged.\n")
                return

            try:
                parts = line.rsplit(" ", 1)
                exercise = parts[0]
                weight_reps = parts[1]

                sets = weight_reps.split(",")

                weights = []
                reps = []

                for s in sets:
                    w, r = s.split("x")
                    weights.append(float(w))
                    reps.append(int(r))

                entry = {
                    "day": day,
                    "type": "lift",
                    "completed": True,
                    "exercise": exercise.strip(),
                    "weights": weights,   # ✅ list of weights
                    "reps": reps          # ✅ list of reps
                }

                memory["workouts"].append(entry)
                print("✅ SAVED:", entry)

            except Exception as e:
                print("❌ ERROR:", e)

    save_memory(memory)

    print("✅ Workout logged.\n")


def update_fatigue(memory):
    fatigue = int(input("Enter fatigue level (1-10): "))
    memory["fatigue"] = fatigue
    save_memory(memory)
    print("✅ Fatigue updated.\n")


def show_plan(memory):
    plan = generate_plan(memory)

    print("\n📅 YOUR ADAPTIVE WEEKLY PLAN:\n")
    for p in plan:
        print(p)


def main():
    memory = load_memory()

    while True:
        print("\n=== Adaptive Training Agent ===")
        print("1. Log workout")
        print("2. Update fatigue")
        print("3. Generate weekly plan")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            log_workout(memory)

        elif choice == "2":
            update_fatigue(memory)

        elif choice == "3":
            show_plan(memory)

        elif choice == "4":
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()