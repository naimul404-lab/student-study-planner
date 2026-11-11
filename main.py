from study_planner import StudyPlanner


def main() -> None:
    planner = StudyPlanner("tasks.json")

    while True:
        print("\nStudent Study Planner")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark as done")
        print("4. Delete task")
        print("5. Suggest next task")
        print("6. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            title = input("Task title: ").strip()
            subject = input("Subject: ").strip()
            due_date = input("Due date (YYYY-MM-DD): ").strip()
            priority = input("Priority [High/Normal/Low] (default: Normal): ").strip() or "Normal"
            estimated = input("Estimated minutes: ").strip() or "30"
            try:
                planner.add_task(title, subject, due_date, priority, int(estimated))
                print("Task added successfully.")
            except Exception as exc:
                print(f"Error: {exc}")

        elif choice == "2":
            tasks = planner.list_tasks(include_completed=False)
            if not tasks:
                print("No open tasks.")
                continue
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task.title} | {task.subject} | {task.due_date} | {task.priority} | {task.estimated_minutes} min")

        elif choice == "3":
            tasks = planner.list_tasks(include_completed=False)
            if not tasks:
                print("No tasks to complete.")
                continue
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task.title}")
            task_number = int(input("Select task number: "))
            planner.complete_task(task_number)
            print("Task marked as done.")

        elif choice == "4":
            tasks = planner.list_tasks(include_completed=True)
            if not tasks:
                print("No tasks to delete.")
                continue
            for i, task in enumerate(tasks, start=1):
                status = "Done" if task.done else "Open"
                print(f"{i}. {task.title} [{status}]")
            task_number = int(input("Select task number: "))
            planner.remove_task(task_number)
            print("Task deleted.")

        elif choice == "5":
            suggestion = planner.suggest_next_task()
            if suggestion:
                print(f"Suggested next task: {suggestion.title} ({suggestion.subject}) due {suggestion.due_date}")
            else:
                print("No tasks left. Great work!")

        elif choice == "6":
            print("Good luck with your study plan!")
            break

        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    main()
