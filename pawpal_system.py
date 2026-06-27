from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Task:
    """Represents one pet-care activity such as a walk, feed, or grooming session."""

    title: str
    duration_minutes: int
    priority: int
    recurring: bool = False
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def update_duration(self, minutes: int) -> None:
        """Update the task duration, rejecting invalid values."""
        if minutes <= 0:
            raise ValueError("Task duration must be positive")
        self.duration_minutes = minutes

    def is_eligible(self) -> bool:
        """Return True when the task is still pending."""
        return not self.completed

    def matches_preference(self, preference: str) -> bool:
        """Check whether a task title reflects an owner preference."""
        if not preference:
            return False
        return preference.lower() in self.title.lower()

    def effective_priority(self, preferences: List[str] | None = None) -> int:
        """Compute a scheduling score that includes preference and recurring bonuses."""
        score = self.priority
        if self.recurring:
            score += 2
        if preferences:
            for preference in preferences:
                if self.matches_preference(preference):
                    score += 3
                    break
        return score


@dataclass
class Pet:
    """Stores pet information and owns the tasks that belong to that pet."""

    name: str
    species: str
    age: int
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a new task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from the pet's collection."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_pending_tasks(self) -> List[Task]:
        """Return only tasks that are still pending."""
        return [task for task in self.tasks if task.is_eligible()]

    def update_info(
        self,
        name: str | None = None,
        species: str | None = None,
        age: int | None = None,
        breed: str | None = None,
    ) -> None:
        """Update pet information fields."""
        if name is not None:
            self.name = name
        if species is not None:
            self.species = species
        if age is not None:
            self.age = age
        if breed is not None:
            self.breed = breed


@dataclass
class Owner:
    """Represents the person who owns the pets and provides constraints for planning."""

    name: str
    availability_minutes: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        if pet not in self.pets:
            self.pets.append(pet)

    def set_preference(self, pref: str) -> None:
        """Add a new owner preference if it does not already exist."""
        if pref and pref not in self.preferences:
            self.preferences.append(pref)

    def update_availability(self, minutes: int) -> None:
        """Update the owner's available time in minutes."""
        if minutes < 0:
            raise ValueError("Availability cannot be negative")
        self.availability_minutes = minutes

    def get_all_tasks(self) -> List[Task]:
        """Collect pending tasks from every pet owned by the owner."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.get_pending_tasks())
        return tasks


@dataclass
class Schedule:
    """Builds and explains a daily plan that fits an owner's time and preferences."""

    date: str = field(default_factory=lambda: date.today().isoformat())
    scheduled_tasks: List[Task] = field(default_factory=list)
    owner: Owner | None = None

    def generate_schedule(self, owner: Owner, tasks: List[Task]) -> None:
        """Generate a schedule from an owner and a list of tasks."""
        self.owner = owner
        eligible_tasks = [task for task in tasks if task.is_eligible()]
        prioritized_tasks = sorted(
            eligible_tasks,
            key=lambda task: (
                -task.effective_priority(owner.preferences),
                task.duration_minutes,
                task.title.lower(),
            ),
        )

        remaining_time = owner.availability_minutes
        selected_tasks: List[Task] = []
        for task in prioritized_tasks:
            if task.duration_minutes <= remaining_time:
                selected_tasks.append(task)
                remaining_time -= task.duration_minutes

        self.scheduled_tasks = selected_tasks

    def total_duration(self) -> int:
        """Return the total duration of all scheduled tasks."""
        return sum(task.duration_minutes for task in self.scheduled_tasks)

    def explain_decisions(self) -> str:
        """Return a plain-text explanation of scheduling decisions."""
        if self.owner is None:
            return "No owner has been assigned to this schedule."

        lines = [
            f"Schedule for {self.owner.name} on {self.date}",
            f"Availability: {self.owner.availability_minutes} minutes",
        ]
        if self.owner.preferences:
            lines.append(f"Preferences considered: {', '.join(self.owner.preferences)}")
        else:
            lines.append("Preferences considered: none")

        if self.scheduled_tasks:
            lines.append("Selected tasks:")
            for task in self.scheduled_tasks:
                reasons = [f"priority {task.priority}"]
                if task.recurring:
                    reasons.append("recurring")
                matched_preferences = [
                    preference
                    for preference in self.owner.preferences
                    if task.matches_preference(preference)
                ]
                if matched_preferences:
                    reasons.append(f"matches preference '{matched_preferences[0]}'")
                lines.append(
                    f"- {task.title} ({task.duration_minutes} min; {'; '.join(reasons)})"
                )
            lines.append(f"Total planned time: {self.total_duration()} minutes")
        else:
            lines.append("No tasks fit within the available time.")

        return "\n".join(lines)

    def sort_by_priority(self) -> None:
        """Sort scheduled tasks by descending priority, preferring preferred and recurring work."""
        self.scheduled_tasks.sort(
            key=lambda task: (
                -task.effective_priority(self.owner.preferences if self.owner else None),
                task.duration_minutes,
                task.title.lower(),
            )
        )

    def filter_by_availability(self, availability: int) -> None:
        """Filter tasks to fit within the provided availability."""
        if availability < 0:
            raise ValueError("Availability cannot be negative")

        total_time = 0
        kept_tasks: List[Task] = []

        for task in self.scheduled_tasks:
            if total_time + task.duration_minutes <= availability:
                kept_tasks.append(task)
                total_time += task.duration_minutes

        self.scheduled_tasks = kept_tasks
