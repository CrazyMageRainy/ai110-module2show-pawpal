# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

### Smarter Scheduling
New methods in Scheduler
filter_tasks(is_completed, pet_name) — Filter tasks by completion status, pet name, or both
sort_tasks_by_time(tasks) — Sort tasks by scheduled_time ascending, unscheduled tasks go last
detect_conflicts() — Find all pairs of scheduled tasks whose time ranges overlap
check_conflicts() — Lightweight wrapper that returns warning strings instead of raw tuples


### Testing PawPal+
__SORTING__
test_sort_tasks_by_time_chronological_order:	Tasks come back in earliest-first order regardless of insertion order 2
test_sort_tasks_by_time_unscheduled_go_last:	Tasks with no scheduled_time sort after all scheduled tasks 2
__Recurrence__
test_complete_daily_task_creates_next_day_occurrence: Daily task completion creates a new uncompleted task due tomorrow with same attributes 2
test_complete_once_task_creates_no_recurrence: One-time task returns None and no new task is added 4
__Conflicts__
	test_detect_conflicts_overlapping_tasks:Two tasks at the same time are flagged as a conflict 4
    test_detect_conflicts_adjacent_tasks_no_conflict: flict	Back-to-back tasks (end time = start time) are NOT flagged 3
    test_detect_conflicts_ignores_completed_tasks: Completed tasks are excluded from conflict checks 4

command: ``python -m pytest``