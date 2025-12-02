# Unit Tests
import unittest
from school import School
from obesity_analysis import calculate_county_statistics, analyze_economic_disparity


class TestSchoolObesityAnalysis(unittest.TestCase):

    def test_school_initialization(self):
        school = School("Test School", 35.5, 45.0, 100, 2019)
        self.assertEqual(school.school_name, "Test School")
        self.assertEqual(school.obesity_rate, 35.5)
        self.assertEqual(school.economic_disadvantage_rate, 45.0)
        self.assertEqual(school.students_tested, 100)
        self.assertEqual(school.year, 2019)

    def test_calculate_obese_students(self):
        school = School("Test School", 40.0, 50.0, 100, 2019)
        self.assertEqual(school.calculate_obese_students(), 40)

        school2 = School("Test School 2", 25.0, 30.0, 80, 2019)
        self.assertEqual(school2.calculate_obese_students(), 20)

    def test_get_risk_category(self):
        # Test low risk
        school_low = School("Low School", 25.0, 30.0, 100, 2019)
        self.assertEqual(school_low.get_risk_category(), "Low")

        # Test moderate risk
        school_moderate = School("Moderate School", 32.0, 40.0, 100, 2019)
        self.assertEqual(school_moderate.get_risk_category(), "Moderate")

        # Test high risk
        school_high = School("High School", 38.0, 60.0, 100, 2019)
        self.assertEqual(school_high.get_risk_category(), "High")

        # Test critical risk
        school_critical = School("Critical School", 45.0, 70.0, 100, 2019)
        self.assertEqual(school_critical.get_risk_category(), "Critical")

    def test_is_economically_disadvantaged_school(self):
        school_disadvantaged = School("Disadvantaged", 35.0, 55.0, 100, 2019)
        self.assertTrue(school_disadvantaged.is_economically_disadvantaged_school())

        school_not_disadvantaged = School("Not Disadvantaged", 35.0, 45.0, 100, 2019)
        self.assertFalse(school_not_disadvantaged.is_economically_disadvantaged_school())

    def test_compare_to_county_average(self):
        school = School("Test School", 40.0, 50.0, 100, 2019)
        comparison = school.compare_to_county_average(35.0)
        self.assertIn("above", comparison)

    def test_calculate_county_statistics(self):
        schools = [
            School("School 1", 30.0, 40.0, 100, 2019),
            School("School 2", 40.0, 60.0, 100, 2019)
        ]
        stats = calculate_county_statistics(schools)
        self.assertEqual(stats["total_schools"], 2)
        self.assertEqual(stats["avg_obesity"], 35.0)
        self.assertEqual(stats["total_students"], 200)

    def test_analyze_economic_disparity(self):
        schools = [
            School("High Disadvantage School", 40.0, 60.0, 100, 2019),
            School("Low Disadvantage School", 20.0, 30.0, 100, 2019)
        ]
        analysis = analyze_economic_disparity(schools)

        self.assertEqual(analysis["high_disadvantage"]["count"], 1)
        self.assertEqual(analysis["low_disadvantage"]["count"], 1)

        self.assertEqual(analysis["high_disadvantage"]["avg_obesity"], 40.0)
        self.assertEqual(analysis["low_disadvantage"]["avg_obesity"], 20.0)

        self.assertEqual(analysis["disparity_factor"], 2.0)


if __name__ == "__main__":
    unittest.main()