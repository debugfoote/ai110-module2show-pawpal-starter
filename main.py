from pawpal_system import Owner, Pet, Schedule, Task

def main():
    # Create an owner with specific availability and preferences
    owner = Owner(name="Mekayla", availability_minutes=90)
    owner.set_preference("walk")
    owner.set_preference("feeding")

    # Create pets and add tasks to them
    pet1 = Pet(name="Luna", species="dog", age=5, breed="Labrador")
    pet1.add_task(Task(title="Morning walk", duration_minutes=30, priority=5))
    pet1.add_task(Task(title="Feeding", duration_minutes=15, priority=4))

    pet2 = Pet(name="Bruno", species="cat", age=3, breed="pitbull")
    pet2.add_task(Task(title="Playtime", duration_minutes=20, priority=3))
    pet2.add_task(Task(title="Grooming", duration_minutes=10, priority=2))

    # Add pets to the owner's collection
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # Generate a schedule based on the owner's constraints and preferences
    schedule = Schedule()
    schedule.generate_schedule(owner, owner.get_all_tasks())

    # Print the scheduled tasks with owner and pet associations
    print("Today's Schedule")
    print(f"Owner: {owner.name}\n")

    for pet in owner.pets:
        for task in pet.tasks:
            if task in schedule.scheduled_tasks:
                print(f"Pet: {pet.name}")
                print(f"Task: {task.title}")
                print(f"Duration: {task.duration_minutes} minutes")
                print(f"Priority: {task.priority}\n")

if __name__ == "__main__":
    main()