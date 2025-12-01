class School:
    """Represents a single elementary school's obesity and demographic data."""

    def __init__(self, school_name, obesity_rate, economic_disadvantage_rate, students_tested, year):
        """Constructor to initialize school object."""
        self.school_name = school_name
        self.obesity_rate = float(obesity_rate)
        self.economic_disadvantage_rate = float(economic_disadvantage_rate)
        self.students_tested = int(students_tested)
        self.year = int(year)

    def calculate_obese_students(self):
        """Returns estimated number of obese/overweight students based on percentage and total tested."""
        return round((self.obesity_rate / 100) * self.students_tested)

    def get_risk_category(self):
        """Categorizes school obesity rate as Low (<30%), Moderate (30-35%), High (35-40%), or Critical (>40%)."""
        if self.obesity_rate < 30:
            return "Low"
        elif self.obesity_rate < 35:
            return "Moderate"
        elif self.obesity_rate <= 40:
            return "High"
        else:
            return "Critical"

    def is_economically_disadvantaged_school(self, threshold=50.0):
        """Returns True if school has economic disadvantage rate above threshold."""
        return self.economic_disadvantage_rate > threshold

    def compare_to_county_average(self, county_avg):
        """Compares school's obesity rate to county average and returns analysis."""
        difference = self.obesity_rate - county_avg
        if difference > 5:
            status = "significantly above"
        elif difference > 2:
            status = "above"
        elif difference < -5:
            status = "significantly below"
        elif difference < -2:
            status = "below"
        else:
            status = "about the same as"

        return f"{self.obesity_rate}% ({status} county average of {county_avg}%)"

    def __str__(self):
        """Returns formatted string representation of school data."""
        risk = self.get_risk_category()
        obese_count = self.calculate_obese_students()
        return (f"{self.school_name}: {self.obesity_rate}% obesity ({risk}), "
                f"{self.economic_disadvantage_rate}% economic disadvantage, "
                f"{obese_count} students affected")