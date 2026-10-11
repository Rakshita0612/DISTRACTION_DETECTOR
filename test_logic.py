"""
Unit tests for Distraction Detector logic
Verifying formulas, validations, categories, and data storage.
"""

import unittest
import pandas as pd
from focus_calculator import (
    validate_session_inputs,
    calculate_focus_metrics,
    get_recommendations,
    CATEGORY_CONFIG
)
import data_manager


class TestFocusCalculator(unittest.TestCase):

    def test_specified_example(self):
        """
        Test user request specification:
        - Subject: Python
        - Total study time: 60 minutes
        - Distraction time: 15 minutes
        - Main distraction: Mobile Phone
        Expected:
        - Focused time: 45 minutes
        - Focus score: 75%
        - Category: Good Focus
        """
        valid, msg = validate_session_inputs(60.0, 15.0, "Python")
        self.assertTrue(valid)
        self.assertEqual(msg, "")

        metrics = calculate_focus_metrics(60.0, 15.0)
        self.assertEqual(metrics["focused_time"], 45.0)
        self.assertEqual(metrics["focus_score"], 75.0)
        self.assertEqual(metrics["category"], "Good Focus")

        recs = get_recommendations("Mobile Phone", metrics["focus_score"])
        self.assertGreater(len(recs), 0)
        # Check that physical distance or mobile advice is present
        titles = [r["title"] for r in recs]
        self.assertTrue(any("Mobile" in t or "Phone" in t or "Distance" in t for t in titles))

    def test_validation_zero_study_time(self):
        """Zero study duration must be rejected."""
        valid, msg = validate_session_inputs(0, 0, "Python")
        self.assertFalse(valid)
        self.assertIn("greater than 0", msg)

    def test_validation_negative_study_time(self):
        """Negative study duration must be rejected."""
        valid, msg = validate_session_inputs(-10, 0, "Python")
        self.assertFalse(valid)
        self.assertIn("greater than 0", msg)

    def test_validation_negative_distraction_time(self):
        """Negative distraction duration must be rejected."""
        valid, msg = validate_session_inputs(60, -5, "Python")
        self.assertFalse(valid)
        self.assertIn("cannot be negative", msg)

    def test_validation_distraction_exceeds_study(self):
        """Distraction exceeding total study time must be rejected."""
        valid, msg = validate_session_inputs(60, 75, "Python")
        self.assertFalse(valid)
        self.assertIn("cannot exceed", msg)

    def test_validation_empty_subject(self):
        """Empty subject must be rejected."""
        valid, msg = validate_session_inputs(60, 10, "")
        self.assertFalse(valid)
        self.assertIn("Subject is required", msg)

        valid_whitespace, _ = validate_session_inputs(60, 10, "   ")
        self.assertFalse(valid_whitespace)

    def test_category_boundaries(self):
        """Test exact category boundaries: 80+, 60-79.9, 40-59.9, <40."""
        # 100% -> Excellent
        m100 = calculate_focus_metrics(100, 0)
        self.assertEqual(m100["focus_score"], 100.0)
        self.assertEqual(m100["category"], "Excellent Focus")

        # 80% -> Excellent
        m80 = calculate_focus_metrics(100, 20)
        self.assertEqual(m80["focus_score"], 80.0)
        self.assertEqual(m80["category"], "Excellent Focus")

        # 79.9% -> Good
        m79 = calculate_focus_metrics(100, 20.1)
        self.assertAlmostEqual(m79["focus_score"], 79.9, places=1)
        self.assertEqual(m79["category"], "Good Focus")

        # 60% -> Good
        m60 = calculate_focus_metrics(100, 40)
        self.assertEqual(m60["focus_score"], 60.0)
        self.assertEqual(m60["category"], "Good Focus")

        # 59.9% -> Needs Improvement
        m59 = calculate_focus_metrics(100, 40.1)
        self.assertEqual(m59["category"], "Needs Improvement")

        # 40% -> Needs Improvement
        m40 = calculate_focus_metrics(100, 60)
        self.assertEqual(m40["focus_score"], 40.0)
        self.assertEqual(m40["category"], "Needs Improvement")

        # 39.9% -> High Distraction
        m39 = calculate_focus_metrics(100, 60.1)
        self.assertEqual(m39["category"], "High Distraction")

        # 0% -> High Distraction
        m0 = calculate_focus_metrics(100, 100)
        self.assertEqual(m0["focus_score"], 0.0)
        self.assertEqual(m0["category"], "High Distraction")

    def test_data_manager_empty_and_save(self):
        """Test loading and saving in data manager."""
        empty_df = data_manager.get_empty_dataframe()
        self.assertTrue(empty_df.empty)
        for col in data_manager.COLUMNS:
            self.assertIn(col, empty_df.columns)

        # Test demo data loader
        demo_df = data_manager.load_demo_data()
        self.assertGreater(len(demo_df), 0)
        self.assertTrue(all(demo_df["is_demo"]))

        # Test clear
        data_manager.clear_sessions()
        cleared_df = data_manager.load_sessions()
        self.assertTrue(cleared_df.empty)


if __name__ == "__main__":
    unittest.main()
