# -*- coding: utf-8 -*-
"""
    Created on Mon Jul 31 18:12:44 2023

    File that implements the logic for creating the analysis matrixes for OntoGenix.

    @author: gines
    @author: drakopablo
"""
#%%
from typing import Tuple

import pandas as pd
from xsdDataType import XSDDataType
from csv_tools import ensure_read_csv

#### Constants ####

PUNTUATION_STR = '.,!?;:' # Just used in `feature_vector` if `add_additional_info` flag is set.
DEFAULT_PAIRS_DELIMITER = '____'
REFLEXIVE_PROPERTY_PAIR = '-' # '1:1' # TODO: Reflexive property not implemented yet.

#### Functions ####

def pd_infer_column_type(column:pd.DataFrame, default_datatype:str="string") -> str:
    """
        Infers the column type of a given pandas dataframe

        # https://andrewwegner.com/python-gotcha-comparisons.html#nan-nan # tldr; NaN is float
    """
    #infer_type = lambda x: pd.api.types.infer_dtype(x, skipna=True)
    try:
        return pd.api.types.infer_dtype(column, skipna=True)
    except TypeError as te:
        print(te)
        return default_datatype or "unknown"

def feature_vector(fileTable:pd.DataFrame, add_additional_info:bool=False, precision:int=5) -> pd.DataFrame:
    '''
        Method to calculate the feature vector of a given dataset.
        NOTE: Pandas' data types: https://pbpython.com/pandas_dtypes.html
        Example:
            # With add_additional_info == True
            columns=['DataType', 'XsdDataTypes', 'Total', 'NoNull', 'Unique',
                    'numWords', 'lenWord', 'numLetter', 'numDigit', 'numPunct']
            # With add_additional_info == False
            columns=['XsdDataTypes', 'Total', 'NoNull', 'Unique']
        Args:
            fileTable: pandas.DataFrame with the data
            add_additional_info: Flag to indicate whether to preprocess the data with additional statistical information or not
            precision: Number of decimals to use for the floating point precision numbers of the previous statistics
        Output:
            pd.DataFrame with the Feature Vector (FV)
    '''
    # Get column names and dimensions
    rows = fileTable.shape[0]
    # Initialize counts matrix
    df_counts = pd.DataFrame(index=fileTable.columns,
                             columns=['DataType', 'XsdDataTypes', 'Total',
                                    'NoNull', 'Unique', 'numWords', 'lenWord',
                                    'numLetter', 'numDigit', 'numPunct']) \
                if add_additional_info else \
                pd.DataFrame(index=fileTable.columns,
                             columns=['XsdDataTypes', 'Total', 'NoNull', 'Unique'])
    # Precompute fixed values
    df_counts['Total'] = rows
    df_counts['NoNull'] = fileTable.count(axis=0) # (fileTable.count(axis=0) / rows * 100).round(precision)
    df_counts['Unique'] = fileTable.nunique(axis=0)
    if add_additional_info:
        df_counts['DataType'] = fileTable.apply(pd_infer_column_type, axis=0) #fileTable.dtypes
        # Precompute column information outside loops
        precomputed_info = {}
        for column in fileTable.columns:
            col_data = fileTable[column].dropna()
            col_uniq = col_data.unique()
            col_uniq_series = pd.Series(col_uniq)
            # Calculate the distribution of the characters' type in the element.
            num_word = 0
            len_word = 0
            num_letter = 0
            num_digit = 0
            num_punct = 0
            for x in col_uniq_series:
                str_word = str(x) # Aux variable
                num_word += len(str_word.split())
                len_word += len(str_word)
                for c in str_word:
                    if c.isalpha():
                        num_letter += 1
                    elif c.isdigit():
                        num_digit += 1
                    if c in PUNTUATION_STR:
                        num_punct += 1
            # Populate the precomputed info dictionary
            precomputed_info[column] = {
                'col_uniq_series': col_uniq_series,
                'num_col_uniq': len(col_uniq),
                'num_word': num_word,
                'len_word': len_word,
                'num_letter': num_letter,
                'num_digit': num_digit,
                'num_punct': num_punct
            }
        # Populate the feature vector
        proportion = 1/rows # (!) Multiplication is better than division for the ALU
        for column in fileTable.columns:
            info = precomputed_info[column]
            df_counts.at[column, 'lenWord'] = round(info['len_word'] * proportion, precision)
            df_counts.at[column, 'numWords'] = round(info['num_word'] * proportion, precision)
            df_counts.at[column, 'numLetter'] = round(info['num_letter'] * proportion, precision)
            df_counts.at[column, 'numDigit'] = round(info['num_digit'] * proportion, precision)
            df_counts.at[column, 'numPunct'] = round(info['num_punct'] * proportion, precision)
    # Infer the xsd datatypes from the dataset
    xsdDT = XSDDataType(use_lru_cache=True, cache_maxsize=None)
    df_counts['XsdDataTypes'] = xsdDT.parse_df(fileTable.dropna(), vectorize_dataframe=True, show_only_best_datatypes=True)
    # Fill missing values with 0
    df_counts = df_counts.fillna(0)
    # Remove object from memory
    del xsdDT
    # Return the resulting dataframe
    return df_counts

@DeprecationWarning
def get_uniq_pairs(column1:pd.Series, column2:pd.Series, 
                   default_separator:str=DEFAULT_PAIRS_DELIMITER) -> Tuple[int, pd.DataFrame]:
    """
        Get the number of unique pairs between two columns after converting types and removing NaNs.
    """
    def convert_type(elem):
        '''If a value is not null,
        then convert its type into a string'''
        if pd.isnull(elem):
            pass
        elif type(elem) != str:
            elem = str(elem)
        return elem

    # # Convert types and remove rows with NaN in either column
    # dfuni = pd.DataFrame({'a': column1.apply(convert_type), 'b': column2.apply(convert_type)}).dropna()

    # # Generate unique pairs using concatenation with a separator and get unique values
    # uniq_pairs = dfuni['a'].astype(str) + default_separator + dfuni['b'].astype(str)

    uniq_pairs = (column1.astype(str) + default_separator + column2.astype(str)).dropna()
    # Return the count of unique pairs and the unique pairs themselves
    return uniq_pairs.nunique(), uniq_pairs.unique()

def count_num_of_pairs(uniq_pair_set:pd.DataFrame|list|set, 
                       default_separator:str=DEFAULT_PAIRS_DELIMITER) -> Tuple[int, int]:
    """
        Count unique elements in each part of the pairs separated by the given separator.
    """
    # Split the pairs into two columns and count unique values in each
    A, B = zip(*[str(pair).split(default_separator) for pair in uniq_pair_set])
    return len(set(A)), len(set(B))

# TODO: improve these matrixes
def cardinality_matrix(fileTable: pd.DataFrame, verbose: bool = False) -> pd.DataFrame:
    """
    Calculate the cardinality relationship matrix between each pair of columns in a DataFrame.
    """
    # Get column names and number of rows
    name_col = fileTable.columns
    rows = len(fileTable)
    
    # Precompute null counts and initialize results dictionary
    null_counts = fileTable.isnull().sum()
    results = {}
    
    # Iterate over each pair of columns
    for i, A_name in enumerate(name_col):
        for j, B_name in enumerate(name_col): #in range(i, len(name_col)):
            #B_name = name_col[j]

            if verbose:
                print(A_name, DEFAULT_PAIRS_DELIMITER, B_name)
            
            # Pre-fetch null counts for the columns
            null_count_A = null_counts[A_name]
            null_count_B = null_counts[B_name]

            # Handle cases where columns are the same
            if A_name == B_name:
                results[(A_name, B_name)] = REFLEXIVE_PROPERTY_PAIR # TODO: Reflexive property not implemented yet.
                continue
            
            # Handle cases where one of the columns is fully null
            if null_count_A == rows or null_count_B == rows:
                results[(A_name, B_name)] = '0:0'
                results[(B_name, A_name)] = '0:0'
                continue
            
            # Compute unique pairs and their counts
            column1 = fileTable[A_name]
            column2 = fileTable[B_name]
            # Generate unique pairs using concatenation with a separator and get unique values. NOTE: Without NaN values.
            uniq_pairs: pd.DataFrame = (column1.astype(str) + DEFAULT_PAIRS_DELIMITER + column2.astype(str)).dropna().unique() # df containing unique pairs
            num_uniq_pairs: int = len(uniq_pairs) # Number of unique pairs
            #num_uniq_pairs, uniq_pairs = get_uniq_pairs(column1, column2, DEFAULT_PAIRS_DELIMITER)
            num_uniq_A, num_uniq_B = count_num_of_pairs(uniq_pairs, DEFAULT_PAIRS_DELIMITER)

            # Determine "cardinality relationships"
            if null_count_A == 0 and null_count_B == 0:  # No null values
                results[(A_name, B_name)] = '1:1' if num_uniq_pairs == num_uniq_A else '1:N'
                results[(B_name, A_name)] = '1:1' if num_uniq_pairs == num_uniq_B else '1:N'
            elif null_count_A == 0:  # A_name non-null, B_name has nulls
                results[(A_name, B_name)] = '0:1' if num_uniq_pairs == num_uniq_A else '0:N'
                results[(B_name, A_name)] = '1:1' if num_uniq_pairs == num_uniq_B else '1:N'
            elif null_count_B == 0:  # B_name non-null, A_name has nulls
                results[(A_name, B_name)] = '1:1' if num_uniq_pairs == num_uniq_A else '1:N'
                results[(B_name, A_name)] = '0:1' if num_uniq_pairs == num_uniq_B else '0:N'
            else:  # Both fields have null values
                nan_mask = fileTable[[A_name, B_name]].isnull().any(axis=1)
                A_count = fileTable.loc[~fileTable[A_name].isnull() & nan_mask, B_name].isnull().sum()
                B_count = fileTable.loc[~fileTable[B_name].isnull() & nan_mask, A_name].isnull().sum()

                results[(A_name, B_name)] = (
                    '1:1' if num_uniq_pairs == num_uniq_A and A_count == 0 else
                    '0:1' if num_uniq_pairs == num_uniq_A else
                    '1:N' if A_count == 0 else
                    '0:N'
                )
                results[(B_name, A_name)] = (
                    '1:1' if num_uniq_pairs == num_uniq_B and B_count == 0 else
                    '0:1' if num_uniq_pairs == num_uniq_B else
                    '1:N' if B_count == 0 else
                    '0:N'
                )

    # Convert results to DataFrame
    df_fields = pd.DataFrame(index=name_col, columns=name_col)
    for (A_name, B_name), value in results.items():
        df_fields.at[A_name, B_name] = value

    return df_fields

def mer_matrix(card_matrix: pd.DataFrame) -> pd.DataFrame:
    '''Calculate the MER cardinality matrix from the cardinality matrix of CSV'''
    name_col = card_matrix.columns
    # Convert elements to list only once
    card_matrix = card_matrix.applymap(lambda x: x.split(':'))  # Convert '1:N' to ['1', 'N']
    # Initialize the result DataFrame
    mer_mat = pd.DataFrame(index=name_col, columns=name_col, dtype=str)
    for i, A_name in enumerate(name_col):
        for j, B_name in enumerate(name_col[i:], start=i):
            if A_name == B_name:
                mer_mat.at[A_name, B_name] = '-'
            else:
                max_one = card_matrix.at[A_name, B_name][1]  # Max cardinality A_name->B_name
                max_two = card_matrix.at[B_name, A_name][1]  # Max cardinality B_name->A_name

                if max_one == 'N' and max_two == 'N':
                    mer_mat.at[A_name, B_name] = 'M:N'
                    mer_mat.at[B_name, A_name] = 'N:M'
                else:
                    mer_mat.at[A_name, B_name] = f"{max_two}:{max_one}"
                    mer_mat.at[B_name, A_name] = f"{max_one}:{max_two}"
    # Return the resulting dataframe
    return mer_mat

def extreme_matrix(card_matrix: pd.DataFrame) -> pd.DataFrame:
    '''Calculate the extreme cardinality matrix from the cardinality matrix of CSV.'''
    name_col = card_matrix.columns
    # Convert elements to list only once
    card_matrix = card_matrix.applymap(lambda x: x.split(':'))  # Convert '1:N' to ['1', 'N']
    # Initialize the result DataFrame
    extr_mat = pd.DataFrame(index=name_col, columns=name_col, dtype=str)
    # Iterate over the fields of the dataframe
    for i, A_name in enumerate(name_col):
        for j, B_name in enumerate(name_col[i:], start=i):
            if A_name == B_name:
                extr_mat.at[A_name, B_name] = '-'
                continue
            # Calculate minimum cardinality
            if card_matrix.at[A_name, B_name][0] == 'N' or card_matrix.at[B_name, A_name][0] == 'N':
                min_one = 'N'
            else:
                min_one = str(min(int(card_matrix.at[A_name, B_name][0]), int(card_matrix.at[B_name, A_name][0])))
            # Calculate maximum cardinality
            if min_one == 'N':
                min_one = 'M'
                max_one = 'N'
            elif card_matrix.at[A_name, B_name][1] == 'N' or card_matrix.at[B_name, A_name][1] == 'N':
                max_one = 'N'
            else:
                max_one = str(max(int(card_matrix.at[A_name, B_name][1]), int(card_matrix.at[B_name, A_name][1])))
            # Store results
            extr_mat.at[A_name, B_name] = f"{min_one}:{max_one}"
            extr_mat.at[B_name, A_name] = f"{min_one}:{max_one}"
    # Return the resulting dataframe
    return extr_mat


#%%
if __name__ == "__main__":
    from time import time
    ####  Hyperparameters  #####  Hyperparameters  ## 
    separator = ','         ##Separator CSV fields
    precision = 5           ##Number of decimal digits
    threshold = 0.1         ## Percentage of error to consider a datatype

    ##### VARIABLES ############ VARIABLES ############ VARIABLES #######
    ## Input file
    name_input = "eCommerce" #"ratings_Beauty" #"bbp_processed_data" #"AmazonRating_data20k2"
    path_input = "C:/Users/Dragg/Documents/Tecnomod/Code Gines/"
    file_input = path_input + name_input + ".csv" 

    ## Output file
    path_output = path_input+"results/" #"E:/Basf/Tools/DataProcessingCSV/Ontogenix/CustomerComplaint/"
    file_features_vector = path_output + name_input + "_abridged_features_vector.csv"
    file_cardinality_matrix = path_output + name_input + "_cardinality_matrix.csv"
    file_mer_matrix = path_output + name_input + "_mer_matrix.csv"
    file_extreme_matrix = path_output + name_input + "_extreme_matrix.csv"
    ##########################################################################################
    ##########################################################################################

    ### OPEN FILE CSV for analysis of datatypes####
    fileTable = ensure_read_csv(file_input)

    ###### RUNTIME ###
    ini = time()

    # ##Generate the feature vector table
    DEFAULT_PRECISION = 5 # Number of decimal digits
    # df_feature_vector = feature_vector(fileTable, precision=DEFAULT_PRECISION, add_additional_info=False)
    # ### Save Feature vector into a CSV file format (rows = csv_columns, columns = features)
    # df_feature_vector.to_csv(file_features_vector, index=True, encoding="utf-8")
    
    ###### RUNTIME ###
    print(time()-ini)

    ###### RUNTIME ###
    ini = time()

    ##Generate the relation vector table
    df_relation_vector = cardinality_matrix(fileTable)
    ### Save Feature vector into a CSV file format (rows = csv_columns, columns = features)
    df_relation_vector.to_csv(file_cardinality_matrix, index=True, encoding="utf-8")
    
    ###### RUNTIME ###
    print(time()-ini)

    ###### RUNTIME ###
    # ini = time()

    # ##Generate the MER matrix
    # df_mer_matrix = mer_matrix(df_relation_vector)  
    # ### Save MER matrix into a CSV file format (rows = csv_columns, columns = features)
    # df_mer_matrix.to_csv(file_mer_matrix, index=True, encoding="utf-8")
    
    # ###### RUNTIME ###
    # print(time()-ini)

    # ###### RUNTIME ###
    # ini = time()

    # ##Generate the extreme matrix
    # df_extreme_matrix = extreme_matrix(df_relation_vector)  
    # ### Save MER matrix into a CSV file format (rows = csv_columns, columns = features)
    # df_extreme_matrix.to_csv(file_extreme_matrix, index=True, encoding="utf-8")

    # ###### RUNTIME ###
    # print(time()-ini)



# %%
