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
    def join_results_with_description(results, description):
        return (
            pd.merge(
                results,
                description,
                left_on='n_df',
                right_index=True
            )
        )