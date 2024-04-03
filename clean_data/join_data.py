import pandas as pd

class Perform:

    @staticmethod
    def join_titles_with_results(titles, results):

        joined_data = pd.merge(
            results,
            titles,
            left_on='n_df',
            right_index=True
        )

        return joined_data

    @staticmethod
    def _create_year(results):
        return (
            results
            ['fecha']
            .dt.year
        )

    @staticmethod
    def _create_month(results):
        return (
            results
            ['fecha']
            .dt.month
        )

    @staticmethod
    def _add_year_and_month(results):
        results['year'] = Perform._create_year(results)
        results['month'] = Perform._create_month(results)

        return results

    @staticmethod
    def _filter_by_month(results):
        return (
            results
            ['fecha']
            .dt.month > 6
        )

    @staticmethod
    def _filter_by_number(results):
        return (
            results['number'] == "I"
        )

    @staticmethod
    def add_periods(results):

        results = Perform._add_year_and_month(results)

        filter_month = Perform._filter_by_month(results)

        results.loc[filter_month, "number"] = "I"
        results.loc[~filter_month, "number"] = "II"

        filter_number = Perform._filter_by_number(results)

        results.loc[filter_number, "periodo"] = results["fecha"].dt.year + 1
        results.loc[~filter_number, "periodo"] = results["fecha"].dt.year

        results['periodo'] = results['periodo'].astype(int)

        return results