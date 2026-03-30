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


@dataclass
class Task:
    name: str
    duration: int          # in minutes
    priority: int
    preference_rating: int
    pet: Pet

    def edit_task(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
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
