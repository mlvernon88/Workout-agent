def generate_explanation(adjustment, stats, fatigue):
    return f"""
Adjustments Made: {adjustment['intensity'].upper()}

Reason:
- Completed workouts: {stats['completed']}
- Missed workouts: {stats['missed']}
- Fatigue level: {fatigue}/10

Decision logic:
{adjustment['reason']}
"""