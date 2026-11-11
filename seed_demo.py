import json
from pathlib import Path

from study_planner import StudyPlanner


DEFAULT_TASKS = [
    {
        "title": "Review Python basics",
        "subject": "Programming",
        "due_date": "2026-11-15",
        "priority": "High",
        "estimated_minutes": 45,
        "done": False,
    },
    {
        "title": "Complete first assignment",
        "subject": "Math",
        "due_date": "2026-11-18",
        "priority": "Normal",
        "estimated_minutes": 60,
        "done": False,
    },
]


def seed_demo_tasks(path: str = "tasks.json") -> None:
    file_path = Path(path)
    if file_path.exists():
        return

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(DEFAULT_TASKS, file, indent=2)


if __name__ == "__main__":
    seed_demo_tasks()
    planner = StudyPlanner("tasks.json")
    print("Demo tasks loaded.")
    print(planner.suggest_next_task())
