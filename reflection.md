# PawPal+ Project Reflection

## 1. System Design
a. Initial design

Briefly describe your initial UML design.
What classes did you include, and what responsibilities did you assign to each?

b. Design changes

Did your design change during implementation?
If yes, describe at least one change and why you made it.


Core Actions:

1. user should be able to add and manage pet care tasks
2. Enter pet and owner information
3. Generate and view the pet care tasks based on priority, time availablility, preference

Brainstorm 
Classes:
Owner
Attributes: owner_name, availbility,
Methods: add_pet, set_preference, update_preference
Pet
Attributes: pet_name, species, age, breed, pet_needs
Methods: add_pet_needs(), update_pet_needs, 
Task
Attributes: title, duration, priority,task_details, recurring
Schedule
Methods: mark_complete(), update_duration, uodate_priority


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?


One tradeoff in my scheduler is that the conflict detection algorithm only checks whether two tasks have the exact same scheduled start time. This approach keeps the algorithm simple, and easy to understand, but it however does not detect overlapping tasks with different start times. For example, a task from 9:00–9:30 and another from 9:15–9:45. A more advanced scheduler could use each task's duration to calculate start and end times and detect all overlapping appointments.



---

## 3. AI Collaboration

**a. How you used AI**

- I used AI as a programming partner for debugging, refactoring the code, and improving the Streamlit UI. AI helped me identify and fix issues in widget state management, pet selection logic, and schedule conflict handling.
- The most helpful prompts were specific debugging requests like “why does the pet dropdown only show one pet?” and “how can I validate HH:MM task times in Streamlit?”. I also asked for refactor like suggestions, such as “add task edit/delete support” and “improve conflict warning messages”.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not accept an AI suggestion was when it suggested changing the pet selection logic in a way that would have overwritten widget state after Streamlit had already created the widgets. I knew that approach could cause  errors specifically runtime, so I did not implement it right away.
- I evaluated the suggestion by checking the Streamlit behavior and verifying it against the actual error message. I also tested the app after making a smaller change that kept the widget state stable, and I confirmed the fix by running the app and the test suite.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion behavior, recurring task creation, time-based sorting, conflict detection, pet/task filtering, and multi-pet scheduling. I also tested the new UI behaviors for invalid time input, task editing, task deletion, and adding multiple pets.

These tests were important because they confirm that the scheduler makes sensible decisions under realistic conditions and that the app handles common user mistakes without crashing.

**b. Confidence**

I am not fully confident yet because a few issues remain around the multi-pet experience, and I would want to refine that functionality so it feels more seamless before calling it fully complete.However I am fairly confident that the scheduler works correctly for the core use cases in this project because the main behaviors are covered by automated tests and I verified the app by running the app and the test suite.
If I had more time, I would test edge cases such as overlapping tasks with different durations, very tight availability limits, invalid or malformed time strings, and more complex recurring schedules, multipet functionality.

---

## 5. Reflection

**a. What went well**

I am pretty satisfied with how the app evolved from a simple idea into a working system that can manage owner information, multiple pets, tasks, and a basic schedule. I also feel proud that I was able to improve the user experience by adding validation, conflict handling, and task management features.

**b. What you would improve**

If I had another iteration, I would improve the multi-pet experience so it feels more seamless, refine the scheduler to better detect overlapping tasks with different durations, and make the UI more user friendly and production ready.

**c. Key takeaway**

 One important thing I learned is that good system design requires separating core logic from the user interface so the app is easier to test, debug, and improve. I also learned that AI is most effective when paired with careful verification and real-world testing. Also not to trust AI recommedation for everything. Take the time that is needed to go throught the changes because AI can simplify or complicate logic.
