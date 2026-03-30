from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class TimeSlot:
    start_time: time
    end_time: time
    def __post_init__(self):
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
        if not 1 <= self.priority <= 10:
            raise ValueError(f"priority must be between 1 and 10, got {self.priority}")
        if not 1 <= self.preference_rating <= 10:
            raise ValueError(f"preference_rating must be between 1 and 10, got {self.preference_rating}")
        valid_frequencies = {"once", "daily", "weekly"}
        if self.frequency not in valid_frequencies:
            raise ValueError(f"frequency must be one of {valid_frequencies}, got '{self.frequency}'")

    def mark_completed(self) -> None:
        self.is_completed = True

    # def edit_task(self, **kwargs) -> None:
    #     for key, value in kwargs.items():
    #         if hasattr(self, key):
    #             setattr(self, key, value)
    def edit_task(self, **kwargs) -> None:
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

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

class Owner:
    def __init__(self):
        self.pets: list[Pet] = []
        self.availability: list[TimeSlot] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        return [task for pet in self.pets for task in pet.tasks]

    def get_available_slots(self) -> list[TimeSlot]:
        return self.availability


class DailyPlan:
    def __init__(self):
        self.date: date = date.today()
        self.tasks: list[Task] = []
        self.explanation: str = ""

    def view_daily_plan(self) -> None:
        print(f"Daily Plan for {self.date}")
        for task in self.tasks:
            print(f"  - {task.name} ({task.duration} min)")
        print(f"\nExplanation: {self.explanation}")

    def generate_plan(self, owner: Owner) -> None:
        # TODO: implement scheduling logic using owner.get_all_tasks() and owner.availability
        pass
