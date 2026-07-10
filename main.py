from pawpal_system import Owner, Pet, Schedule, Task


def main():
    # Create an owner with specific availability and preferences
    owner = Owner(name="Mekayla", availability_minutes=90)
    owner.set_preference("walk")
    owner.set_preference("feeding")

    # Create pets and add tasks to them out of order
    pet1 = Pet(name="Luna", species="dog", age=5, breed="Labrador")
    pet1.add_task(Task(title="Feeding", duration_minutes=15, priority=4, time_of_day="19:30"))
    pet1.add_task(Task(title="Morning walk", duration_minutes=30, priority=5, time_of_day="08:00"))

    pet2 = Pet(name="Bruno", species="cat", age=3, breed="pitbull")
    pet2.add_task(Task(title="Grooming", duration_minutes=10, priority=2, time_of_day="17:00"))
    pet2.add_task(Task(title="Playtime", duration_minutes=20, priority=3, time_of_day="14:00"))

    # Add a same-time overlap to demonstrate conflict detection
    pet2.add_task(Task(title="Nap time", duration_minutes=10, priority=3, time_of_day="14:00"))

    # Add pets to the owner's collection
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Mark one task as complete to demonstrate completion filtering and recurring re-queueing
    pet1.mark_task_complete(pet1.tasks[0])

    # Generate a schedule from the filtered, pending tasks
    pending_tasks = owner.filter_tasks(include_completed=False)
    schedule = Schedule()
    schedule.generate_schedule(owner, pending_tasks)
    schedule.sort_by_time()

    # Print the scheduled tasks with owner and pet associations
    print("Today's Schedule")
    print(f"Owner: {owner.name}\n")

    print("Pending tasks for all pets (sorted by time):")
    for task in schedule.scheduled_tasks:
        pet = next(pet for pet in owner.pets if task in pet.tasks)
        print(f"Pet: {pet.name}")
        print(f"Task: {task.title}")
        print(f"Time: {task.time_of_day}")
        print(f"Duration: {task.duration_minutes} minutes")
        print(f"Priority: {task.priority}\n")

    if schedule.time_conflict_warnings:
        print("Time conflict warnings:")
        for warning in schedule.time_conflict_warnings:
            print(f"- {warning}")
    else:
        print("No time conflicts detected.")

    print("\nTasks for Luna only:")
    for task in owner.filter_tasks(pet_name="Luna"):
        status = "done" if task.completed else "pending"
        print(f"- {task.title} ({status})")

    print("\nAll tasks including completed ones:")
    for task in owner.filter_tasks(include_completed=True):
        status = "done" if task.completed else "pending"
        print(f"- {task.title} ({status})")


if __name__ == "__main__":
    main()