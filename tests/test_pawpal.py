from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task, TimeSlot


def test_mark_completed_changes_status():
    task = Task(name="Walk", description="Morning walk", duration=30, priority=5, preference_rating=7)
    assert task.is_completed is False
    task.mark_completed()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", personal_pet_id="P001", species="Dog")
    task = Task(name="Feed", description="Evening meal", duration=10, priority=8, preference_rating=9)
    pet.add_task(task)
    assert pet.task_count == 1


# --- Sorting Correctness ---

def test_sort_tasks_by_time_chronological_order():
    """Tasks with scheduled times are returned earliest-first."""
    owner = Owner()
    pet = Pet(name="Rex", personal_pet_id="P01", species="Dog")
    t1 = Task(name="Walk", description="", duration=30, priority=5, preference_rating=5, scheduled_time=time(9, 0))
    t2 = Task(name="Feed", description="", duration=10, priority=8, preference_rating=5, scheduled_time=time(7, 0))
    t3 = Task(name="Play", description="", duration=15, priority=3, preference_rating=5, scheduled_time=time(8, 0))
    pet.add_task(t1)
    pet.add_task(t2)
    pet.add_task(t3)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_time([t1, t2, t3])

    assert [t.name for t in sorted_tasks] == ["Feed", "Play", "Walk"]


def test_sort_tasks_by_time_unscheduled_go_last():
    """Tasks without a scheduled_time appear after all scheduled tasks."""
    t_scheduled = Task(name="Walk", description="", duration=30, priority=5, preference_rating=5, scheduled_time=time(10, 0))
    t_unscheduled = Task(name="Groom", description="", duration=20, priority=9, preference_rating=5)

    owner = Owner()
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_time([t_unscheduled, t_scheduled])

    assert sorted_tasks[0].name == "Walk"
    assert sorted_tasks[1].name == "Groom"


# --- Recurrence Logic ---

def test_complete_daily_task_creates_next_day_occurrence():
    """Completing a daily task creates a new task due tomorrow with same attributes."""
    today = date.today()
    pet = Pet(name="Buddy", personal_pet_id="P01", species="Dog")
    task = Task(
        name="Feed", description="Morning meal", duration=10,
        priority=8, preference_rating=7, frequency="daily", due_date=today,
    )
    pet.add_task(task)

    next_task = pet.complete_task(task)

    assert task.is_completed is True
    assert next_task is not None
    assert next_task.is_completed is False
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.name == "Feed"
    assert next_task.frequency == "daily"
    assert pet.task_count == 2


def test_complete_once_task_creates_no_recurrence():
    """Completing a one-time task returns None and adds no new task."""
    pet = Pet(name="Buddy", personal_pet_id="P01", species="Dog")
    task = Task(name="Vet Visit", description="Checkup", duration=60, priority=10, preference_rating=5, frequency="once")
    pet.add_task(task)

    result = pet.complete_task(task)

    assert result is None
    assert pet.task_count == 1


# --- Conflict Detection ---

def test_detect_conflicts_overlapping_tasks():
    """Two tasks scheduled at the same time are flagged as a conflict."""
    owner = Owner()
    pet = Pet(name="Rex", personal_pet_id="P01", species="Dog")
    t1 = Task(name="Walk", description="", duration=30, priority=5, preference_rating=5, scheduled_time=time(7, 0))
    t2 = Task(name="Feed", description="", duration=15, priority=8, preference_rating=5, scheduled_time=time(7, 0))
    pet.add_task(t1)
    pet.add_task(t2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert conflicts[0] == (t1, t2)


def test_detect_conflicts_adjacent_tasks_no_conflict():
    """Tasks that are back-to-back (no overlap) should not be flagged."""
    owner = Owner()
    pet = Pet(name="Rex", personal_pet_id="P01", species="Dog")
    t1 = Task(name="Walk", description="", duration=30, priority=5, preference_rating=5, scheduled_time=time(7, 0))
    t2 = Task(name="Feed", description="", duration=15, priority=8, preference_rating=5, scheduled_time=time(7, 30))
    pet.add_task(t1)
    pet.add_task(t2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 0


def test_detect_conflicts_ignores_completed_tasks():
    """Completed tasks should not appear in conflict detection."""
    owner = Owner()
    pet = Pet(name="Rex", personal_pet_id="P01", species="Dog")
    t1 = Task(name="Walk", description="", duration=30, priority=5, preference_rating=5, scheduled_time=time(7, 0))
    t2 = Task(name="Feed", description="", duration=15, priority=8, preference_rating=5, scheduled_time=time(7, 0), is_completed=True)
    pet.add_task(t1)
    pet.add_task(t2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 0
