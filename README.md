# Q2
A better help queue for CS classes

## Overview

### Project Description
This will be a new help queue to replace the ones that many CS classes currently use (142, 235, 236, 240).
The current help queue mostly works, but there are some bugs with it, such as innacurate statistics being presented, major clock skew on the server, and unreliable chat. There are also some pretty serious security concerns (details not shared here for obvious reasons).
Also, the codebase is pretty ugly. It is in php. It is barely maintainable. And not easily extensible at all.

We will make Q2 better.

Many features will be the same, especially the basic functionality of allowing students to join a queue and TAs selecting to help them. However, with a new product we can improve on some features, possible add more, and possibly scale down a bit (at least for the class portion of the project).

### Team
I'm looking for at least two additional group members, and would be open to more if enough people want to commit to the project.

I would especially like:
- somebody who is knowledgable in setting up a server from scratch, or would like to learn how to do so, as our hope is to have a dedicated server in the Talmage Building (some discussion with the sysadmins has already been happening).
- anybody who TAs for a CS class that would want to use Q2. If no such person is able to join the team directly, we will still try to consult with TAs from other courses.

### Implementation
We'll use a traditional client-server model, with all business logic and security checks on the server side. For the server, I have an inkling to use Rust as our implementation language, but could be convinced to use Node or other popular frameworks.

### SQL
I'm most familiar with sqlite, but would be open to other relational databases.

### No-SQL
I'm open to different ideas, but I lean to a key-value NoSQL database for the NoSQL portion of the project.

## BOLTS

### Business
This will be an internal tool for the purposes of the CS department. As such, no fees will be charged for use. The only major business aspect to this project will be coordinating with CS courses and the department.

### Operation
As a group we will create at least a minimum viable product of the queue, and be primary developers and maintainers of the product for at least this semester. Beyond this semester, I will remain maintining Q2, but will be able to give control to additional TAs, and when I do eventually graduate \[:(], pass on control to future employees of the CS department.

### Legal
This will be an open-source project used by the BYU CS department.

### Technical
There are a few major components of the project, and with the ideal team, each member will be able to focus on the portions they would like to, and consult on the other portions:
- Coordination with CS courses/department
- API design
- Building a front-end - ideally mobile-friendly
- Server setup
- Server-side backend database management
- Server-side business logic management

### Social
'Customers' will be CS students. I feel no need to be cutesy with the project and try to be social in the traditional sense, but we will strive for a clean interface and reliable service so that students and TAs can have a hassle-free experience in the help queue.
