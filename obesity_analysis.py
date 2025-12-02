from school import School

### Reads school data from text file and creates School objects. Returns list of School objects.
def load_data_from_file(filename):
    schools = []
    try:
        with open(filename, 'r') as file:
            next(file)
            for line_num, line in enumerate(file, 2):
                line = line.strip()
                if line:
                    try:
                        parts = line.split(',')
                        if len(parts) == 5:
                            school = School(
                                school_name=parts[0].strip(),
                                obesity_rate=parts[1].strip(),
                                economic_disadvantage_rate=parts[2].strip(),
                                students_tested=parts[3].strip(),
                                year=parts[4].strip()
                            )
                            schools.append(school)
                        else:
                            print(f"Warning: Line {line_num} has incorrect format: {line}")
                    except ValueError as e:
                        print(f"Error processing line {line_num}: {line} - {e}")

        print(f"Successfully loaded {len(schools)} schools")
        return schools

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

### Returns dictionary of county-wide statistics.
def calculate_county_statistics(schools):
    if not schools:
        return {}

    total_schools = len(schools)
    total_students = sum(school.students_tested for school in schools)
    avg_obesity = sum(school.obesity_rate for school in schools) / total_schools
    avg_economic_disadvantage = sum(school.economic_disadvantage_rate for school in schools) / total_schools

    obesity_rates = [school.obesity_rate for school in schools]
    min_obesity = min(obesity_rates)
    max_obesity = max(obesity_rates)

    above_avg_count = sum(1 for school in schools if school.obesity_rate > avg_obesity)

    return {
        "total_schools": total_schools,
        "total_students": total_students,
        "avg_obesity": avg_obesity,
        "avg_economic_disadvantage": avg_economic_disadvantage,
        "min_obesity": min_obesity,
        "max_obesity": max_obesity,
        "above_avg_count": above_avg_count,
        "above_avg_percent": (above_avg_count / total_schools) * 100
    }

### Analyzes relationship between economic disadvantage and obesity rates
def analyze_economic_disparity(schools):
    high_disadvantage_schools = []
    low_disadvantage_schools = []

    for school in schools:
        if school.is_economically_disadvantaged_school():
            high_disadvantage_schools.append(school)
        else:
            low_disadvantage_schools.append(school)

    high_disadvantage_avg = (sum(s.obesity_rate for s in high_disadvantage_schools) /
                             len(high_disadvantage_schools)) if high_disadvantage_schools else 0
    low_disadvantage_avg = (sum(s.obesity_rate for s in low_disadvantage_schools) /
                            len(low_disadvantage_schools)) if low_disadvantage_schools else 0

    disparity_factor = (high_disadvantage_avg / low_disadvantage_avg
                        if low_disadvantage_avg > 0 else 0)

    return {
        "high_disadvantage": {
            "schools": high_disadvantage_schools,
            "avg_obesity": high_disadvantage_avg,
            "count": len(high_disadvantage_schools)
        },
        "low_disadvantage": {
            "schools": low_disadvantage_schools,
            "avg_obesity": low_disadvantage_avg,
            "count": len(low_disadvantage_schools)
        },
        "disparity_factor": disparity_factor
    }

### Generate a detailed report for a specific school
def get_school_report(schools, statistics, economic_analysis):

    print("INDIVIDUAL SCHOOL REPORT")


    school_name = input("Enter school name: ").strip()

    found_school = None
    for school in schools:
        if school_name.lower() in school.school_name.lower():
            found_school = school
            break

    if not found_school:
        print(f"School '{school_name}' not found in database.")
        print("Available schools:")
        for school in schools:
            print(f"  - {school.school_name}")
        return

    print(f"\nDETAILED REPORT FOR: {found_school.school_name}")
    print("-" * 40)

    obese_count = found_school.calculate_obese_students()
    risk_category = found_school.get_risk_category()

    print(f"Obesity Rate: {found_school.obesity_rate}% ({risk_category} risk)")
    print(f"Economic Disadvantage Rate: {found_school.economic_disadvantage_rate}%")
    print(f"Students Tested: {found_school.students_tested}")
    print(f"Estimated Obese Students: {obese_count}")
    print(f"Year: {found_school.year}")

    comparison = found_school.compare_to_county_average(statistics['avg_obesity'])
    print(f"\nCOMPARISON TO COUNTY AVERAGE:")
    print(f"  {comparison}")

    economic_status = "High" if found_school.is_economically_disadvantaged_school() else "Low"
    print(f"Economic Status: {economic_status} Disadvantage")

    print(f"\nECONOMIC DISPARITY ANALYSIS:")
    high_disadvantage_avg = economic_analysis['high_disadvantage']['avg_obesity']
    low_disadvantage_avg = economic_analysis['low_disadvantage']['avg_obesity']

    if found_school.is_economically_disadvantaged_school():
        if found_school.obesity_rate > high_disadvantage_avg:
            print(f"  • This school's obesity rate is ABOVE average for high-disadvantage schools ({high_disadvantage_avg:.1f}%)")
        else:
            print(f"  • This school's obesity rate is BELOW average for high-disadvantage schools ({high_disadvantage_avg:.1f}%)")
    else:
        if found_school.obesity_rate > low_disadvantage_avg:
            print(f"  • This school's obesity rate is ABOVE average for low-disadvantage schools ({low_disadvantage_avg:.1f}%)")
        else:
            print(f"  • This school's obesity rate is BELOW average for low-disadvantage schools ({low_disadvantage_avg:.1f}%)")

    print(f"\nSCHOOL-SPECIFIC RECOMMENDATIONS:")
    if found_school.get_risk_category() in ["High", "Critical"]:
        print("  • Priority intervention needed for obesity reduction")
        print("  • Implement targeted nutrition education programs")
        print("  • Increase physical activity opportunities")

    if found_school.is_economically_disadvantaged_school():
        print("  • Focus on economic barrier reduction strategies")
        print("  • Provide access to affordable healthy food options")
        print("  • Partner with community organizations for support")

    if found_school.obesity_rate < statistics['avg_obesity']:
        print("  • Share successful strategies with other schools")
        print("  • Continue current effective programs")

### Provide conclusions about economic disadvantage and obesity relationship
def analyze_economic_relationship(economic_analysis):

    print("ECONOMIC DISADVANTAGE & OBESITY RELATIONSHIP")


    high_data = economic_analysis['high_disadvantage']
    low_data = economic_analysis['low_disadvantage']
    disparity = economic_analysis['disparity_factor']

    print(f"\nKEY FINDINGS:")
    print(f"• High Economic Disadvantage Schools (>50%):")
    print(f"  - Average Obesity Rate: {high_data['avg_obesity']:.1f}%")
    print(f"  - Number of Schools: {high_data['count']}")

    print(f"• Low Economic Disadvantage Schools (≤50%):")
    print(f"  - Average Obesity Rate: {low_data['avg_obesity']:.1f}%")
    print(f"  - Number of Schools: {low_data['count']}")

    print(f"\nDISPARITY ANALYSIS:")
    print(f"• Disparity Factor: {disparity:.2f}x")

    if disparity > 1.5:
        print("  - STRONG correlation: Economic disadvantage strongly linked to higher obesity")
    elif disparity > 1.2:
        print("  - MODERATE correlation: Clear relationship between poverty and obesity")
    else:
        print("  - WEAK correlation: Limited relationship observed")

    print(f"\nCONCLUSIONS:")
    if high_data['avg_obesity'] > low_data['avg_obesity']:
        difference = high_data['avg_obesity'] - low_data['avg_obesity']
        print(f"• Students in high-poverty schools have {difference:.1f}% higher obesity rates")
        print("• Economic factors significantly impact childhood obesity")
        print("• Targeted interventions in disadvantaged schools are crucial")
    else:
        print("• Limited economic disparity observed in obesity rates")
        print("• Other factors may be more significant in this county")

### Run interactive mode for user
def interactive_mode(schools, statistics, economic_analysis):
    while True:

        print("\nSLO COUNTY CHILDHOOD OBESITY ANALYSIS")

        print("1. School specific report")
        print("2. Economic disadvantage relationship analysis")
        print("3. All schools summary")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == '1':
            get_school_report(schools, statistics, economic_analysis)
        elif choice == '2':
            analyze_economic_relationship(economic_analysis)
        elif choice == '3':
            print("\nALL SCHOOLS SUMMARY:")
            print("-" * 20)
            for school in schools:
                risk = school.get_risk_category()
                print(f"{school.school_name}: {school.obesity_rate}% obesity ({risk}), "
                      f"{school.economic_disadvantage_rate}% economic disadvantage")
        elif choice == '4':
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

        input("\nPress Enter to continue...")

### Main function to run the childhood obesity analysis program
def main():
    input_filename = "slo_schools_obesity.txt"

    schools = load_data_from_file(input_filename)

    if not schools:
        print("No data loaded. Please check your input file.")
        return

    print(f"Loaded {len(schools)} schools successfully")

    statistics = calculate_county_statistics(schools)
    economic_analysis = analyze_economic_disparity(schools)

    interactive_mode(schools, statistics, economic_analysis)

if __name__ == "__main__":
    print("PROGRAM STARTING")
    main()