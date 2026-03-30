from dataclasses import dataclass, field
from datetime import date, time


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

    # def edit_task(self, **kwargs) -> None:
    #     for key, value in kwargs.items():
    #         if hasattr(self, key):
    #             setattr(self, key, value)
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
    task_count: int = 0
    tasks: list[Task] = field(default_factory=list)
    def add_task(self, task: Task) -> None:
        """Add a task to this pet and increment the task count."""
        self.tasks.append(task)
        self.task_count += 1 

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

    def get_available_slots(self) -> list[TimeSlot]:
        """Return the owner's available time slots."""
        return self.availability


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

    def sort_tasks_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks by priority in descending order."""
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    def generate_plan(self) -> DailyPlan:
        """Generate a daily plan by scheduling pending tasks within available time."""
        plan = DailyPlan()
        pending = self.get_pending_tasks()
        sorted_tasks = self.sort_tasks_by_priority(pending)

        available_minutes = 0
        for slot in self.owner.get_available_slots():
            start = slot.start_time.hour * 60 + slot.start_time.minute
            end = slot.end_time.hour * 60 + slot.end_time.minute
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
