import unittest

from study_planner import StudyPlanner


class StudyPlannerTests(unittest.TestCase):
    def setUp(self):
        self.planner = StudyPlanner("test_tasks.json")
        self.planner.tasks = []
        self.planner.save()

    def tearDown(self):
        import os
        if os.path.exists("test_tasks.json"):
            os.remove("test_tasks.json")

    def test_add_task(self):
        task = self.planner.add_task("Read chapter 1", "Biology", "2026-11-15", "High", 30)
        self.assertEqual(len(self.planner.tasks), 1)
        self.assertEqual(task.title, "Read chapter 1")

    def test_complete_task(self):
        self.planner.add_task("Solve math quiz", "Math", "2026-11-12", "Normal", 40)
        task = self.planner.complete_task(1)
        self.assertTrue(task.done)

    def test_suggest_next_task_prioritizes_high_priority_and_earliest_due(self):
        self.planner.add_task("Finish essay", "History", "2026-11-20", "Normal", 60)
        self.planner.add_task("Prepare for quiz", "Science", "2026-11-14", "High", 30)
        suggestion = self.planner.suggest_next_task()
        self.assertEqual(suggestion.title, "Prepare for quiz")


if __name__ == "__main__":
    unittest.main()
