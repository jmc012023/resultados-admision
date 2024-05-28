from clean_data.handle_raw_data import handle
from clean_data.clean_titles import HandleTitles
from clean_data.clean_results import HandleRawResults
from clean_data.join_data import Perform
from clean_data.last_details import HandleGrades

def generate_cleaned_data(raw_data, description):

    raw_data.to_csv("./clean_data/raw_data.csv", index=False)
    description.to_csv("./clean_data/description.csv", index=False)

    raw_titles, raw_results = handle(raw_data)

    date_column = HandleTitles.titles_to_columns(raw_titles)
    results = HandleRawResults.generated_results(raw_results)


    combined_data = Perform.join_titles_with_results(date_column, results)

    new_combined_data = Perform.join_results_with_description(combined_data, description)

    fourth_grades = HandleGrades.filter_fourth_grades(new_combined_data)
    third_grades = HandleGrades.filter_third_grades(new_combined_data)
    first_grades = HandleGrades.filter_first_grades(new_combined_data)

    results = HandleGrades.combine_grades(first_grades, third_grades, fourth_grades)

    return results