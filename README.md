# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).

3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

***
Today's Schedule
Owner: Mekayla

Pet: Luna
Task: Morning walk
Duration: 30 minutes
Priority: 5

Pet: Luna
Task: Feeding
Duration: 15 minutes
Priority: 4

Pet: Bruno
Task: Playtime
Duration: 20 minutes
Priority: 3

Pet: Bruno
Task: Grooming
Duration: 10 minutes
Priority: 2



***

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```
Test Covers

The test suite verifies the core functionality of the PawPal+ app which includes:

*   Task scheduling based on owner availability
*   Sorting tasks in chronological order
*   Daily recurring task creation
*   Time conflict detection for duplicate task times
*   Task filtering and completion behavior


Sample test output:

```
# Paste your pytest output here
```
..........                       [100%]
11 passed in 0.03s

Confidence Level 5/5 - All 11 test passed successful. The test also covered the core functionality which includes sorting, recurrence, conflict detection, filtering etc.

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Schedule.sort_by_priority()`; `Schedule.sort_by_time()`; `Schedule.generate()` | Sorting used when generating and when explicitly re-ordering scheduled items. `generate()` applies a compound sort by priority, duration, and title to choose tasks that fit available time. |
| Filtering | `Owner.filter_tasks()`; `Owner.get_all_tasks()`; `Schedule.filter_by_availability()` | `Owner.filter_tasks()` and `get_all_tasks()` filter by pet name and completed status. `Schedule.filter_by_availability()` trims scheduled tasks so total duration fits the available minutes. |
| Conflict detection | `Schedule.detect_time_conflicts()` | Lightweight detection that parses `time_of_day` strings (HH:MM) and show warnings when two tasks have the same start time. Invalid time strings produce warnings rather than exceptions. |
| Recurring tasks | `Task.mark_complete()`; `Task.create_next_occurrence()`; `Pet.mark_task_complete()` | Recurring tasks (daily/weekly) produce the next occurrence when completed; `mark_complete()` returns the next `Task` which `Pet.mark_task_complete()` re-attaches to the pet. |




## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
