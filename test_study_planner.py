import csv
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from study_planner import StudyPlanner


class StudyPlannerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.planner = StudyPlanner(str(self.root / "tasks.json"))

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_and_reload_task(self):
        task = self.planner.add_task("Read chapter 1", "Biology", (date.today() + timedelta(days=2)).isoformat(), "High", 30, "Revision")
        reloaded = StudyPlanner(str(self.root / "tasks.json"))
        self.assertEqual(reloaded.tasks[0].title, task.title)
        self.assertEqual(reloaded.tasks[0].category, "Revision")

    def test_rejects_invalid_date_and_time(self):
        with self.assertRaises(ValueError):
            self.planner.add_task("Read", "Biology", "not-a-date")
        with self.assertRaises(ValueError):
            self.planner.add_task("Read", "Biology", date.today().isoformat(), estimated_minutes=0)

    def test_complete_and_filter_by_subject(self):
        due = (date.today() + timedelta(days=1)).isoformat()
        self.planner.add_task("Read chapter", "Biology", due)
        self.planner.add_task("Solve problems", "Math", due)
        self.assertEqual(len(self.planner.list_tasks(subject="biology")), 1)
        task = self.planner.complete_task(1)
        self.assertTrue(task.done)
        self.assertEqual(len(self.planner.list_tasks()), 1)

    def test_weekly_summary_counts_due_tasks(self):
        due = (date.today() + timedelta(days=1)).isoformat()
        self.planner.add_task("Study", "Science", due, estimated_minutes=35)
        summary = self.planner.weekly_summary()
        self.assertEqual(summary["open_count"], 1)
        self.assertEqual(summary["planned_minutes"], 35)

    def test_csv_export_contains_tasks(self):
        due = (date.today() + timedelta(days=3)).isoformat()
        self.planner.add_task("Essay", "English", due)
        output = self.planner.export_csv(str(self.root / "export.csv"))
        with output.open(newline="", encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        self.assertEqual(rows[0]["title"], "Essay")

    def test_demo_tasks_do_not_overwrite_existing_tasks(self):
        due = (date.today() + timedelta(days=1)).isoformat()
        self.planner.add_task("My task", "Math", due)
        self.assertEqual(self.planner.add_demo_tasks(), 0)
        self.assertEqual(len(self.planner.tasks), 1)


if __name__ == "__main__":
    unittest.main()
