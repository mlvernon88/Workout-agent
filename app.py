import streamlit as st

st.set_page_config(
    page_title="Training Agent",
    layout="centered"
)

from datetime import datetime

import json
import os

import workouts

def load_memory():
    file_path = os.path.join(os.path.dirname(__file__), "memory.json")

    with open(file_path, "r") as f:
        return json.load(f)

def save_memory(memory):
    file_path = os.path.join(os.path.dirname(__file__), "memory.json")

    with open(file_path, "w") as f:
        json.dump(memory, f, indent=2)

from workouts import get_workout

st.title("🏋️ Training Agent")
st.subheader("Hybrid Strength + Run Program")

# ✅ Button
# ✅ Initialize once
if "week" not in st.session_state:
    st.session_state.week = None


# ✅ Side-by-side buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Generate Weekly Plan", key="generate_week"):
        memory = load_memory()
        st.session_state.week = workouts.generate_week(memory)

with col2:
    if st.button("Clear Plan", key="clear_week"):
        st.session_state.week = None



# ✅ Use stored plan
week = st.session_state.week

from datetime import datetime
today = datetime.now().strftime("%A")

if week:
    for day, plan in week.items():
        if day == today:
            label = f"🔥 TODAY — {day}"
        else:
            label = f"📅 {day}"

        with st.expander(label, expanded=(day == today)):
            if plan["run"]:
                st.markdown("#### 🏃 Run (Primary)")
                st.markdown(plan["run"])

            if plan["lift"]:
                st.markdown("#### 🏋️ Lift (Secondary)")
                for block in plan["lift"]:
                    st.code(block)

            if not plan["run"] and not plan["lift"]:
                st.info("😴 Rest Day — Recovery")

# Divider
st.markdown("---")
st.subheader("📥 Log Workout")

log_input = st.text_area(
    "Enter workout (e.g. Flat Bench Press 135x8,145x8,145x8)"
)
if st.button("Log Workout"):
    if log_input:
        try:
            memory = load_memory()

            if "workouts" not in memory:
                memory["workouts"] = []

            parts = log_input.rsplit(" ", 1)
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
                "type": "lift",
                "exercise": exercise.strip(),
                "weights": weights,
                "reps": reps
            }

            memory["workouts"].append(entry)

            save_memory(memory)

            st.success("✅ Workout logged successfully!")

        except Exception as e:
            st.error(f"❌ Error: {e}")
