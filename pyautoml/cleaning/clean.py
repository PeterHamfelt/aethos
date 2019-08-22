import os

import pandas as pd
import pyautoml
import yaml
from pyautoml.base import MethodBase
from pyautoml.cleaning.categorical import *
from pyautoml.cleaning.numeric import *
from pyautoml.cleaning.util import *

pkg_directory = os.path.dirname(pyautoml.__file__)

with open(f"{pkg_directory}/technique_reasons.yml", 'r') as stream:
    try:
        technique_reason_repo = yaml.safe_load(stream)
    except yaml.YAMLError as e:
        print("Could not load yaml file.")

class Clean(MethodBase):

    
    def __init__(self, data=None, train_data=None, test_data=None, test_split_percentage=0.2, use_full_data=False, target_field="", report_name=None):   

        super().__init__(data=data, train_data=train_data, test_data=test_data, test_split_percentange=test_split_percentage,
                         use_full_data=use_full_data, target_field=target_field, report_name=report_name)
        
        if self.data_properties.report is not None:
            self.report.write_header("Cleaning")


    def remove_columns(self, threshold: float):
        """
        Remove columns from the dataframe that have more than the threshold value of missing columns.
        Example: Remove columns where > 50% of the data is missing.

        This function exists in `clean/utils.py`
        
        Parameters
        ----------
        threshold : float
            Value between 0 and 1 that describes what percentage of a column can be missing values.
        
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided. 
        """

        report_info = technique_reason_repo['clean']['general']['remove_columns']

        if self.data_properties.use_full_data:            
            #Gather original data information
            original_columns = set(list(self.data_properties.data.columns))

            self.data_properties.data = remove_columns_threshold(threshold, data=self.data_properties.data)

            #Write to report
            if self.report is not None:
                new_columns = original_columns.difference(self.data_properties.data.columns)
                self.report.report_technique(report_info, new_columns)

            return self.data_properties.data

        else:
            #Gather original data information
            original_columns = set(list(self.data_properties.train_data.columns))

            self.data_properties.train_data, self.data_properties.test_data = remove_columns_threshold(threshold,
                                                                                                        train_data=self.data_properties.train_data,
                                                                                                        test_data=self.data_properties.test_data)

            if self.report is not None:
                new_columns = original_columns.difference(self.data_properties.train_data.columns)
                self.report.report_technique(report_info, new_columns)

            return self.data_properties.train_data, self.data_properties.test_data


    def remove_rows(self, threshold: float):
        """
        Remove rows from the dataframe that have more than the threshold value of missing rows.
        Example: Remove rows where > 50% of the data is missing.

        This function exists in `clean/utils.py`.

        Parameters
        ----------
        threshold : float
            Value between 0 and 1 that describes what percentage of a row can be missing values.
        
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided. 
        """

        report_info = technique_reason_repo['clean']['general']['remove_rows']

        if self.data_properties.use_full_data:
            self.data_properties.data = remove_rows_threshold(threshold, data=self.data_properties.data)

            #Write to report
            if self.report is not None:            
                self.report.report_technique(report_info, [])

            return self.data_properties.data

        else:
            self.data_properties.train_data, self.data_properties.test_data = remove_rows_threshold(threshold,
                                                                                                    train_data=self.data_properties.train_data,
                                                                                                    test_data=self.data_properties.test_data)

            #Write to report
            if self.report is not None:            
                self.report.report_technique(report_info, [])                                                                                    

            return self.data_properties.train_data, self.data_properties.test_data
    
    def replace_missing_mean(self, list_of_cols=[]):
        """
        Replaces missing values in every numeric column with the mean of that column.

        Mean: Average value of the column. Effected by outliers.

        This function exists in `clean/numeric.py` as `replace_missing_mean_median_mode`.
        
        Parameters
        ----------
        list_of_cols : list, optional
            A list of specific columns to apply this technique to, by default []
        
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided. 
        """

        report_info = technique_reason_repo['clean']['numeric']['mean']

        if self.data_properties.use_full_data:
            self.data_properties.data = replace_missing_mean_median_mode("mean", list_of_cols, data=self.data_properties.data)

            #Write to report
            if self.report is not None:            
                if list_of_cols:
                    self.report.report_technique(report_info, list_of_cols)
                else:
                    list_of_cols = _numeric_input_conditions(list_of_cols, self.data_properties.data, None)
                    self.report.report_technique(report_info, list_of_cols)

            return self.data_properties.data

        else:
            self.data_properties.train_data, self.data_properties.test_data = replace_missing_mean_median_mode("mean",
                                                                                                            list_of_cols=list_of_cols,
                                                                                                            train_data=self.data_properties.train_data,
                                                                                                            test_data=self.data_properties.test_data)
            
            if self.report is not None:
                if list_of_cols:
                    self.report.report_technique(report_info, list_of_cols)
                else:
                    list_of_cols = _numeric_input_conditions(list_of_cols, None, self.data_properties.train_data)
                    self.report.report_technique(report_info, list_of_cols)

            return self.data_properties.train_data, self.data_properties.test_data

    def replace_missing_median(self, list_of_cols=[]):
        """
        Replaces missing values in every numeric column with the median of that column.

        Median: Middle value of a list of numbers. Equal to the mean if data follows normal distribution. Not effected much by anomalies.

        This function exists in `clean/numeric.py` as `replace_missing_mean_median_mode`.
        
        Parameters
        ----------
        list_of_cols : list, optional
            A list of specific columns to apply this technique to., by default []
        
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided. 
        """

        report_info = technique_reason_repo['clean']['numeric']['median']

        if self.data_properties.use_full_data:
            self.data_properties.data = replace_missing_mean_median_mode("median", list_of_cols, data=self.data_properties.data)
            
            if self.report is not None:
                if list_of_cols:
                    self.report.report_technique(report_info, list_of_cols)
                else:
                    list_of_cols = _numeric_input_conditions(list_of_cols, self.data_properties.data, None)
                    self.report.report_technique(report_info, list_of_cols)

            return self.data_properties.data

        else:
            self.data_properties.train_data, self.data_properties.test_data = replace_missing_mean_median_mode("median",
                                                                                                            list_of_cols=list_of_cols,
                                                                                                            train_data=self.data_properties.train_data,
                                                                                                            test_data=self.data_properties.test_data)

            if self.report is not None:
                if list_of_cols:
                    self.report.report_technique(report_info, list_of_cols)
                else:
                    list_of_cols = _numeric_input_conditions(list_of_cols, None, self.data_properties.train_data)
                    self.report.report_technique(report_info, list_of_cols)

            return self.data_properties.train_data, self.data_properties.test_data

    def replace_missing_mostcommon(self, list_of_cols=[]):
        """
        Replaces missing values in every numeric column with the most common value of that column

        Mode: Most common value.

        This function exists in `clean/numeric.py` as `replace_missing_mean_median_mode`.
        
        Parameters
        ----------
        list_of_cols : list, optional
            A list of specific columns to apply this technique to., by default []
        
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
            * Returns 2 Dataframes if Train and Test data is provided. 
        """
       
        report_info = technique_reason_repo['clean']['numeric']['mode']

        if self.data_properties.use_full_data:
            self.data_properties.data = replace_missing_mean_median_mode("most_frequent", list_of_cols, data=self.data_properties.data)

            if self.report is not None:
                if list_of_cols:
                    self.report.report_technique(report_info, list_of_cols)
                else:
                    list_of_cols = _numeric_input_conditions(list_of_cols, self.data_properties.data, None)
                    self.report.report_technique(report_info, list_of_cols)

            return self.data_properties.data

        else:
            self.data_properties.train_data, self.data_properties.test_data = replace_missing_mean_median_mode("most_frequent",
                                                                                                            list_of_cols=list_of_cols,
                                                                                                            train_data=self.data_properties.train_data,
                                                                                                            test_data=self.data_properties.test_data)
            if self.report is not None:
                if list_of_cols:
                    self.report.report_technique(report_info, list_of_cols)
                else:
                    list_of_cols = _numeric_input_conditions(list_of_cols, None, self.data_properties.train_data)
                    self.report.report_technique(report_info, list_of_cols)

            return self.data_properties.train_data, self.data_properties.test_data

    def replace_missing_constant(self, constant=0, col_to_constant=None):
        """
        Replaces missing values in every numeric column with a constant.

        This function exists in `clean/numeric.py` as `replace_missing_constant`.
        
        
        Parameters
        ----------
        constant : int or float, optional
            Numeric value to replace all missing values with , by default 0
        col_to_constant : list or dict, optional
            A list of specific columns to apply this technique to or a dictionary
            mapping {'ColumnName': `constant`}, by default None
        
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided. 

        Examples
        --------
        >>> replace_missing_constant({'a': 1, 'b': 2, 'c': 3})

        >>> replace_missing_constant(1, ['a', 'b', 'c'])
        """

        report_info = technique_reason_repo['clean']['numeric']['constant']

        if self.data_properties.use_full_data:
            self.data_properties.data = replace_missing_constant(constant, col_to_constant, data=self.data_properties.data)

            if self.report is not None:
                if col_to_constant is None:
                    self.report.report_technique(report_info, self.data_properties.data.columns)
                else:
                    self.report.report_technique(report_info, list(col_to_constant))

            return self.data_properties.data

        else:
            self.data_properties.train_data, self.data_properties.test_data = replace_missing_constant(constant,
                                                                                                    col_to_constant,
                                                                                                    train_data=self.data_properties.train_data,
                                                                                                    test_data=self.data_properties.test_data)

            if self.report is not None:
                if col_to_constant is None:
                    self.report.report_technique(report_info, self.data_properties.train_data.columns)
                else:
                    self.report.report_technique(report_info, list(col_to_constant))

            return self.data_properties.train_data, self.data_properties.test_data

    def replace_missing_new_category(self, new_category=None, col_to_category=None):
        """
        Replaces missing values in categorical column with its own category. The categories can be autochosen
        from the defaults set.

        For numeric categorical columns default values are: -1, -999, -9999
        For string categorical columns default values are: "Other", "Unknown", "MissingDataCategory"

        This function exists in `clean/categorical.py` as `replace_missing_new_category`.
        
        Parameters
        ----------
        new_category : str, int, or float, optional
            Category to replace missing values with, by default None
        col_to_category : list or dict, optional
            A list of specific columns to apply this technique to or a dictionary
            mapping {'ColumnName': `constant`}, by default None
        
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided. 

        Examples
        --------
        >>> ReplaceMissingCategory({'a': "Green", 'b': "Canada", 'c': "December"})

        >>> ReplaceMissingCategory("Blue", ['a', 'b', 'c'])
        """

        report_info = technique_reason_repo['clean']['categorical']['new_category']

        if self.data_properties.use_full_data:
            self.data_properties.data = replace_missing_new_category(constant=new_category, col_to_category=col_to_category, data=self.data_properties.data)

            if self.report is not None:
                if col_to_category is None:
                    self.report.report_technique(report_info, self.data_properties.data.columns)
                else:
                    self.report.report_technique(report_info, list(col_to_category))

            return self.data_properties.data

        else:
            self.data_properties.train_data, self.data_properties.test_data = replace_missing_new_category(constant=new_category,
                                                                                                        col_to_category=col_to_category,                                                                                                    
                                                                                                        train_data=self.data_properties.train_data,
                                                                                                        test_data=self.data_properties.test_data)

            if self.report is not None:
                if col_to_category is None:
                    self.report.report_technique(report_info, self.data_properties.train_data.columns)
                else:
                    self.report.report_technique(report_info, list(col_to_category))                                                                                                   

            return self.data_properties.train_data, self.data_properties.test_data


    def replace_missing_remove_row(self, cols_to_remove: list):
        """
        Remove rows where the value of a column for those rows is missing.

        This function exists in `clean/categorical.py` as `replace_missing_remove_row`.
        
        Parameters
        ----------
        cols_to_remove : list
            A list of specific columns to remove.

        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided. 
        """

        report_info = technique_reason_repo['clean']['categorical']['remove_rows']

        if self.data_properties.use_full_data:
            self.data_properties.data = replace_missing_remove_row(cols_to_remove, data=self.data_properties.data)

            if self.report is not None:
                self.report.report_technique(report_info, cols_to_remove)

            return self.data_properties.data

        else:
            self.data_properties.train_data, self.data_properties.test_data = replace_missing_remove_row(cols_to_remove,                                                                                                    
                                                                                                    train_data=self.data_properties.train_data,
                                                                                                    test_data=self.data_properties.test_data)                                                                                        

            if self.report is not None:
                self.report.report_technique(report_info, list(cols_to_remove))

            return self.data_properties.train_data, self.data_properties.test_data

    def remove_duplicate_rows(self, list_of_cols=[]):
        """
        Remove rows from the data that are exact duplicates of each other and leave only 1.
        This can be used to reduce processing time or performance for algorithms where
        duplicates have no effect on the outcome (i.e DBSCAN)

        This function exists in `clean/util.py` as `remove_duplicate_rows`.
       
        Parameters
        ----------
        list_of_cols : list, optional
            A list of specific columns to apply this technique to, by default []
       
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided. 
        """
    
        report_info = technique_reason_repo['clean']['general']['remove_duplicate_rows']
    
        if self.data_properties.use_full_data:
            self.data_properties.data = remove_duplicate_rows(list_of_cols=list_of_cols, data=self.data_properties.data)
    
            return self.data_properties.data
    
        else:
            self.data_properties.train_data, self.data_properties.test_data = remove_duplicate_rows(list_of_cols=[],
                                                                                                train_data=self.data_properties.train_data,
                                                                                                test_data=self.data_properties.test_data)

            return self.data_properties.train_data, self.data_properties.test_data

    def remove_duplicate_columns(self):
        """
        Remove columns from the data that are exact duplicates of each other and leave only 1.
        
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided. 
        """
    
        report_info = technique_reason_repo['clean']['general']['remove_duplicate_columns']
    
        if self.data_properties.use_full_data:
            self.data_properties.data = remove_duplicate_columns(data=self.data_properties.data)

            if self.report is not None:
                self.report.ReportTechnique(report_info)
    
            return self.data_properties.data
    
        else:
            self.data_properties.train_data, self.data_properties.test_data = remove_duplicate_columns(train_data=self.data_properties.train_data,
                                                                                                        test_data=self.data_properties.test_data)

            if self.report is not None:
                self.report.ReportTechnique(report_info)

            return self.data_properties.train_data, self.data_properties.test_data

    def replace_missing_random_discrete(self, list_of_cols: list):
        """
        Replace missing values in with a random number based off the distribution (number of occurences) 
        of the data.
        
        Parameters
        ----------
        list_of_cols : list
            A list of specific columns to apply this technique to, by default []
        
        Returns
        -------
        Dataframe, *Dataframe:
            Cleaned columns of the dataframe(s) provides with the provided constant.
            
        * Returns 2 Dataframes if Train and Test data is provided.

        Examples
        --------
        >>> For example if your data was [5, 5, NaN, 1, 2]
        >>> There would be a 50% chance that the NaN would be replaced with a 5, a 25% chance for 1 and a 25% chance for 2.

        """
    
        report_info = technique_reason_repo['clean']['general']['random_discrete']
    
        if self.data_properties.use_full_data:   
            self.data_properties.data = replace_missing_random_discrete(list_of_cols, data=self.data_properties.data)

            if self.report is not None:
                self.report.ReportTechnique(report_info)
    
            return self.data_properties.data
    
        else:
            self.data_properties.train_data, self.data_properties.test_data = replace_missing_random_discrete(list_of_cols,
                                                                                                            train_data=self.data_properties.train_data,
                                                                                                            test_data=self.data_properties.test_data)
    
            if self.report is not None:
                self.report.ReportTechnique(report_info)
    
            return self.data_properties.train_data, self.data_properties.test_data