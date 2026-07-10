from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    recurring: bool = False
    completed: bool = False
    time_of_day: str | None = None
    frequency: str | None = None
    due_date: date = field(default_factory=date.today)

    def mark_complete(self) -> "Task | None":
        """Mark the task as completed and create the next occurrence for daily/weekly tasks."""
        self.completed = True
        if self.recurring and self.frequency in {"daily", "weekly"}:
            return self.create_next_occurrence()
        return None

    def create_next_occurrence(self) -> "Task":
        """Create a fresh task for the next recurring occurrence using a new due date."""
        if self.frequency == "daily":
            next_due_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due_date = self.due_date + timedelta(days=7)
        else:
            next_due_date = self.due_date

        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            recurring=True,
            completed=False,
            time_of_day=self.time_of_day,
            frequency=self.frequency,
            due_date=next_due_date,
        )

    def update_duration(self, minutes: int) -> None:
        """Update the task duration."""
        if minutes <= 0:
            raise ValueError("Task duration must be positive")
        self.duration_minutes = minutes

    def update_details(
        self,
        title: str | None = None,
        duration_minutes: int | None = None,
        priority: int | None = None,
        time_of_day: str | None = None,
        recurring: bool | None = None,
        frequency: str | None = None,
    ) -> None:
        """Update multiple task fields at once."""
        if title is not None:
            self.title = title
        if duration_minutes is not None:
            if duration_minutes <= 0:
                raise ValueError("Task duration must be positive")
            self.duration_minutes = duration_minutes
        if priority is not None:
            self.priority = priority
        if time_of_day is not None:
            self.time_of_day = time_of_day
        if recurring is not None:
            self.recurring = recurring
        if frequency is not None:
            self.frequency = frequency

    def is_eligible(self) -> bool:
        """Return True when the task is still pending."""
        return not self.completed


@dataclass
class Pet:
    name: str
    species: str
    age: int
    breed: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to the pet."""
        self.tasks.append(task)

    def mark_task_complete(self, task: Task) -> "Task | None":
        """Complete a task and add the next recurring occurrence back to the pet."""
        next_task = task.mark_complete()
        if next_task is not None:
            self.add_task(next_task)
        return next_task

    def delete_task(self, task: Task) -> bool:
        """Remove a task from the pet. Returns True when removed."""
        try:
            self.tasks.remove(task)
            return True
        except ValueError:
            return False

    def get_pending_tasks(self) -> List[Task]:
        """Return only tasks that are still pending."""
        return [task for task in self.tasks if task.is_eligible()]

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
        if pref and pref not in self.preferences:
            self.preferences.append(pref)

    def update_availability(self, minutes: int) -> None:
        """Update the owner's available time in minutes."""
        if minutes < 0:
            raise ValueError("Availability cannot be negative")
        self.availability_minutes = minutes

    def filter_tasks(self, pet_name: str | None = None, include_completed: bool = False) -> List[Task]:
        """Return tasks filtered by pet name and completion status."""
        tasks: List[Task] = []
        for pet in self.pets:
            if pet_name is not None and pet.name != pet_name:
                continue
            for task in pet.tasks:
                if include_completed or task.is_eligible():
                    tasks.append(task)
        return tasks

    def get_all_tasks(self, pet_name: str | None = None, include_completed: bool = False) -> List[Task]:
        """Collect tasks from every pet owned by the owner."""
        return self.filter_tasks(pet_name=pet_name, include_completed=include_completed)


@dataclass
class Schedule:
    date: str = field(default_factory=lambda: date.today().isoformat())
    scheduled_tasks: List[Task] = field(default_factory=list)
    conflicts: List[Task] = field(default_factory=list)
    time_conflict_warnings: List[str] = field(default_factory=list)
    owner: Owner | None = None
    def generate_schedule(self, owner: Owner, tasks: List[Task]) -> None:
        """
        Generate a schedule for the given owner from a list of candidate tasks.

        Algorithm summary:
        - Filter out ineligible (completed) tasks.
        - Sort remaining tasks by a compound key that prefers higher priority,
          then shorter duration, then alphabetic title to make selection stable.
        - Greedily select tasks in that order while the owner's remaining
          availability (in minutes) can accommodate the task duration.

        The method sets `self.owner`, fills `self.scheduled_tasks` with the
        selected tasks, places any unselected tasks into `self.conflicts`, and
        populates `self.time_conflict_warnings` by calling
        `detect_time_conflicts` on the scheduled tasks.

        This is a fast, greedy scheduler that favors high-priority, short
        tasks. It does not perform backtracking or optimize for global
        throughput; those would require a different algorithm (e.g., knapSack
        or integer programming) when strict optimality is required.
        """
        self.owner = owner
        eligible_tasks = [task for task in tasks if task.is_eligible()]
        prioritized_tasks = sorted(
            eligible_tasks,
            key=lambda task: (
                -task.priority,
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
        self.conflicts = [task for task in prioritized_tasks if task not in selected_tasks]
        self.time_conflict_warnings = self.detect_time_conflicts(self.scheduled_tasks)

    def recommend_alternate_time(self, task: Task) -> str | None:
        """Recommend an alternate HH:MM time not used by scheduled tasks.

        Scans 30-minute slots between 06:00 and 21:30 and returns the first
        unused slot as an HH:MM string, or None when no reasonable slot is
        available.
        """
        used_times = set()
        for t in self.scheduled_tasks:
            if t.time_of_day:
                try:
                    # normalize to HH:MM
                    h, m = self._time_key(t.time_of_day)
                    used_times.add(f"{h:02d}:{m:02d}")
                except ValueError:
                    continue

        for hour in range(6, 22):
            for minute in (0, 30):
                slot = f"{hour:02d}:{minute:02d}"
                if slot not in used_times:
                    return slot
        return None

    generate = generate_schedule

    def explain_decisions(self) -> str:
        """Return a plain-text explanation of scheduling decisions."""
        lines: List[str] = [
            "Schedule generated based on owner availability, task priority, and preferences.",
            "Scheduled tasks:",
        ]
        for task in self.scheduled_tasks:
            pet_name = self._find_pet_name(task) or "(unknown pet)"
            recur = ""
            if task.recurring and task.frequency:
                recur = f" — repeats {task.frequency}"
            lines.append(f"- {task.title} ({pet_name}) at {task.time_of_day or 'No set time'}{recur}")

        return "\n".join(lines)

    def sort_by_priority(self) -> None:
        """Sort scheduled tasks by descending priority."""
        self.scheduled_tasks.sort(key=lambda task: task.priority, reverse=True)

    def detect_time_conflicts(self, tasks: List[Task] | None = None) -> List[str]:
        """
        Inspect scheduled tasks and return human-readable warnings for
        conflicting time slots.

        Behaviour:
        - If `tasks` is None, the method inspects `self.scheduled_tasks`.
        - Tasks without a `time_of_day` are ignored for conflict checks.
        - Time strings are parsed using `_time_key`; invalid formats produce
          a warning rather than raising, to remain robust in the face of bad
          input.
        - A lightweight equality-based conflict test is used: two tasks
          conflict when their parsed hour/minute tuples are equal. This
          intentionally checks exact-start collisions and does not detect
          overlapping intervals that start at different times.

        Returns a list of warning messages and updates
        `self.time_conflict_warnings` with the same list.
        """
        candidate_tasks = tasks if tasks is not None else self.scheduled_tasks
        warnings: List[str] = []

        for index, task in enumerate(candidate_tasks):
            if not task.time_of_day:
                continue

            try:
                current_time = self._time_key(task.time_of_day)
            except ValueError:
                warnings.append(f"Warning: {task.title} has an invalid time '{task.time_of_day}'.")
                continue

            for other in candidate_tasks[index + 1 :]:
                if not other.time_of_day:
                    continue
                try:
                    other_time = self._time_key(other.time_of_day)
                except ValueError:
                    warnings.append(f"Warning: {other.title} has an invalid time '{other.time_of_day}'.")
                    continue

                if current_time == other_time:
                    task_pet = self._find_pet_name(task)
                    other_pet = self._find_pet_name(other)
                    task_label = f"{task.title} ({task_pet})" if task_pet else task.title
                    other_label = f"{other.title} ({other_pet})" if other_pet else other.title
                    # Suggest moving the lower-priority task when possible
                    if task.priority >= other.priority:
                        to_suggest = other
                    else:
                        to_suggest = task

                    suggestion = self.recommend_alternate_time(to_suggest)
                    if suggestion:
                        warnings.append(
                            f"Warning: {task_label} and {other_label} overlap at {task.time_of_day}."
                        )
                        warnings.append(
                            f"Suggestion: Consider moving '{to_suggest.title}' to {suggestion}."
                        )
                    else:
                        warnings.append(
                            f"Warning: {task_label} and {other_label} overlap at {task.time_of_day}."
                        )

        self.time_conflict_warnings = warnings
        return warnings

    def _find_pet_name(self, task: Task) -> str | None:
        """
        Return the name of the pet that owns `task`, or None when not found.

        The lookup uses `self.owner.pets` and checks membership of the task in
        each pet's `tasks` list. If `self.owner` is None, the function returns
        None.
        """
        if self.owner is None:
            return None
        for pet in self.owner.pets:
            if task in pet.tasks:
                return pet.name
        return None

    def _time_key(self, time_value: str | None) -> tuple[int, int]:
        """
        Parse an HH:MM time string into a tuple (hour, minute) suitable for
        sorting and equality comparisons.

        Rules:
        - If `time_value` is `None`, return the sentinel (23, 59) which sorts
          last.
        - Expects a string in the exact `HH:MM` form; if parsing fails a
          `ValueError` is raised by the underlying conversions and is handled
          by callers (who convert parsing errors into warnings).

        Returns a tuple `(hour, minute)` of integers.
        """
        if time_value is None:
            return (23, 59)
        hours_str, minutes_str = time_value.split(":")
        hours, minutes = int(hours_str), int(minutes_str)
        if not (0 <= hours < 24 and 0 <= minutes < 60):
            raise ValueError("Invalid hour or minute range")
        return hours, minutes

    def sort_by_time(self) -> None:
        """
        Sort `self.scheduled_tasks` in-place by their `time_of_day` value.

        Tasks with `None` for `time_of_day` are treated as late-day items and
        will appear after explicit times because `_time_key(None)` returns
        `(23, 59)`.
        """
        self.scheduled_tasks.sort(key=lambda task: self._time_key(task.time_of_day))

    def filter_by_availability(self, availability: int) -> None:
        """
        Trim `self.scheduled_tasks` so that the cumulative duration does not
        exceed `availability` minutes.

        The method iterates tasks in their current order and keeps each task
        if adding it does not push the cumulative duration past `availability`.
        This preserves any ordering (priority/time) chosen earlier.
        """
        if availability < 0:
            raise ValueError("Availability cannot be negative")

        total_time = 0
        kept_tasks: List[Task] = []

        for task in self.scheduled_tasks:
            if total_time + task.duration_minutes <= availability:
                kept_tasks.append(task)
                total_time += task.duration_minutes

        self.scheduled_tasks = kept_tasks
