import pandas as pd
from scipy.stats import ks_2samp


def calculate_data_drift(
        old_data,
        new_data
):

    drift_results = {}


    # ---------------------------------
    # Numeric Feature Drift
    # ---------------------------------

    numeric_columns = (

        old_data
        .select_dtypes(
            include="number"
        )
        .columns

    )


    for column in numeric_columns:


        if column in new_data.columns:


            score, p_value = ks_2samp(

                old_data[column],

                new_data[column]

            )


            drift_results[column] = round(

                score * 100,

                2

            )


    return drift_results




def drift_status(
        drift_results
):


    if len(drift_results) == 0:

        return "NO DATA"



    average_drift = (

        sum(
            drift_results.values()
        )

        /

        len(drift_results)

    )



    if average_drift < 10:

        return "STABLE"



    elif average_drift < 25:

        return "WARNING"



    else:

        return "DRIFT DETECTED"