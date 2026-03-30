import streamlit as st
from datetime import time
from pawpal_system import Scheduler, Owner, Pet, Task, TimeSlot
st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    pet = Pet(name=pet_name, personal_pet_id=f"{pet_name}-01", species=species)
    st.session_state.owner.add_pet(pet)
    st.success(f"Added {pet_name} ({species})")

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table([{"Name": p.name, "Species": p.species, "Tasks": p.task_count} for p in st.session_state.owner.pets])

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    if not st.session_state.owner.pets:
        st.error("Add a pet first before adding tasks.")
    else:
        priority_map = {"low": 3, "medium": 5, "high": 8}
        task = Task(
            name=task_title,
            description=task_title,
            duration=int(duration),
            priority=priority_map[priority],
            preference_rating=5,
        )
        st.session_state.owner.pets[-1].add_task(task)
        st.success(f"Added '{task_title}' to {st.session_state.owner.pets[-1].name}")

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table([{"Task": t.name, "Duration": t.duration, "Priority": t.priority} for t in all_tasks])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Set your availability and click generate to build a daily plan.")

avail_col1, avail_col2 = st.columns(2)
with avail_col1:
    avail_start = st.time_input("Available from", value=time(8, 0))
with avail_col2:
    avail_end = st.time_input("Available until", value=time(18, 0))

if st.button("Generate schedule"):
    if not st.session_state.owner.pets:
        st.error("Add a pet first.")
    elif not st.session_state.owner.get_all_tasks():
        st.error("Add at least one task first.")
    elif avail_start >= avail_end:
        st.error("End time must be after start time.")
    else:
        st.session_state.owner.availability = [TimeSlot(avail_start, avail_end)]
        scheduler = Scheduler(st.session_state.owner)
        plan = scheduler.generate_plan()
        st.markdown(f"**Plan for {plan.date}**")
        if plan.tasks:
            st.table([
                {"Task": t.name, "Duration (min)": t.duration, "Priority": t.priority}
                for t in plan.tasks
            ])
        else:
            st.warning("No tasks could fit in the available time.")
        st.info(plan.explanation)
