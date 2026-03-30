from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Pet:
    name: str
    personal_pet_id: str
    species: str


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
    duration: int          # in minutes
    priority: int
    preference_rating: int
    pet: Pet

    def __post_init__(self):
        if not 1 <= self.priority <= 10:
            raise ValueError(f"priority must be between 1 and 10, got {self.priority}")
        if not 1 <= self.preference_rating <= 10:
            raise ValueError(f"preference_rating must be between 1 and 10, got {self.preference_rating}")

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


class Owner:
    def __init__(self):
        self.pets: list[Pet] = []
        self.availability: list[TimeSlot] = []
        self.task_list: list[Task] = []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_available_slots(self) -> list[TimeSlot]:
        return self.availability

    def create_task(self, task: Task) -> None:
        self.task_list.append(task)


class DailyPlan:
    def __init__(self):
        self.date: date = date.today()
        self.tasks: list[Task] = []
        self.explanation: str = ""

    def view_daily_plan(self) -> None:
        print(f"Daily Plan for {self.date}")
        for task in self.tasks:
            print(f"  - {task.name} ({task.duration} min) for {task.pet.name}")
        print(f"\nExplanation: {self.explanation}")

    def generate_plan(self, owner: Owner) -> None:
        # TODO: implement scheduling logic using owner.task_list and owner.availability
        pass
