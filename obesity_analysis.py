###LIST OF ELEMENTARY SCHOOLS:
#PACHECO
#BISHOP'S PEAK
#LOS RANCHOS
#HAWTHORNE
#C.L. SMITH


from school import School

###Reads school data from text file and creates School objects. Returns list of School objects.

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

        print(f"✓ Successfully loaded {len(schools)} schools")
        return schools

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

###Returns dictionary of county-wide statistics.
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

    # Count schools above county average
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

### Categorizes schools by obesity risk level
def categorize_schools_by_risk(schools):

    risk_categories = {
        "Low": [],
        "Moderate": [],
        "High": [],
        "Critical": []
    }

    for school in schools:
        risk_category = school.get_risk_category()
        risk_categories[risk_category].append(school)

    return risk_categories

### Analyzes relationship between economic disadvantage and obesity rates
def analyze_economic_disparity(schools):

    high_disadvantage_schools = []
    low_disadvantage_schools = []

    for school in schools:
        if school.is_economically_disadvantaged_school():
            high_disadvantage_schools.append(school)
        else:
            low_disadvantage_schools.append(school)

# Calculate average obesity rates for each group
    high_disadvantage_avg = (sum(s.obesity_rate for s in high_disadvantage_schools) /
                             len(high_disadvantage_schools)) if high_disadvantage_schools else 0
    low_disadvantage_avg = (sum(s.obesity_rate for s in low_disadvantage_schools) /
                            len(low_disadvantage_schools)) if low_disadvantage_schools else 0

    # Calculate disparity factor
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

### Identifies schools with highest obesity rates for intervention
def identify_priority_schools(schools, top_n=5):

    # Sort schools by obesity rate (descending)
    sorted_schools = sorted(schools, key=lambda x: x.obesity_rate, reverse=True)
    return sorted_schools[:top_n]

### Identifies schools with lowest obesity rates for best practices study
def identify_successful_schools(schools, top_n=3):

    # Sort schools by obesity rate (ascending)
    sorted_schools = sorted(schools, key=lambda x: x.obesity_rate)
    return sorted_schools[:top_n]

### Generates recommendations based on analysis results
def generate_recommendations(statistics, risk_categories, economic_analysis, priority_schools):

    recommendations = {}

    # Critical intervention recommendations
    critical_count = len(risk_categories["Critical"])
    if critical_count > 0:
        recommendations["critical_intervention"] = (
            f"Immediate intervention needed for {critical_count} critical schools "
            f"(>40% obesity rate). Focus on nutrition education and physical activity programs."
        )
    else:
        recommendations["critical_intervention"] = (
            "No schools in critical range. Maintain monitoring and prevention programs."
        )

    # Economic disparity recommendations
    disparity = economic_analysis["disparity_factor"]
    if disparity > 1.3:
        recommendations["economic_disparity"] = (
            f"Strong economic disparity detected ({disparity:.1f}x higher obesity in "
            f"economically disadvantaged schools). Target resources to schools with "
            f">50% economic disadvantage."
        )
    else:
        recommendations["economic_disparity"] = (
            "Moderate economic disparity. Continue equity-focused programs."
        )

    # Best practices recommendations
    low_risk_count = len(risk_categories["Low"])
    if low_risk_count > 0:
        recommendations["best_practices"] = (
            f"Study {low_risk_count} low-obesity schools for successful strategies. "
            f"Share best practices county-wide."
        )

    # County-wide recommendations
    county_avg = statistics["avg_obesity"]
    if county_avg > 35:
        recommendations["county_wide"] = (
            f"County average obesity rate ({county_avg:.1f}%) is concerning. "
            f"Implement comprehensive county-wide health initiatives."
        )
    elif county_avg > 30:
        recommendations["county_wide"] = (
            f"County average obesity rate ({county_avg:.1f}%) is moderate. "
            f"Focus on prevention and maintaining positive trends."
        )
    else:
        recommendations["county_wide"] = (
            f"County average obesity rate ({county_avg:.1f}%) is good. "
            f"Continue current successful programs."
        )

    # Resource allocation recommendations
    if priority_schools:
        rec_schools = ", ".join([school.school_name for school in priority_schools[:3]])
        recommendations["resource_allocation"] = (
            f"Prioritize resources for: {rec_schools}. "
            f"These schools have the highest obesity rates and need targeted support."
        )

    return recommendations

### Displays comprehensive analysis results to console
def display_results(schools, statistics, risk_categories, economic_analysis, recommendations):

    print("SLO COUNTY CHILDHOOD OBESITY ANALYSIS")
    print()

    # County-wide statistics
    print("COUNTY-WIDE STATISTICS:")
    print(f"  Total Schools Analyzed: {statistics['total_schools']}")
    print(f"  Total Students Tested: {statistics['total_students']}")
    print(f"  Average Obesity Rate: {statistics['avg_obesity']:.1f}%")
    print(f"  Range: {statistics['min_obesity']:.1f}% - {statistics['max_obesity']:.1f}%")
    print(f"  Schools Above County Average: {statistics['above_avg_count']} "
          f"({statistics['above_avg_percent']:.1f}%)")
    print(f"  Average Economic Disadvantage: {statistics['avg_economic_disadvantage']:.1f}%")
    print()

    # Risk category breakdown
    print("RISK CATEGORY BREAKDOWN:")
    for category, school_list in risk_categories.items():
        print(f"  {category}: {len(school_list)} schools")
        if school_list and len(school_list) <= 5:  # Show details for small categories
            for school in school_list:
                print(f"    - {school.school_name} ({school.obesity_rate}%)")
    print()

    # Economic disparity analysis
    econ_data = economic_analysis
    print("ECONOMIC DISPARITY ANALYSIS:")
    print(f"  High Economic Disadvantage (>50%):")
    print(f"    - Average Obesity Rate: {econ_data['high_disadvantage']['avg_obesity']:.1f}%")
    print(f"    - Schools: {econ_data['high_disadvantage']['count']}")
    print(f"  Low Economic Disadvantage (≤50%):")
    print(f"    - Average Obesity Rate: {econ_data['low_disadvantage']['avg_obesity']:.1f}%")
    print(f"    - Schools: {econ_data['low_disadvantage']['count']}")
    print(f"  Disparity Factor: {econ_data['disparity_factor']:.2f}x "
          f"higher obesity in disadvantaged schools")
    print()

    # Priority schools
    priority_schools = identify_priority_schools(schools, 3)
    print("TOP PRIORITY SCHOOLS FOR INTERVENTION:")
    for i, school in enumerate(priority_schools, 1):
        risk = school.get_risk_category()
        obese_count = school.calculate_obese_students()
        print(f"{i}. {school.school_name}")
        print(f"   - Obesity: {school.obesity_rate}% ({risk})")
        print(f"   - Economic Disadvantage: {school.economic_disadvantage_rate}%")
        print(f"   - Students Affected: ~{obese_count} students")
        print(f"   - Comparison: {school.compare_to_county_average(statistics['avg_obesity'])}")
    print()

    # Successful schools
    successful_schools = identify_successful_schools(schools, 3)
    print("SCHOOLS WITH SUCCESSFUL OUTCOMES:")
    for i, school in enumerate(successful_schools, 1):
        risk = school.get_risk_category()
        print(f"{i}. {school.school_name} ({school.obesity_rate}% obesity, {risk})")
        if school.economic_disadvantage_rate > 40:
            print(
                f"   - Notable: Achieved low obesity despite {school.economic_disadvantage_rate}% economic disadvantage")
    print()

    # Recommendations
    print("RECOMMENDATIONS:")
    for key, recommendation in recommendations.items():
        print(f"✓ {recommendation}")
    print()

### Writes comprehensive analysis report to text file
def write_analysis_report(filename, schools, statistics, risk_categories, economic_analysis, recommendations):

    try:
        with open(filename, 'w') as file:
            file.write("SAN LUIS OBISPO COUNTY CHILDHOOD OBESITY ANALYSIS REPORT\n")
            file.write("Generated: [Current Date]\n")
            file.write("=" * 60 + "\n\n")

            # County-wide statistics
            file.write("COUNTY-WIDE STATISTICS:\n")
            file.write("-" * 25 + "\n")
            file.write(f"Total Schools Analyzed: {statistics['total_schools']}\n")
            file.write(f"Total Students Tested: {statistics['total_students']}\n")
            file.write(f"Average Obesity Rate: {statistics['avg_obesity']:.1f}%\n")
            file.write(f"Range: {statistics['min_obesity']:.1f}% - {statistics['max_obesity']:.1f}%\n")
            file.write(f"Average Economic Disadvantage: {statistics['avg_economic_disadvantage']:.1f}%\n\n")

            # Risk categories
            file.write("RISK CATEGORY BREAKDOWN:\n")
            file.write("-" * 25 + "\n")
            for category, school_list in risk_categories.items():
                file.write(f"{category} Risk (<30%): {len(school_list)} schools\n")
            file.write("\n")

            # High-risk schools
            file.write("HIGH-RISK SCHOOLS REQUIRING INTERVENTION:\n")
            file.write("-" * 40 + "\n")
            priority_schools = identify_priority_schools(schools, 5)
            for i, school in enumerate(priority_schools, 1):
                obese_count = school.calculate_obese_students()
                file.write(f"{i}. {school.school_name} - {school.obesity_rate}% "
                           f"({school.get_risk_category()})\n")
                file.write(f"   - Economic Disadvantage: {school.economic_disadvantage_rate}%\n")
                file.write(f"   - Estimated Obese Students: {obese_count}\n")
                file.write(f"   - Students Tested: {school.students_tested}\n\n")

            # Economic disparity
            econ_data = economic_analysis
            file.write("ECONOMIC DISPARITY FINDINGS:\n")
            file.write("-" * 30 + "\n")
            file.write(f"High Disadvantage Schools (>50%): {econ_data['high_disadvantage']['count']} schools\n")
            file.write(f"Average Obesity (High Disadvantage): {econ_data['high_disadvantage']['avg_obesity']:.1f}%\n")
            file.write(f"Average Obesity (Low Disadvantage): {econ_data['low_disadvantage']['avg_obesity']:.1f}%\n")
            file.write(f"Disparity Factor: {econ_data['disparity_factor']:.2f}x\n\n")

            # Recommendations
            file.write("RECOMMENDATIONS:\n")
            file.write("-" * 15 + "\n")
            for key, recommendation in recommendations.items():
                # Convert key to readable title
                title = key.replace('_', ' ').title()
                file.write(f"{title}:\n")
                file.write(f"  {recommendation}\n\n")

            file.write("=" * 60 + "\n")
            file.write("END OF REPORT\n")

        print(f"Report saved to: {filename}")

    except Exception as e:
        print(f"Error writing report: {e}")

### Generate a detailed report for a specific school
def get_school_report(schools, statistics, economic_analysis):

    print("\n" + "=" * 60)
    print("INDIVIDUAL SCHOOL REPORT")
    print("=" * 60)

    # Get school name from user
    school_name = input("Enter school name: ").strip()

    # Find the school
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

    # Display school details
    print(f"\nDETAILED REPORT FOR: {found_school.school_name}")
    print("-" * 40)

    # Basic school info
    obese_count = found_school.calculate_obese_students()
    risk_category = found_school.get_risk_category()

    print(f"Obesity Rate: {found_school.obesity_rate}% ({risk_category} risk)")
    print(f"Economic Disadvantage Rate: {found_school.economic_disadvantage_rate}%")
    print(f"Students Tested: {found_school.students_tested}")
    print(f"Estimated Obese Students: {obese_count}")
    print(f"Year: {found_school.year}")

    # Comparison to county average
    comparison = found_school.compare_to_county_average(statistics['avg_obesity'])
    print(f"\nCOMPARISON TO COUNTY AVERAGE:")
    print(f"  {comparison}")

    # Economic status analysis
    economic_status = "High" if found_school.is_economically_disadvantaged_school() else "Low"
    print(f"Economic Status: {economic_status} Disadvantage")

    # Relationship analysis
    print(f"\nECONOMIC DISPARITY ANALYSIS:")
    high_disadvantage_avg = economic_analysis['high_disadvantage']['avg_obesity']
    low_disadvantage_avg = economic_analysis['low_disadvantage']['avg_obesity']

    if found_school.is_economically_disadvantaged_school():
        if found_school.obesity_rate > high_disadvantage_avg:
            print(
                f"  • This school's obesity rate is ABOVE average for high-disadvantage schools ({high_disadvantage_avg:.1f}%)")
        else:
            print(
                f"  • This school's obesity rate is BELOW average for high-disadvantage schools ({high_disadvantage_avg:.1f}%)")
    else:
        if found_school.obesity_rate > low_disadvantage_avg:
            print(
                f"  • This school's obesity rate is ABOVE average for low-disadvantage schools ({low_disadvantage_avg:.1f}%)")
        else:
            print(
                f"  • This school's obesity rate is BELOW average for low-disadvantage schools ({low_disadvantage_avg:.1f}%)")

    # Recommendations for this school
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

    print("\n" + "=" * 60)
    print("ECONOMIC DISADVANTAGE & OBESITY RELATIONSHIP")
    print("=" * 60)

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
def interactive_mode(schools, statistics, economic_analysis, recommendations):

    while True:
        print("\n" + "=" * 60)
        print("=" * 60)
        print("1. School specific report")
        print("2. Economic disadvantage relationship analysis")
        print("3. All schools summary")
        print("4. View county-wide statistics")
        print("5. Exit interactive mode")

        choice = input("\nEnter your choice (1-5): ").strip()

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
            print("\nCOUNTY-WIDE STATISTICS:")
            print("-" * 25)
            print(f"Total Schools: {statistics['total_schools']}")
            print(f"Average Obesity Rate: {statistics['avg_obesity']:.1f}%")
            print(f"Range: {statistics['min_obesity']:.1f}% - {statistics['max_obesity']:.1f}%")
            print(f"Average Economic Disadvantage: {statistics['avg_economic_disadvantage']:.1f}%")
        elif choice == '5':
            print("Exiting interactive mode...")
            break
        else:
            print("Invalid choice. Please enter 1-5.")

        input("\nPress Enter to continue...")

### Main function to run the childhood obesity analysis program
def main():

    input_filename = "slo_schools_obesity.txt"


    schools = load_data_from_file(input_filename)

    if not schools:
        print("No data loaded. Please check your input file.")
        return

    print(f"Loaded {len(schools)} schools successfully")

    # Test user input
    test_input = input("Type start: ")
    print(f"You typed: {test_input}")

    # If that works, start the full interactive mode
    print("\nSTARTING FULL INTERACTIVE MODE")

    # Calculate ALL the required statistics
    statistics = calculate_county_statistics(schools)
    risk_categories = categorize_schools_by_risk(schools)  # This was missing!
    economic_analysis = analyze_economic_disparity(schools)
    priority_schools = identify_priority_schools(schools, 5)

    # Now generate recommendations with ALL the required data
    recommendations = generate_recommendations(statistics, risk_categories, economic_analysis, priority_schools)

    interactive_mode(schools, statistics, economic_analysis, recommendations)


if __name__ == "__main__":
    print("PROGRAM STARTING")
    main()