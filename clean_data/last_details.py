import pandas as pd

class HandleGrades:

    @staticmethod
    def _create_filter_fourth_grades(results):
        cepunt = 'CEPUNT'
        years = [2019, 2020]

        cepunt_data = results['tipo'] == cepunt
        year_data = results['periodo'].isin(years)

        filter_fourth_grades = (cepunt_data) & (year_data)

        return filter_fourth_grades
    
    @staticmethod
    def _create_filter_first_grades(results):
        types = ["EXTRAORDINARIO", "ORDINARIO"]
        year = 2024
        period = "II"

        type_data = results['tipo'].isin(types)
        year_data = results['periodo'] == year
        period_data = results['number'] == period

        filter_first_grades = (type_data) & (year_data) & (period_data)

        return filter_first_grades
    
    @staticmethod
    def _create_filter_third_grades(results):
        filter_first_grades = HandleGrades._create_filter_first_grades(
            results
        )

        filter_fourth_grades = HandleGrades._create_filter_fourth_grades(
            results
        )

        filter_third_grades = ~((filter_first_grades) | (filter_fourth_grades))

        return filter_third_grades
    
    @staticmethod
    def filter_fourth_grades(results):
        filter_fourth_grades = HandleGrades._create_filter_fourth_grades(
            results
        )

        fourth_grades = results[filter_fourth_grades]

        fourth_grades = fourth_grades.drop(['r1', 'r2', 'r3', 'r5'], axis=1)

        fourth_grades = fourth_grades.rename(
            columns={
                'r4': 'puntaje'
            }
        )

        return fourth_grades
    
    @staticmethod
    def filter_first_grades(results):
        filter_first_grades = HandleGrades._create_filter_first_grades(
            results
        )

        first_grades = results[filter_first_grades]

        first_grades = first_grades.drop(['r2', 'r3', 'r4', 'r5'], axis=1)

        first_grades = first_grades.rename(
            columns={
                'r1': 'puntaje'
            }
        )

        return first_grades
    
    @staticmethod
    def filter_third_grades(results):
        filter_third_grades = HandleGrades._create_filter_third_grades(
            results
        )

        third_grades = results[filter_third_grades]

        third_grades = third_grades.drop(['r1', 'r2', 'r4', 'r5'], axis=1)

        third_grades = third_grades.rename(
            columns={
                'r3': 'puntaje'
            }
        )

        return third_grades
    
    @staticmethod
    def combine_grades(grades1, grades3, grades4):

        results = pd.concat(
            [
                grades1,
                grades3,
                grades4
            ]
        )

        results = results.reset_index()
        results = results.drop(['index', 'n_df', 'year', 'month'], axis=1)
        
        return results