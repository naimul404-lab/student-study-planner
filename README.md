# Student Study Planner

A practical Python tool to help students manage assignments, deadlines, and study sessions in a simple, offline workflow.

## Why this project is useful

This project helps students by making study planning easier and less stressful. Instead of keeping tasks in scattered notes or messages, they can keep everything in one place and focus on what matters next.

## Features

- Add study tasks with a subject and due date
- Set task priority and estimated study time
- View all open tasks
- Mark tasks as complete
- Delete tasks you no longer need
- Get a suggested next task based on due date and priority
- Save tasks to a local JSON file so data stays on the user's machine

## Quick start

```bash
python main.py
```

## Example usage

1. Run the app.
2. Select "Add task".
3. Enter a title, subject, due date, priority, and estimated minutes.
4. Choose "View tasks" to see your plan.
5. Use "Suggest next task" to get a quick recommendation.

## Project structure

```text
student-study-planner/
├── main.py
├── study_planner.py
├── seed_demo.py
├── test_study_planner.py
├── tasks.json
├── README.md
├── docs/
│   ├── accessibility.md
│   └── sample-tasks.md
└── LICENSE
```

## Beginner-friendly design

The app is intentionally small and easy to understand so students can learn from the code as they build with it.

## Future improvements

- add task categories like exam, assignment, reading, revision
- filter by subject or priority
- add weekly study summaries
- export tasks as CSV
- build a simple web version

## Contributing

This project is open to beginner-friendly improvements, documentation updates, and new features that make the planner more helpful for students.
