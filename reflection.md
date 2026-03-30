# PawPal+ Project Reflection

## 1. System Design
  THe app is required to keep track of:
    1. pet care tasks
    2. The schedule of the pet owner
    3. Pets added
    The Core actions of the user must be to
    1. Add a pet
    2. Create/Edit a Task
    3. View the Daily Plan 
    Attributes:
1. The pets themselves
    1. Their name
    2. And personal_pet_id
    3. What kind of animal
2. The owner themself (their schedule)
3. Tasks
    1. What the task is about
    2. THe nature of said task.
    3. Duration of the task
    4. The Priority of the task
    5. Which pet is the task connected to (using their id)
Methods:
1. Method to create a daily task
Objects needed:
Pet Object:
- Name of pet
- ID of pet

Owner:
- Must have some way to list an owners schedule
- Their Pets

Task:
1. Name of Task
2. Duration of Task
3. Priority of Task
4. Pets its related to
5. whether or not the owner prefers doing it (rating: 1-10)

Daily_Plan:
1. Lists all tasks for the day
2. Its explaination
End of objects to list
**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
  The intial UML design contains the following Objects:
  1. Owner
  2. DailyPlan
  3. Task
  4. Pet
  5. TimeSlot
  The Daily PLan keeps secheduled task within itself. The Owner has a list of timeslots available to add tasks, as well as a list of unscheduled tasks. TimeSlot object is there as a way to implement what times are available to add tasks to. Pet is also there for each pet added to the app.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
 It didnt change much of the current implementation. It was recommending changes which would be needed if the app had multiple users. It wanted me to put changes I didn't believe is warrented for this project. FOr the TimeSlot, I added a _postinit_ validation which it recommended to verify that the input given is correct (start is before end time) to avoid a logic error. Also it askks me to add another valition to the method "edit_task" in the Task object to be able to edit created tasks.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff it made is with my detect_conflicst implementation, where the while loop it gave me cause it to check multiple time, with a O(n^2). ITs recommendation lowers it to O(n). However, the new implementation makes more mistakes. missing non-adjacent overlaps.
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
