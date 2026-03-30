from datetime import time
from pawpal_system import TimeSlot, Task, Owner, Pet, Scheduler

owner1 = Owner()
pet1 = Pet("SnowBall", "1", "Dog")
pet2 = Pet("Squak", "2", "Bird")

task1 = Task("Morning Walk", "Take SnowBall for a walk around the park", 30, 8, 9, frequency="daily")
task2 = Task("Feeding", "Feed SnowBall breakfast", 10, 10, 7, frequency="daily")
task3 = Task("Bath Time", "Give SnowBall a bath", 45, 5, 4, frequency="weekly")

pet1.add_task(task1)
pet1.add_task(task2)
pet1.add_task(task3)
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
daily_plan = scheduler.generate_plan()
daily_plan.view_daily_plan()
