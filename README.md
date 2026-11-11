# Student Study Planner

A practical, beginner-friendly Python command-line tool that helps students organize assignments, exams, revision, reading, and study sessions. It works offline and stores tasks locally on your computer.

> A planning aid—not a pressure machine. Use suggestions flexibly, plan breaks, and adjust workloads to fit your life.

## Features

- Add tasks with subject, category, due date, priority, and estimated time
- View tasks ordered by deadline and filter by subject
- Mark tasks complete or delete them
- Get an optional next-task suggestion
- See a weekly overview of open work, overdue tasks, tasks due this week, and completed tasks
- Export tasks to CSV for spreadsheets or backup
- Load sample tasks to explore the app; sample data is only added when your list is empty
- Save data locally in `tasks.json`; no account or internet connection is needed

## Requirements

- Python 3.8 or newer
- No third-party packages

## Run the app

```bash
git clone https://github.com/naimul404-lab/student-study-planner.git
cd student-study-planner
python main.py
```

On some systems, use `python3 main.py` instead.

Select **9** to load demo tasks into an empty planner. Choose **8** to export your tasks to `study_tasks.csv`. Both files are created locally and are not uploaded anywhere.

## Run tests

```bash
python -m unittest -v
```

## Data and privacy

Your planner data is saved in `tasks.json` in the directory where you run the program. CSV export creates `study_tasks.csv` there. Keep private details out of task titles and notes, and make your own backups if the data matters to you. The app does not send data to a server.

## Project structure

```text
student-study-planner/
├── main.py
├── study_planner.py
├── test_study_planner.py
├── README.md
├── docs/
│   ├── accessibility.md
│   └── sample-tasks.md
└── LICENSE
```

## Wellbeing and accessibility

The next-task suggestion is optional and is based on due date, priority, and estimated time. It is not a judgment or a rigid schedule. The tool encourages manageable planning and breaks. For inclusive-design goals, see [`docs/accessibility.md`](docs/accessibility.md).

## Contributing

Beginner-friendly contributions are welcome. You can improve documentation, add tests, report a usability issue, or suggest features. Please avoid posting sensitive personal information in public issues.

## License

MIT. See [LICENSE](LICENSE).
