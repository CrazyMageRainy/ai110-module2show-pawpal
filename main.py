from datetime import time
from pawpal_system import TimeSlot, Task, Owner, Pet, Scheduler

owner1 = Owner()
pet1 = Pet("SnowBall", "1", "Dog")
pet2 = Pet("Squak", "2", "Bird")

task1 = Task("Morning Walk", "Take SnowBall for a walk around the park", 30, 8, 9, frequency="daily")
task2 = Task("Feeding", "Feed SnowBall breakfast", 10, 10, 7, frequency="daily")
task3 = Task("Bath Time", "Give SnowBall a bath", 45, 5, 4, frequency="weekly")
task7 = Task("Vet Visit", "Annual checkup for SnowBall", 60, 9, 3, frequency="once")

pet1.add_task(task1)
pet1.add_task(task2)
pet1.add_task(task3)
pet1.add_task(task7)
# A lot of manual setup for pets, tasks. WHich then insert into the Owner
task4 = Task("Cage Cleaning", "Clean Squak's cage thoroughly", 20, 7, 6, frequency="weekly")
task5 = Task("Seed Refill", "Refill Squak's food and water", 5, 9, 8, frequency="daily")
task6 = Task("Playtime", "Let Squak out for supervised flying time", 15, 6, 9, frequency="daily")

pet2.add_task(task4)
pet2.add_task(task5)
pet2.add_task(task6)

owner1.add_pet(pet1)
owner1.add_pet(pet2)
owner1.availability = [TimeSlot(time(7, 0), time(9, 0))]

scheduler = Scheduler(owner1)

# Complete a recurring task — auto-creates next occurrence
print("=== Recurring Task Completion ===")
print(f"Completing '{task2.name}' (frequency: {task2.frequency}, due: {task2.due_date})")
next_task = pet1.complete_task(task2)
if next_task:
    print(f"  -> Next occurrence created: '{next_task.name}' (due: {next_task.due_date})")
print(f"  -> Original completed: {task2.is_completed}")

# Complete a weekly task
print(f"\nCompleting '{task3.name}' (frequency: {task3.frequency}, due: {task3.due_date})")
next_task3 = pet1.complete_task(task3)
if next_task3:
    print(f"  -> Next occurrence created: '{next_task3.name}' (due: {next_task3.due_date})")
else:
    print(f"  -> No next occurrence (one-time task)")

# Complete a one-time task — no new instance
print(f"\nCompleting '{task7.name}' (frequency: {task7.frequency}, due: {task7.due_date})")
next_task7 = pet1.complete_task(task7)
if next_task7:
    print(f"  -> Next occurrence created: '{next_task7.name}' (due: {next_task7.due_date})")
else:
    print(f"  -> No next occurrence (one-time task)")
print()

# Filter tasks by completion status
print("=== Incomplete Tasks ===")
for t in scheduler.filter_tasks(is_completed=False):
    print(f"  - {t.name} (done: {t.is_completed})")

print("\n=== Completed Tasks ===")
for t in scheduler.filter_tasks(is_completed=True):
    print(f"  - {t.name} (done: {t.is_completed})")

# Filter tasks by pet name
print("\n=== Squak's Tasks ===")
for t in scheduler.filter_tasks(pet_name="Squak"):
    print(f"  - {t.name}")

# Filter by both
print("\n=== SnowBall's Incomplete Tasks ===")
for t in scheduler.filter_tasks(is_completed=False, pet_name="SnowBall"):
    print(f"  - {t.name}")

# Sort by priority
print("\n=== Tasks Sorted by Priority ===")
for t in scheduler.sort_tasks_by_priority(scheduler.get_pending_tasks()):
    print(f"  - {t.name} (priority: {t.priority})")

# Sort by time — assign times to a few tasks first
task1.scheduled_time = time(7, 0)    # Morning Walk: 7:00 - 7:30 (30 min)
task5.scheduled_time = time(7, 0)    # Seed Refill:  7:00 - 7:05 (5 min) — exact same start time!
task4.scheduled_time = time(8, 0)    # Cage Cleaning: 8:00 - 8:20 (20 min)
task6.scheduled_time = time(8, 0)    # Playtime:      8:00 - 8:15 (15 min) — exact same start time!

print("\n=== Tasks Sorted by Scheduled Time ===")
for t in scheduler.sort_tasks_by_time(owner1.get_all_tasks()):
    print(f"  - {t.name} (time: {t.scheduled_time}, duration: {t.duration} min)")

# Lightweight conflict check — warnings instead of crashes
print("\n=== Conflict Check (Warnings) ===")
warnings = scheduler.check_conflicts()
if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts found.")

# Fix conflicts and re-check
print("\n=== After Fixing Conflicts ===")
task5.scheduled_time = time(7, 30)   # Move Seed Refill after Morning Walk ends
task6.scheduled_time = time(8, 20)   # Move Playtime after Cage Cleaning ends
warnings = scheduler.check_conflicts()
if warnings:
    for w in warnings:
        print(f"  {w}")
else:
    print("  No conflicts found.")

# Generate daily plan
print()
daily_plan = scheduler.generate_plan()
daily_plan.view_daily_plan()

# filter_tasks(is_completed=False) — shows the 5 incomplete tasks (Feeding was marked completed)
# filter_tasks(is_completed=True) — shows only Feeding
# filter_tasks(pet_name="Squak") — shows Squak's 3 tasks regardless of status
# filter_tasks(is_completed=False, pet_name="SnowBall") — combines both filters
# sort_tasks_by_priority() — orders pending tasks from priority 9 down to 5
# sort_tasks_by_time() — tasks with assigned times come first in HH:MM order, None tasks at the end
# generate_plan() — fits all 5 pending tasks into the 120-minute window