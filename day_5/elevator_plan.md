# Elevator plan — Day 5 ✅

## Summary
This document records the optimal stop sequence and timing for the scenario:
- Elevator starts at **floor 5**
- Person 1: at **floor 2** → destination **floor 1**
- Person 2: at **floor 10** → destination **floor 6**
- Person 3: at **floor 15** → destination **floor 19**

Travel assumptions:
- Travel time = **1 time unit per floor**
- Boarding/door overhead ignored
- "Wait time" = time from now until elevator arrives to pick up the person

---

## Optimal stop order (minimize average pickup wait) 🔧
**Floor sequence (stops):**
`5 → 2 → 10 → 15 → 19 → 10 → 6 → 1`

### Pickup times (when elevator arrives to pick up each person)
- **Person 1 (floor 2)** picked at t = |5 − 2| = **3**
- **Person 2 (floor 10)** picked at t = 3 + |2 − 10| = **11**
- **Person 3 (floor 15)** picked at t = 11 + |10 − 15| = **16**

**Average pickup wait** = (3 + 11 + 16) / 3 = **10** units
**Maximum wait** = **16** units

### Arrival (drop-off) times
- **Person 3** arrives at floor 19 at t = 16 + |15 − 19| = **20**
- **Person 2** arrives at floor 6 at t = 20 + |19 − 10| + |10 − 6| = **33**
- **Person 1** arrives at floor 1 at t = 33 + |6 − 1| = **38**

**Total elevator travel/time** = **38** units

---

## Alternative sequence (minimize total travel) 🔁
**Floor sequence (stops):**
`5 → 15 → 19 → 10 → 6 → 2 → 1`

### Pickup times (when elevator arrives to pick up each person)
- **Person 3 (floor 15)** picked at t = |5 − 15| = **10**
- **Person 2 (floor 10)** picked at t = 10 + |15 − 19| + |19 − 10| = **23**
- **Person 1 (floor 2)** picked at t = 23 + |10 − 6| + |6 − 2| = **31**

**Average pickup wait** = (10 + 23 + 31) / 3 = **≈ 21.33** units
**Maximum wait** = **31** units

### Arrival (drop-off) times
- **Person 3** arrives at floor 19 at t = 10 + |15 − 19| = **14**
- **Person 2** arrives at floor 6 at t = 14 + |19 − 10| + |10 − 6| = **27**
- **Person 1** arrives at floor 1 at t = 27 + |6 − 2| + |2 − 1| = **32**

**Total elevator travel/time** = **32** units

---

## Comparison of candidate sequences 📊
| Metric | Sequence A — minimize pickup wait | Sequence B — minimize total travel |
|---|---:|---:|
| Floor sequence | `5 → 2 → 10 → 15 → 19 → 10 → 6 → 1` | `5 → 15 → 19 → 10 → 6 → 2 → 1` |
| Average pickup wait | **10** | **≈ 21.33** |
| Maximum pickup wait | **16** | **31** |
| Total travel/time | **38** | **32** |
| Average arrival time | **≈ 30.33** | **≈ 24.33** |

**Recommendation:**
- Use **Sequence A** if your priority is minimizing passenger pickup wait and fairness (lower average and max wait).
- Use **Sequence B** if your priority is minimizing total elevator travel or average arrival time, accepting higher pickup waits for some passengers.

---

## Notes & trade-offs 💡
- This sequence prioritizes minimizing **average pickup wait** (the time until people are picked up). Dropping a passenger immediately when picked (e.g., returning to 1 after picking P1 at 2) increases pickup times for others.
- If you prefer minimizing **maximum wait**, **total travel**, or **average arrival time**, the stop order may change—tell me which metric you'd like to optimize and I can recompute.
- If you'd like door/boarding overhead included, specify the per-stop overhead and I'll update the times.

---

## Next steps (for iteration) ✅
- Edit this file for alternate objectives or add boarding overheads.
- I can add a small script (`day_5/elevator.py`) to compute optimal sequences for arbitrary inputs if you want programmatic exploration.

---

*File: `day_5/elevator_plan.md`*