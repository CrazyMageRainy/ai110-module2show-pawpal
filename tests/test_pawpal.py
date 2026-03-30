from pawpal_system import Task, Pet


def test_mark_completed_changes_status():
    task = Task(name="Walk", description="Morning walk", duration=30, priority=5, preference_rating=7)
    assert task.is_completed is False
    task.mark_completed()
    assert task.is_completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Buddy", personal_pet_id="P001", species="Dog", task_count=0)
    task = Task(name="Feed", description="Evening meal", duration=10, priority=8, preference_rating=9)
    pet.add_task(task)
    assert pet.task_count == 1
