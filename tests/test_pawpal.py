from datetime import date, timedelta

from pawpal_system import Owner, Pet, Schedule, Task


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


def test_schedule_generate_populates_scheduled_tasks() -> None:
    owner = Owner(name="Jordan", availability_minutes=40)
    pet = Pet(name="Mochi", species="Cat", age=2, breed="Tabby")
    owner.add_pet(pet)

    pet.add_task(Task(title="Morning walk", duration_minutes=20, priority=3))
    pet.add_task(Task(title="Feed dinner", duration_minutes=15, priority=2))

    schedule = Schedule()
    schedule.generate(owner, owner.get_all_tasks())

    assert len(schedule.scheduled_tasks) == 2
    assert schedule.scheduled_tasks[0].title == "Morning walk"
    assert schedule.scheduled_tasks[1].title == "Feed dinner"


def test_mark_complete_creates_next_occurrence_for_daily_tasks() -> None:
    task = Task(
        title="Feed breakfast",
        duration_minutes=10,
        priority=2,
        recurring=True,
        frequency="daily",
        time_of_day="08:00",
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.frequency == "daily"
    assert next_task.title == "Feed breakfast"


def test_mark_complete_sets_next_due_date_for_daily_and_weekly_tasks() -> None:
    daily_task = Task(
        title="Feed breakfast",
        duration_minutes=10,
        priority=2,
        recurring=True,
        frequency="daily",
        due_date=date(2026, 7, 6),
    )
    weekly_task = Task(
        title="Grooming",
        duration_minutes=15,
        priority=2,
        recurring=True,
        frequency="weekly",
        due_date=date(2026, 7, 6),
    )

    next_daily_task = daily_task.mark_complete()
    next_weekly_task = weekly_task.mark_complete()

    assert next_daily_task is not None
    assert next_daily_task.due_date == date(2026, 7, 7)
    assert next_weekly_task is not None
    assert next_weekly_task.due_date == date(2026, 7, 13)


def test_get_all_tasks_filters_by_pet_and_completion() -> None:
    owner = Owner(name="Jordan", availability_minutes=60)
    pet1 = Pet(name="Mochi", species="Cat", age=2, breed="Tabby")
    pet2 = Pet(name="Buddy", species="Dog", age=4, breed="Beagle")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(title="Feed breakfast", duration_minutes=10, priority=1)
    task2 = Task(title="Grooming", duration_minutes=15, priority=2)
    task2.mark_complete()
    pet1.add_task(task1)
    pet1.add_task(task2)

    tasks = owner.get_all_tasks(pet_name="Mochi")

    assert task1 in tasks
    assert task2 not in tasks

    all_tasks = owner.get_all_tasks(pet_name="Mochi", include_completed=True)
    assert task1 in all_tasks
    assert task2 in all_tasks


def test_generate_schedule_detects_conflicts() -> None:
    owner = Owner(name="Jordan", availability_minutes=20)
    pet = Pet(name="Mochi", species="Cat", age=2, breed="Tabby")
    owner.add_pet(pet)

    pet.add_task(Task(title="Morning walk", duration_minutes=15, priority=3, recurring=True))
    pet.add_task(Task(title="Feed dinner", duration_minutes=15, priority=2))

    schedule = Schedule()
    schedule.generate(owner, owner.get_all_tasks())

    assert len(schedule.scheduled_tasks) == 1
    assert len(schedule.conflicts) == 1
    assert schedule.conflicts[0].title == "Feed dinner"


def test_sort_by_time_orders_tasks_by_hhmm_strings() -> None:
    schedule = Schedule()
    schedule.scheduled_tasks = [
        Task(title="Feed dinner", duration_minutes=10, priority=2, time_of_day="19:30"),
        Task(title="Morning walk", duration_minutes=20, priority=3, time_of_day="08:00"),
        Task(title="Lunch break", duration_minutes=15, priority=1, time_of_day="12:15"),
    ]

    schedule.sort_by_time()

    assert [task.title for task in schedule.scheduled_tasks] == [
        "Morning walk",
        "Lunch break",
        "Feed dinner",
    ]
