from transform.helper import delete_white_spaces, divide, join_headers_with_body_results, join_results_with_twp_content
from transform.header import headers_to_columns
from transform.body import create_body_results
from transform.grade import filter_first_grades, filter_third_grades, filter_fourth_grades, combine_grades, filling_data

def create_results_frame(link_results, twebpage_content):
    link_results = delete_white_spaces(link_results)
    raw_headers, raw_results = divide(link_results)

    date_column = headers_to_columns(raw_headers)
    results = create_body_results(raw_results)

    combined_data = join_headers_with_body_results(date_column, results)
    new_combined_data = join_results_with_twp_content(combined_data, twebpage_content)

    fourth_grades = filter_fourth_grades(new_combined_data)
    third_grades = filter_third_grades(new_combined_data)
    first_grades = filter_first_grades(new_combined_data)
    results = combine_grades(first_grades, third_grades, fourth_grades)
    results = filling_data(results)

    return results