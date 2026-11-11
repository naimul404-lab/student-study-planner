import csv
import json
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Optional


PRIORITIES = ("High", "Normal", "Low")
CATEGORIES = ("Assignment", "Exam", "Revision", "Reading", "Other")


@dataclass
class Task:
    title: str
    subject: str
    due_date: str
    priority: str = "Normal"
    estimated_minutes: int = 30
    done: bool = False
    created_at: str = ""
    category: str = "Other"
    completed_at: str = ""

    def __post_init__(self) -> None:
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")


class StudyPlanner:
    def __init__(self, storage_path: str = "tasks.json"):
        self.storage_path = Path(storage_path)
        self.tasks: List[Task] = self._load_tasks()

    def _load_tasks(self) -> List[Task]:
        if not self.storage_path.exists():
            return []
        try:
            with self.storage_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, list):
                raise ValueError("Task data must be a JSON list.")
            return [Task(**item) for item in data]
        except (json.JSONDecodeError, TypeError, KeyError) as exc:
            raise ValueError(f"Could not read task data in {self.storage_path}: {exc}") from exc

    def save(self) -> None:
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump([asdict(task) for task in self.tasks], file, indent=2)

    def add_task(
        self,
        title: str,
        subject: str,
        due_date: str,
        priority: str = "Normal",
        estimated_minutes: int = 30,
        category: str = "Other",
    ) -> Task:
        title, subject = title.strip(), subject.strip()
        if not title or not subject:
            raise ValueError("Title and subject are required.")
        try:
            date.fromisoformat(due_date)
        except (TypeError, ValueError) as exc:
            raise ValueError("Due date must be a real date in YYYY-MM-DD format.") from exc
        if priority not in PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(PRIORITIES)}.")
        if category not in CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}.")
        if isinstance(estimated_minutes, bool) or estimated_minutes <= 0:
            raise ValueError("Estimated study time must be a positive number of minutes.")

        task = Task(title, subject, due_date, priority, estimated_minutes, category=category)
        self.tasks.append(task)
        self.save()
        return task

    def list_tasks(self, include_completed: bool = False, subject: Optional[str] = None) -> List[Task]:
        tasks = [task for task in self.tasks if include_completed or not task.done]
        if subject:
            tasks = [task for task in tasks if task.subject.casefold() == subject.strip().casefold()]
        return sorted(tasks, key=lambda task: (task.due_date, PRIORITIES.index(task.priority) if task.priority in PRIORITIES else 1, task.title.casefold()))

    def complete_task(self, task_number: int) -> Task:
        tasks = self.list_tasks()
        if not 1 <= task_number <= len(tasks):
            raise IndexError("Open task number is out of range.")
        task = tasks[task_number - 1]
        task.done = True
        task.completed_at = datetime.now().isoformat(timespec="seconds")
        self.save()
        return task

    def remove_task(self, task_number: int) -> Task:
        tasks = self.list_tasks(include_completed=True)
        if not 1 <= task_number <= len(tasks):
            raise IndexError("Task number is out of range.")
        task = tasks[task_number - 1]
        self.tasks.remove(task)
        self.save()
        return task

    def suggest_next_task(self) -> Optional[Task]:
        tasks = self.list_tasks()
        if not tasks:
            return None
        today = date.today()

        def sort_key(task: Task):
            due = date.fromisoformat(task.due_date)
            overdue_rank = 0 if due < today else 1
            return (overdue_rank, due, PRIORITIES.index(task.priority) if task.priority in PRIORITIES else 1, task.estimated_minutes)

        return min(tasks, key=sort_key)

    def overdue_tasks(self) -> List[Task]:
        today = date.today()
        return [task for task in self.list_tasks() if date.fromisoformat(task.due_date) < today]

    def upcoming_tasks(self, days: int = 7) -> List[Task]:
        if days < 0:
            raise ValueError("Number of days cannot be negative.")
        today = date.today()
        limit = today + timedelta(days=days)
        return [task for task in self.list_tasks() if today <= date.fromisoformat(task.due_date) <= limit]

    def weekly_summary(self) -> dict:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        open_tasks = self.list_tasks()
        completed_this_week = []
        for task in self.tasks:
            if task.done and task.completed_at:
                try:
                    completed_day = datetime.fromisoformat(task.completed_at).date()
                except ValueError:
                    continue
                if week_start <= completed_day <= week_end:
                    completed_this_week.append(task)
        due_this_week = [task for task in open_tasks if week_start <= date.fromisoformat(task.due_date) <= week_end]
        return {
            "week_start": week_start,
            "week_end": week_end,
            "open_count": len(open_tasks),
            "overdue_count": len(self.overdue_tasks()),
            "due_this_week": due_this_week,
            "completed_count": len(completed_this_week),
            "planned_minutes": sum(task.estimated_minutes for task in due_this_week),
        }

    def export_csv(self, output_path: str = "study_tasks.csv") -> Path:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fields = ["title", "subject", "category", "due_date", "priority", "estimated_minutes", "done", "created_at", "completed_at"]
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for task in self.list_tasks(include_completed=True):
                writer.writerow(asdict(task))
        return path

    def add_demo_tasks(self) -> int:
        if self.tasks:
            return 0
        examples = [
            ("Review lecture notes", "Biology", 2, "Normal", 25, "Revision"),
            ("Practice algebra problems", "Mathematics", 4, "High", 40, "Assignment"),
            ("Read assigned pages", "History", 6, "Low", 30, "Reading"),
        ]
        for title, subject, days, priority, minutes, category in examples:
            due = (date.today() + timedelta(days=days)).isoformat()
            self.add_task(title, subject, due, priority, minutes, category)
        return len(examples)
