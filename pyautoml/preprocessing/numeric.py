"""
This function has the following methods:

preprocess_normalize
"""

import pandas as pd
from pyautoml.util import (_function_input_validation,
                           _numeric_input_conditions, drop_replace_columns)
from sklearn.preprocessing import MinMaxScaler


def preprocess_normalize(list_of_cols=[], params={}, **datasets):
    """
    Function that normalizes all numeric values between 0 and 1 to bring features into same domain.
    
    Parameters
    ----------
    list_of_cols : list, optional
        A list of specific columns to apply this technique to
        If `list_of_cols` is not provided, the strategy will be
        applied to all numeric columns, by default []
    params : dict, optional
        A dictionary of parmaters to pass into MinMaxScaler() constructor
        from Scikit-Learn, by default {}

    Either the full data or training data plus testing data MUST be provided, not both.

    data : DataFrame
        Full dataset, by default None
    train_data : DataFrame
        Training dataset, by default None
    test_data : DataFrame
        Testing dataset, by default None
    
    Returns
    -------
    Dataframe, *Dataframe
        Transformed dataframe with rows with a missing values in a specific column are missing

    * Returns 2 Dataframes if Train and Test data is provided. 
    """

    data = datasets.pop('data', None)
    train_data = datasets.pop('train_data', None)
    test_data = datasets.pop('test_data', None)

    if datasets:
        raise TypeError(f"Invalid parameters passed: {str(datasets)}")    

    if not _function_input_validation(data, train_data, test_data):
        raise ValueError("Function input is incorrectly provided.")

    list_of_cols = _numeric_input_conditions(list_of_cols, data, train_data)
    scaler = MinMaxScaler(**params)

    if data is not None:
        scaled_data = scaler.fit_transform(data[list_of_cols])
        scaled_df = pd.DataFrame(scaled_data, columns=list_of_cols)
        data = drop_replace_columns(data, list_of_cols, scaled_df)
        
        return data
    
    else:
        scaled_train_data = scaler.fit_transform(train_data)
        scaled_train_df = pd.DataFrame(scaled_train_data, columns=list_of_cols)
        train_data = drop_replace_columns(train_data, list_of_cols, scaled_train_df)

        scaled_test_data = scaler.transform(test_data)
        scaled_test_df = pd.DataFrame(scaled_test_data, columns=list_of_cols)
        test_data = drop_replace_columns(test_data, list_of_cols, scaled_test_df)

        return train_data, test_data