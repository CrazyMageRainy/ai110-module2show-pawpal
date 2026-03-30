from dataclasses import dataclass, field, replace
from datetime import date, time, timedelta


def _to_minutes(t: time) -> int:
    """Convert a time object to total minutes since midnight."""
    return t.hour * 60 + t.minute


@dataclass
class TimeSlot:
    start_time: time
    end_time: time
    def __post_init__(self):
        """Validate that end_time is after start_time."""
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")

@dataclass
class Task:
    name: str
    description: str
    duration: int          # in minutes
    priority: int          # 1-10
    preference_rating: int # 1-10
    frequency: str = "once"        # "once", "daily", "weekly"
    scheduled_time: time | None = None
    due_date: date = field(default_factory=date.today)
    is_completed: bool = False

    def __post_init__(self):
        """Validate priority, preference_rating, and frequency values."""
        if not 1 <= self.priority <= 10:
            raise ValueError(f"priority must be between 1 and 10, got {self.priority}")
        if not 1 <= self.preference_rating <= 10:
            raise ValueError(f"preference_rating must be between 1 and 10, got {self.preference_rating}")
        valid_frequencies = {"once", "daily", "weekly"}
        if self.frequency not in valid_frequencies:
            raise ValueError(f"frequency must be one of {valid_frequencies}, got '{self.frequency}'")

    def mark_completed(self) -> None:
        """Mark this task as completed."""
        self.is_completed = True

    def edit_task(self, **kwargs) -> None:
        """Update task attributes with validation on bounded fields."""
        validated = {"priority", "preference_rating"}
        for key, value in kwargs.items():
            if not hasattr(self, key):
                continue
            if key in validated and not 1 <= value <= 10:
                raise ValueError(f"{key} must be between 1 and 10, got {value}")
            setattr(self, key, value)
@dataclass
class Pet:
    name: str
    personal_pet_id: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    @property
    def task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def complete_task(self, task: Task) -> Task | None:
        """Mark a task as completed. If it recurs (daily/weekly), create and add the next occurrence."""
        task.mark_completed()
        if task.frequency == "once":
            return None
        days_ahead = timedelta(days=1) if task.frequency == "daily" else timedelta(weeks=1)
        next_task = replace(task, is_completed=False, due_date=task.due_date + days_ahead)
        self.add_task(next_task)
        return next_task

class Owner:
    def __init__(self):
        self.pets: list[Pet] = []
        self.availability: list[TimeSlot] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return a flat list of all tasks across all pets."""
        return [task for pet in self.pets for task in pet.tasks]


class DailyPlan:
    def __init__(self):
        self.date: date = date.today()
        self.tasks: list[Task] = []
        self.explanation: str = ""

    def view_daily_plan(self) -> None:
        """Print the daily plan with all scheduled tasks and explanation."""
        print(f"Daily Plan for {self.date}")
        for task in self.tasks:
            print(f"  - {task.name} ({task.duration} min)")
        print(f"\nExplanation: {self.explanation}")


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def get_pending_tasks(self) -> list[Task]:
        """Return all tasks that have not been completed yet."""
        return [task for task in self.owner.get_all_tasks() if not task.is_completed]

    def filter_tasks(self, is_completed: bool | None = None, pet_name: str | None = None) -> list[Task]:
        """Filter tasks by completion status, pet name, or both."""
        results = []
        for pet in self.owner.pets:
            if pet_name is not None and pet.name.lower() != pet_name.lower():
                continue
            for task in pet.tasks:
                if is_completed is not None and task.is_completed != is_completed:
                    continue
                results.append(task)
        return results

    def sort_tasks_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority in descending order."""
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    def sort_tasks_by_time(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by scheduled_time ascending, unscheduled tasks go last."""
        return sorted(
            tasks,
            key=lambda t: (t.scheduled_time is None, t.scheduled_time or time.min),
        )

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Detect pairs of tasks whose scheduled times overlap.

        Computes each task's end time using scheduled_time + duration,
        then checks all pairs for overlap. Tasks without a scheduled_time
        are skipped.
        """
        scheduled = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.scheduled_time is not None and not task.is_completed:
                    start = _to_minutes(task.scheduled_time)
                    end = start + task.duration
                    scheduled.append((start, end, task))

        scheduled.sort(key=lambda x: x[0])

        conflicts = []
        for i in range(len(scheduled)):
            for j in range(i + 1, len(scheduled)):
                if scheduled[j][0] < scheduled[i][1]:
                    conflicts.append((scheduled[i][2], scheduled[j][2]))
                else:
                    break
        return conflicts

    def check_conflicts(self) -> list[str]:
        """Return human-readable warning messages for any scheduling conflicts."""
        conflicts = self.detect_conflicts()
        warnings = []
        for t1, t2 in conflicts:
            t1_end_min = _to_minutes(t1.scheduled_time) + t1.duration
            warnings.append(
                f"Warning: '{t1.name}' ({t1.scheduled_time.strftime('%H:%M')}-"
                f"{t1_end_min // 60:02d}:{t1_end_min % 60:02d}) overlaps with "
                f"'{t2.name}' (starts {t2.scheduled_time.strftime('%H:%M')}). "
                f"Consider rescheduling one of them."
            )
        return warnings

    def generate_plan(self) -> DailyPlan:
        """Generate a daily plan by scheduling pending tasks within available time."""
        plan = DailyPlan()
        pending = self.get_pending_tasks()
        sorted_tasks = self.sort_tasks_by_priority(pending)

        available_minutes = 0
        for slot in self.owner.availability:
            start = _to_minutes(slot.start_time)
            end = _to_minutes(slot.end_time)
            available_minutes += end - start

        scheduled_minutes = 0
        for task in sorted_tasks:
            if scheduled_minutes + task.duration <= available_minutes:
                plan.tasks.append(task)
                scheduled_minutes += task.duration

        plan.explanation = (
            f"Scheduled {len(plan.tasks)} task(s) within "
            f"{available_minutes} available minutes by priority."
        )
        return plan
