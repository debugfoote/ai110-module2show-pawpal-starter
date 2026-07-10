import streamlit as st
from pawpal_system import Owner, Pet, Schedule, Task
import re

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps a pet owner turn care tasks into a practical daily plan.
This version connects the Streamlit UI to the scheduling backend so you can
enter pet details, add tasks, generate a schedule, and review any conflicts.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet-care planning assistant. It helps an owner plan care tasks
for one or more pets based on availability, priority, and timing.
"""
    )

st.divider()

# Ensure selection index exists before widgets so we can use it for defaults
if "selected_pet_index" not in st.session_state:
    st.session_state.selected_pet_index = 0

# Ensure owner/session exists before computing pet defaults
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", availability_minutes=120)

# If the owner has no pets yet, add a sensible default so the selector has options
if not st.session_state.owner.pets:
    st.session_state.owner.add_pet(Pet(name="Mochi", species="dog", age=0, breed="Unknown"))

# Normalize selected index
if st.session_state.selected_pet_index >= len(st.session_state.owner.pets):
    st.session_state.selected_pet_index = 0

# Pet selection and management (placed before the detail widgets so defaults update)
st.subheader("Pets")
pet_cols = st.columns([3, 1])
with pet_cols[0]:
    pet_names = [p.name for p in st.session_state.owner.pets]
    selected_name = st.selectbox("Select pet", pet_names, index=st.session_state.selected_pet_index, key="select_pet")
    st.session_state.selected_pet_index = pet_names.index(selected_name)
with pet_cols[1]:
    if st.button("Remove selected pet", key="remove_pet"):
        if len(st.session_state.owner.pets) > 1:
            removed = st.session_state.owner.pets.pop(st.session_state.selected_pet_index)
            st.success(f"Removed pet: {removed.name}")
            st.session_state.selected_pet_index = max(0, st.session_state.selected_pet_index - 1)
        else:
            st.warning("At least one pet must remain.")

with st.expander("Add new pet", expanded=False):
    new_pet_name = st.text_input("New pet name", value="", key="new_pet_name")
    new_pet_species = st.selectbox("Species", ["dog", "cat", "other"], index=0, key="new_pet_species")
    new_pet_age = st.number_input("Age", min_value=0, max_value=30, value=0, key="new_pet_age")
    new_pet_breed = st.text_input("Breed", value="Unknown", key="new_pet_breed")
    if st.button("Add pet", key="add_pet"):
        added = Pet(name=new_pet_name or "Unnamed", species=new_pet_species, age=int(new_pet_age), breed=new_pet_breed)
        st.session_state.owner.add_pet(added)
        st.session_state.selected_pet_index = len(st.session_state.owner.pets) - 1
        st.success(f"Added pet: {added.name}")

# Derive default pet values from the currently selected pet when available
if st.session_state.owner.pets:
    _default_pet = st.session_state.owner.pets[st.session_state.selected_pet_index]
    pet_name_default = _default_pet.name
    species_default = _default_pet.species
    age_default = _default_pet.age
    breed_default = _default_pet.breed
else:
    pet_name_default = "Mochi"
    species_default = "dog"
    age_default = 0
    breed_default = "Unknown"

st.subheader("Owner and pet details")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name or "Jordan", key="owner_name")
pet_name = st.text_input("Pet name", value=pet_name_default, key="pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], index=["dog","cat","other"].index(species_default if species_default in ["dog","cat","other"] else "dog"), key="pet_species")
age = st.number_input("Age", min_value=0, max_value=30, value=age_default, key="pet_age")
breed = st.text_input("Breed", value=breed_default, key="pet_breed")
availability_minutes = st.number_input(
    "Owner availability (minutes)", min_value=0, max_value=1440, value=st.session_state.owner.availability_minutes, step=5, key="availability_minutes"
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, availability_minutes=int(availability_minutes))

if "schedule" not in st.session_state:
    st.session_state.schedule = Schedule()

# Ensure the owner has at least one pet (use the inputs as a starter pet)
if not st.session_state.owner.pets:
    initial_pet = Pet(name=pet_name, species=species, age=int(age), breed=breed)
    st.session_state.owner.add_pet(initial_pet)

if "selected_pet_index" not in st.session_state:
    st.session_state.selected_pet_index = 0

# Keep owner info up to date
st.session_state.owner.name = owner_name
st.session_state.owner.update_availability(int(availability_minutes))

# Clamp selected index and expose the currently-selected pet as `current_pet`
if st.session_state.selected_pet_index >= len(st.session_state.owner.pets):
    st.session_state.selected_pet_index = 0

current_pet = st.session_state.owner.pets[st.session_state.selected_pet_index]
current_pet.update_info(name=pet_name, species=species, age=int(age), breed=breed)

st.caption("Update the profile, then add tasks below to build a plan.")

st.divider()


st.subheader("Add care tasks")
st.caption("Optional times help the scheduler detect overlaps and sort the plan by time.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    time_of_day = st.text_input("Time (HH:MM, optional)", value="", placeholder="08:00")

priority_map = {"low": 1, "medium": 2, "high": 3}


def is_valid_time(value: str | None) -> bool:
    if not value:
        return True
    if not isinstance(value, str):
        return False
    m = re.match(r"^(\d{1,2}):(\d{2})$", value)
    if not m:
        return False
    h = int(m.group(1))
    mm = int(m.group(2))
    return 0 <= h < 24 and 0 <= mm < 60

col5, col6 = st.columns([1, 3])
with col5:
    recurring = st.checkbox("Recurring task")
with col6:
    frequency = st.selectbox(
        "Recurrence",
        ["daily", "weekly"],
        index=0,
        disabled=not recurring,
    )

if st.button("Add task"):
    new_task = Task(
        title=task_title,
        duration_minutes=int(duration),
        priority=priority_map[priority_label],
        time_of_day=time_of_day.strip() or None,
        recurring=recurring,
        frequency=frequency if recurring else None,
    )
    # Validate input
    if not task_title.strip():
        st.warning("Task title cannot be empty.")
    elif not is_valid_time(new_task.time_of_day):
        st.warning("Invalid time format. Please use HH:MM (24-hour).")
    else:
        current_pet.add_task(new_task)
        st.success(f"Added task: {new_task.title} to {current_pet.name}")

if current_pet.tasks:
    st.write("Current tasks")
    st.table(
        [
            {
                "title": task.title,
                "duration_minutes": task.duration_minutes,
                "priority": task.priority,
                "time_of_day": task.time_of_day or "No set time",
                "recurring": task.recurring,
                "completed": task.completed,
            }
            for task in current_pet.tasks
        ]
    )

    # Task management controls: edit, delete, mark complete
    task_options = current_pet.tasks
    selected_task = st.selectbox(
        "Select a task",
        task_options,
        format_func=lambda task: f"{task.title} ({task.time_of_day or 'no time'}) - {'done' if task.completed else 'pending'}",
        key="manage_task_select",
    )

    manage_cols = st.columns([1, 1, 1])
    if manage_cols[0].button("Mark complete"):
        selected_task.mark_complete()
        st.success(f"Marked '{selected_task.title}' complete for {current_pet.name}.")

    if manage_cols[1].button("Delete task"):
        if current_pet.delete_task(selected_task):
            st.success(f"Deleted task '{selected_task.title}' from {current_pet.name}.")
        else:
            st.error("Could not delete task.")

    if manage_cols[2].button("Edit task"):
        with st.expander("Edit task", expanded=True):
            edit_title = st.text_input("Title", value=selected_task.title, key="edit_title")
            edit_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=selected_task.duration_minutes, key="edit_duration")
            edit_priority_label = st.selectbox("Priority", ["low", "medium", "high"], index={1:0,2:1,3:2}[selected_task.priority], key="edit_priority")
            edit_time = st.text_input("Time (HH:MM, optional)", value=selected_task.time_of_day or "", key="edit_time")
            edit_recurring = st.checkbox("Recurring task", value=selected_task.recurring, key="edit_recurring")
            edit_frequency = st.selectbox("Recurrence", ["daily", "weekly"], index=0 if selected_task.frequency=="daily" else 1 if selected_task.frequency=="weekly" else 0, disabled=not edit_recurring, key="edit_frequency")
            if st.button("Save changes", key="save_task_changes"):
                if not edit_title.strip():
                    st.warning("Task title cannot be empty.")
                elif not is_valid_time(edit_time.strip() or None):
                    st.warning("Invalid time format. Please use HH:MM (24-hour).")
                else:
                    selected_task.update_details(
                        title=edit_title.strip(),
                        duration_minutes=int(edit_duration),
                        priority={"low":1,"medium":2,"high":3}[edit_priority_label],
                        time_of_day=edit_time.strip() or None,
                        recurring=edit_recurring,
                        frequency=edit_frequency if edit_recurring else None,
                    )
                    st.success(f"Updated task '{selected_task.title}' for {current_pet.name}.")

    pending_tasks = [task for task in current_pet.tasks if not task.completed]
    if pending_tasks:
        selected_task_pending = st.selectbox(
            "Mark a pending task complete",
            pending_tasks,
            format_func=lambda task: f"{task.title} ({task.time_of_day or 'no time'})",
        )
        if st.button("Mark selected task complete"):
            current_pet.mark_task_complete(selected_task_pending)
            st.success(f"Marked '{selected_task_pending.title}' complete for {current_pet.name}.")
    else:
        st.info("All tasks are complete.")
else:
    st.info("No tasks yet. Add one above to begin planning.")

st.divider()

st.subheader("Build schedule")
st.caption("Generate a plan using the backend scheduler and review the result.")

if st.button("Generate schedule"):
    st.session_state.schedule.generate_schedule(
        st.session_state.owner,
        st.session_state.owner.get_all_tasks(),
    )
    st.session_state.schedule.sort_by_time()
    st.session_state.schedule.detect_time_conflicts()

    if st.session_state.schedule.scheduled_tasks:
        st.success("Schedule generated.")
        st.write("### Scheduled tasks")
        # Build a friendly table including pet and recurrence info
        rows = []
        for task in st.session_state.schedule.scheduled_tasks:
            pet_name = st.session_state.schedule._find_pet_name(task) or "(unknown)"
            rows.append(
                {
                    "title": task.title,
                    "pet": pet_name,
                    "time": task.time_of_day or "No set time",
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "recurring": task.recurring,
                    "frequency": task.frequency or "",
                }
            )

        st.table(rows)

        if st.session_state.schedule.time_conflict_warnings:
            st.warning("Potential scheduling conflicts detected:")
            for warning in st.session_state.schedule.time_conflict_warnings:
                st.write(f"• {warning}")
            st.caption("You can edit a task to change its time, or follow a suggested time above.")
        else:
            st.success("No time conflicts detected for the scheduled tasks.")

        st.markdown("### Why these tasks?")
        st.text(st.session_state.schedule.explain_decisions())
    else:
        st.warning("No tasks fit within the owner's available time.")
