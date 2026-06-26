from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    recurring: bool = False
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def update_duration(self, minutes: int) -> None:
        """Update the task duration."""
        self.duration_minutes = minutes


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def update_info(self, name: str | None = None, species: str | None = None, age: int | None = None, breed: str | None = None) -> None:
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
    name: str
    availability_minutes: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's collection."""
        self.pets.append(pet)

    def set_preference(self, pref: str) -> None:
        """Add a new owner preference."""
        if pref not in self.preferences:
            self.preferences.append(pref)

    def update_availability(self, minutes: int) -> None:
        """Update the owner's available time in minutes."""
        self.availability_minutes = minutes


@dataclass
class Schedule:
    date: str = field(default_factory=lambda: date.today().isoformat())
    scheduled_tasks: List[Task] = field(default_factory=list)
    owner: Owner | None = None

    def generate_schedule(self, owner: Owner, tasks: List[Task]) -> None:
        """Generate a schedule from an owner and a list of tasks."""
        self.owner = owner
        self.scheduled_tasks = list(tasks)

    def explain_decisions(self) -> str:
        """Return a plain-text explanation of scheduling decisions."""
        return "Schedule generated based on owner availability, task priority, and preferences."

    def sort_by_priority(self) -> None:
        """Sort scheduled tasks by descending priority."""
        self.scheduled_tasks.sort(key=lambda task: task.priority, reverse=True)

    def filter_by_availability(self, availability: int) -> None:
        """Filter tasks to fit within the provided availability."""
        total_time = 0
        kept_tasks: List[Task] = []

        for task in self.scheduled_tasks:
            if total_time + task.duration_minutes <= availability:
                kept_tasks.append(task)
                total_time += task.duration_minutes

        self.scheduled_tasks = kept_tasks
