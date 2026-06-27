from pawpal_system import Pet, Task


def test_mark_complete_updates_task_status() -> None:
    task = Task(title="Walk the dog", duration_minutes=20, priority=2)

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Milo", species="Dog", age=3, breed="Golden Retriever")
    task = Task(title="Feed dinner", duration_minutes=10, priority=1)
    initial_task_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == initial_task_count + 1
