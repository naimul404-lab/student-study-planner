import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class Task:
    title: str
    subject: str
    due_date: str
    priority: str = "Normal"
    estimated_minutes: int = 30
    done: bool = False
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat(timespec="seconds")


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
        except json.JSONDecodeError:
            return []

        tasks = []
        for item in data:
            tasks.append(Task(**item))
        return tasks

    def save(self) -> None:
        with self.storage_path.open("w", encoding="utf-8") as file:
            json.dump([asdict(task) for task in self.tasks], file, indent=2)

    def add_task(
        self,
        title: str,
        subject: str,
        due_date: str,
        priority: str = "Normal",
        estimated_minutes: int = 30,
    ) -> Task:
        title = title.strip()
        subject = subject.strip()
        if not title or not subject or not due_date:
            raise ValueError("Title, subject, and due date are required.")

        task = Task(
            title=title,
            subject=subject,
            due_date=due_date,
            priority=priority,
            estimated_minutes=estimated_minutes,
        )
        self.tasks.append(task)
        self.save()
        return task

    def list_tasks(self, include_completed: bool = False) -> List[Task]:
        if include_completed:
            return self.tasks
        return [task for task in self.tasks if not task.done]

    def complete_task(self, task_number: int) -> Task:
        tasks = self.list_tasks(include_completed=True)
        if not 1 <= task_number <= len(tasks):
            raise IndexError("Task number is out of range.")

        task = tasks[task_number - 1]
        task.done = True
        self.save()
        return task

    def remove_task(self, task_number: int) -> Task:
        tasks = self.list_tasks(include_completed=True)
        if not 1 <= task_number <= len(tasks):
            raise IndexError("Task number is out of range.")

        task = tasks.pop(task_number - 1)
        self.tasks = tasks
        self.save()
        return task

    def suggest_next_task(self) -> Optional[Task]:
        tasks = [task for task in self.tasks if not task.done]
        if not tasks:
            return None

        def sort_key(task: Task):
            due_date_value = datetime.fromisoformat(task.due_date).date() if task.due_date else datetime.max.date()
            priority_value = {"High": 0, "Normal": 1, "Low": 2}.get(task.priority, 1)
            return (due_date_value, priority_value, task.estimated_minutes)

        return sorted(tasks, key=sort_key)[0]

    def overdue_tasks(self) -> List[Task]:
        today = datetime.utcnow().date()
        result = []
        for task in self.tasks:
            if task.done:
                continue
            try:
                due_date = datetime.fromisoformat(task.due_date).date()
            except ValueError:
                continue
            if due_date < today:
                result.append(task)
        return result

    def upcoming_tasks(self, days: int = 7) -> List[Task]:
        today = datetime.utcnow().date()
        limit = today.fromordinal(today.toordinal() + days)
        result = []
        for task in self.tasks:
            if task.done:
                continue
            try:
                due_date = datetime.fromisoformat(task.due_date).date()
            except ValueError:
                continue
            if today <= due_date <= limit:
                result.append(task)
        return result


def main() -> None:
    planner = StudyPlanner("tasks.json")

    while True:
        print("\nStudent Study Planner")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark task as done")
        print("4. Delete task")
        print("5. Suggest next task")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            subject = input("Subject: ").strip()
            due_date = input("Due date (YYYY-MM-DD): ").strip()
            priority = input("Priority [High/Normal/Low] (default: Normal): ").strip() or "Normal"
            minutes = input("Estimated minutes (default: 30): ").strip() or "30"
            try:
                task = planner.add_task(
                    title=title,
                    subject=subject,
                    due_date=due_date,
                    priority=priority,
                    estimated_minutes=int(minutes),
                )
                print(f"Added: {task.title} ({task.subject})")
            except ValueError as exc:
                print(f"Error: {exc}")
            except Exception as exc:
                print(f"Error: {exc}")

        elif choice == "2":
            tasks = planner.list_tasks(include_completed=False)
            if not tasks:
                print("No tasks yet.")
                continue
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task.title} | {task.subject} | Due: {task.due_date} | Priority: {task.priority} | {task.estimated_minutes} min")

        elif choice == "3":
            tasks = planner.list_tasks(include_completed=False)
            if not tasks:
                print("No tasks available to complete.")
                continue
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task.title}")
            try:
                number = int(input("Select a task number: "))
                task = planner.complete_task(number)
                print(f"Completed: {task.title}")
            except (ValueError, IndexError) as exc:
                print(f"Error: {exc}")

        elif choice == "4":
            tasks = planner.list_tasks(include_completed=True)
            if not tasks:
                print("No tasks to delete.")
                continue
            for i, task in enumerate(tasks, start=1):
                status = "Done" if task.done else "Open"
                print(f"{i}. {task.title} [{status}]")
            try:
                number = int(input("Select a task number: "))
                task = planner.remove_task(number)
                print(f"Deleted: {task.title}")
            except (ValueError, IndexError) as exc:
                print(f"Error: {exc}")

        elif choice == "5":
            suggestion = planner.suggest_next_task()
            if suggestion is None:
                print("No pending tasks. Great job!")
            else:
                print(f"Suggested next task: {suggestion.title} ({suggestion.subject}) due {suggestion.due_date}")

        elif choice == "6":
            print("Good luck with your study plan!")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
