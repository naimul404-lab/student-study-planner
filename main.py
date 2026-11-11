from study_planner import CATEGORIES, PRIORITIES, StudyPlanner


def print_tasks(tasks) -> None:
    if not tasks:
        print("No tasks found.")
        return
    for number, task in enumerate(tasks, start=1):
        status = "Complete" if task.done else "Open"
        print(
            f"{number}. [{status}] {task.title} | {task.subject} | {task.category} | "
            f"Due {task.due_date} | {task.priority} | {task.estimated_minutes} min"
        )


def ask_task_number(prompt: str) -> int:
    try:
        return int(input(prompt).strip())
    except ValueError as exc:
        raise ValueError("Please enter a task number using digits.") from exc


def main() -> None:
    planner = StudyPlanner("tasks.json")
    menu = (
        "\nStudent Study Planner\n"
        "1. Add task\n"
        "2. View open tasks\n"
        "3. Filter tasks by subject\n"
        "4. Mark task complete\n"
        "5. Delete task\n"
        "6. Suggest a next task\n"
        "7. Weekly summary\n"
        "8. Export tasks to CSV\n"
        "9. Load demo tasks (only when your list is empty)\n"
        "0. Exit"
    )
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                title = input("Task title: ").strip()
                subject = input("Subject: ").strip()
                due_date = input("Due date (YYYY-MM-DD): ").strip()
                priority = input(f"Priority {list(PRIORITIES)} [Normal]: ").strip().title() or "Normal"
                category = input(f"Category {list(CATEGORIES)} [Other]: ").strip().title() or "Other"
                minutes = int(input("Estimated minutes [30]: ").strip() or "30")
                task = planner.add_task(title, subject, due_date, priority, minutes, category)
                print(f"Added '{task.title}'. Remember to plan breaks and keep your workload realistic.")
            elif choice == "2":
                print_tasks(planner.list_tasks())
            elif choice == "3":
                subject = input("Subject to show: ").strip()
                print_tasks(planner.list_tasks(subject=subject))
            elif choice == "4":
                tasks = planner.list_tasks()
                print_tasks(tasks)
                if tasks:
                    task = planner.complete_task(ask_task_number("Open task number to complete: "))
                    print(f"Marked '{task.title}' complete. Nice work!")
            elif choice == "5":
                tasks = planner.list_tasks(include_completed=True)
                print_tasks(tasks)
                if tasks:
                    task = planner.remove_task(ask_task_number("Task number to delete: "))
                    print(f"Deleted '{task.title}'.")
            elif choice == "6":
                task = planner.suggest_next_task()
                if task:
                    print(f"Suggested next step: {task.title} ({task.subject}), due {task.due_date}; estimated {task.estimated_minutes} minutes.")
                    print("This is only a suggestion—choose what fits your time and energy.")
                else:
                    print("No open tasks. Add one whenever you are ready.")
            elif choice == "7":
                summary = planner.weekly_summary()
                print(f"Week: {summary['week_start']} to {summary['week_end']}")
                print(f"Open tasks: {summary['open_count']} | Overdue: {summary['overdue_count']} | Completed this week: {summary['completed_count']}")
                print(f"Estimated time for tasks due this week: {summary['planned_minutes']} minutes")
                print("Tasks due this week:")
                print_tasks(summary["due_this_week"])
                print("Use this as a planning aid, not a measure of your worth. Adjust the plan to your needs.")
            elif choice == "8":
                path = planner.export_csv()
                print(f"Exported tasks to {path.resolve()}")
            elif choice == "9":
                count = planner.add_demo_tasks()
                if count:
                    print(f"Added {count} sample tasks. They are saved locally in tasks.json.")
                else:
                    print("Demo tasks were not added because your task list already has data; your tasks were kept safe.")
            elif choice == "0":
                print("Your tasks are saved locally. Take breaks and good luck with your studies!")
                break
            else:
                print("Choose one of the listed menu numbers.")
        except (ValueError, IndexError, OSError) as exc:
            print(f"Could not complete that action: {exc}")


if __name__ == "__main__":
    main()
