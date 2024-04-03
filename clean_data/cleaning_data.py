from clean_data.handle_raw_data import handle
from clean_data.clean_titles import HandleTitles
from clean_data.clean_results import HandleRawResults
from clean_data.join_data import Perform
from clean_data.last_details import HandleGrades

def generate_cleaned_data(name_raw_data):

    raw_titles, raw_results = handle(name_raw_data)

    titles = HandleTitles.titles_to_columns(raw_titles)
    results = HandleRawResults.generated_results(raw_results)

    combined_data = Perform.join_titles_with_results(titles, results)
    combined_data = Perform.add_periods(combined_data)

    fourth_grades = HandleGrades.filter_fourth_grades(combined_data)
    third_grades = HandleGrades.filter_third_grades(combined_data)
    first_grades = HandleGrades.filter_first_grades(combined_data)

    results = HandleGrades.combine_grades(first_grades, third_grades, fourth_grades)

    return results