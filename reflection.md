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

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
