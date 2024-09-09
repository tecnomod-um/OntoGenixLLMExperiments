# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 18:12:44 2023

@author: gines
"""
#%% import packages
import pandas as pd
import re
import math as mt
import mimetypes
import os
from chardet import UniversalDetector
import magic

from csv_tools import ensure_read_csv

def detect_enc(file_path):
   return magic.Magic(mime_encoding=True,).from_file(file_path)

def check_file_encoding_mime_type(file: str, default_encoding: str = 'utf-8', default_mime_type: str = 'text/plain') -> tuple[str, str]:
    """
        Checks the given file encoding (if exists), and the mime type and returns them.

        NOTE: It may check the file byte order mark (BOM): https://www.w3.org/International/questions/qa-byte-order-mark.en
        More info about this can be found here: https://en.wikipedia.org/wiki/Byte_order_mark
        For a python library that supports BOM encoding see this: https://docs.python.org/3/library/codecs.html#codecs.BOM
        It may be useful for knowing if the file must be read in "little endian" or "big endian" format.
        Also, for the file system encoding is recommended to check this: https://docs.python.org/es/3.10/library/sys.html#sys.platform:~:text=Disponibilidad%3A%20Unix.-,sys.getfilesystemencoding(),-%C2%B6

        file: path of the file with its extension
        default_encoding: by default we'll use utf-8 encoding
        default_mime_type: by default we'll use text/pain mime type
    """
    encoding : str = ''
    mime_type : str = ''
    try:
        # It asummes that the file exists and is readable
        # File size
        size = os.path.getsize(file)
        # Mime Type (optional)
        mime_type, _ = mimetypes.guess_type(file) # Second result is encoding but is not reliable
        # Encoding
        detector : UniversalDetector = UniversalDetector()
        detector.reset()
        for line in open(file, 'rb'):
            detector.feed(line)
            if detector.done: break
        detector.close()
        encoding = detector.result['encoding']
        # Warning about file
        if (size == 0 or encoding is None or len(encoding) == 0):
            print(f"*WARNING*: File of size {size} bytes might be empty or have an invalid encoding")
    except Exception as e:
        print(e) # TODO: Change to less generic error
    return (encoding or default_encoding, mime_type or default_mime_type)

## Convert float with decimal 0 to int

def conv_int(elem):
    if pd.isnull(elem):
      return elem
    else:
      return int(elem)   #24.0 to 24

def conv_data(elem):
    if pd.isnull(elem):
      return elem
    else:
      elem = str(elem).replace(',','.')
      return elem   #'24,1' to 24.1

## check if a number is a float with decimal 0
def check_int(elem):
    if pd.isnull(elem) or mt.ceil(elem) == elem:     #24.0001 != 24 or 24.0 == 24
        return 0
    else:
        return 1      ##If it is not an integer or float, then it is a string

## check if a string is a float with decimal separator as ','
def check_num(elem):
    if pd.isnull(elem):
        return 0
    elif re.match(r'^[+\-]?(\d+\.\d*|\d*\.\d+|\d+)$', str(elem).replace(',','.')):     #float o int pattern
        return 0
    else:
        return 1      ##If it is not a float nor int, then it is a string

def convert_nota_to_number(elem):
    '''Represents the number in scientific notation to its 
    corresponding float or int notation'''
    if pd.isnull(elem):
        return elem
    else:
        new_elem = pd.to_numeric(elem.replace(",", "."))
        if not check_int(new_elem):
           new_elem = conv_int(new_elem)
        else:
           new_elem = elem
        return new_elem

def check_scien_nota(fnumber):
    '''check if it has the correct scientific notation format'''
    if pd.isnull(fnumber):
      return 0
    else:
      fnumber = str(fnumber)    
      if re.match(r'[+\-]?(\d+\.\d*|\d*\.\d+|\d+)([eE][+\-]?\d+)', fnumber.replace(",", ".")):
          return 1
      else:
          return 0

# Remove specific columns by name function
def remove_columns_name(fileTable, *args):
  ''' 
  Remove columns of a table indicating their name
  '''
  return fileTable.drop(list(args), axis=1) 

# Remove specific columns by index function
def remove_columns_position(fileTable, *args):
  ''' 
  Filters rows of a table indicating their position
  '''
  list_args = []  #Store the positions minus one
  list_args = [arg-1 for arg in args]

  return fileTable.drop(fileTable.columns[list_args], axis=1)

# Remove rows by pattern function
def remove_rows(fileTable, filter_patt: str):
  ''' 
  Removes rows of a table containing a given pattern
  '''
  funct_a = lambda x: True if filter_patt in str(x) else False
  
  rows_index = fileTable[fileTable.map(funct_a).any(axis=1)].index

  return fileTable.drop(rows_index).reset_index(drop=True)

# Filter rows by pattern function
def filter_rows(fileTable, filter_patt: str):
  ''' 
  Filters rows of a table containing a given pattern
  '''
  funct_a = lambda x: True if filter_patt in str(x) else False
  
  return fileTable[fileTable.map(funct_a).any(axis=1)]

# Remove rows with all values NaN
def remove_rows_all_null(fileTable):
  ''' 
  Remove rows of a table whose values are all null
  '''
  return fileTable.dropna(how = 'all')

# Remove rows with at least one NaN value
def remove_rows_least_null(fileTable):
  ''' 
  Remove rows with at least one null value
  '''
  return fileTable.dropna()

# Remove duplicate rows
def remove_duplicate_rows(fileTable):
  ''' 
  Remove duplicate rows within a table
  '''
  return fileTable.drop_duplicates()

## Select a random number of rows (without replacement)
def random_sample_rows(fileTable, numb_rows, *random_seed):
  ''' 
  From a table, to obtain a random sample 
  of a given number of rows
  '''
  return fileTable.sample(n= numb_rows, random_state = random_seed, axis = 0, ignore_index = True)

## Descompose multivalued values by rows
def descompose_multivalues(fileTable, separatorMultivalue, *args):
  ''' 
  For each column with multivalues separated by a multivalue separator, 
  generate a row for each value keeping the values of the rest of the 
  columns the same
  '''

  for col in args:
    temp_df = pd.DataFrame(columns = fileTable.columns)  ##Stores the new rows of multivalues
    list_rows = []
    fileTable[col] = fileTable[col].str.split(separatorMultivalue)   ##Get a list of multivalues
    for i in range(len(fileTable[col])):                  ##Rows index
      if type(fileTable.at[i,col]) == list:             ##NO null values
        if len(fileTable.at[i,col])> 1:                   ##There is more of one value
          list_rows.append(i)
          for elem in fileTable.loc[i,col]:                 ##For each value
            temp_row = fileTable.loc[i].copy()                  ##Temporal Row to change
            temp_row.at[col]= elem
            temp_row = temp_row.to_frame().transpose()
            temp_df = pd.concat([temp_df,temp_row], ignore_index=True)
        else:
          fileTable.at[i,col]=fileTable.at[i,col][0]

    fileTable.drop(list_rows, inplace=True)               ##Remove rows with multivalues by index        
    fileTable = pd.concat([fileTable,temp_df], ignore_index=True)     ##Update file with the new rows with atomic data  

  return fileTable

def rev_datatypes(fileTable):
  '''Apply convert_dtypes to each column and
   convert float with all zeros into int and Categorical according to a threshold '''
  for column in fileTable.columns.values:
    if fileTable[column].dtypes == 'float64':
      if  fileTable[column].apply(check_int).sum() == 0:     ##All .0
        fileTable[column] = pd.array(fileTable[column], dtype = pd.Int64Dtype())
    elif fileTable[column].dtypes == 'object':
      if  fileTable[column].apply(check_num).sum() == 0:     ##All a,b or a.b
      #  fileTable[column] = fileTable[column].apply(conv_float)
      #  fileTable[column] = pd.array(fileTable[column], dtype = pd.Float64Dtype())
        fileTable[column] = fileTable[column].apply(conv_data)
        fileTable[column] = fileTable[column].convert_dtypes()
    #    if fileTable[column].dtypes == 'float64':
    #      if  fileTable[column].apply(check_int).sum() == 0:     ##All .0
    #        fileTable[column] = pd.array(fileTable[column], dtype = pd.Int64Dtype())  

  return fileTable

def convert_scientific_notation(fileTable):
    '''Convert a string or number in scientific notation to the
    corresponding float or integer'''
    for column in fileTable.columns.values:
        count_values = fileTable[column].count()  ##Number of values != NA by column
        num_scienti = fileTable[column].apply(check_scien_nota).sum()
        if count_values == num_scienti:
            fileTable[column] = fileTable[column].apply(convert_nota_to_number)
            count_int = fileTable[column].apply(check_int).sum()
            if not count_int:
                fileTable[column] = pd.array(fileTable[column], dtype = pd.Int64Dtype())

    return fileTable

def open_file_encoding(file_csv, separator = ',', coding = 'utf-8'):
    '''Open a file as a pandas dataframe, checking errors 
    of encoding'''
    try:
      with open(file_csv, encoding= coding, newline='') as file_name:        ## For windows is "cp1252"
          table_csv = pd.read_csv(file_name, sep=separator)
          print(f'Warning: Trying to open the file with user encoding {coding}')
    except UnicodeDecodeError:
      try:
        a = check_file_encoding_mime_type(file_csv, default_encoding=coding)
        with open(file_csv, encoding=a[0], newline='') as file_name:
            table_csv = pd.read_csv(file_name, sep=separator)
            print(f'Warning: Trying to open the file with Chardet auto-encoding {a[0]}')
      except UnicodeDecodeError:
        try:
          auto_coding = detect_enc(file_csv)
          with open(file_csv, encoding= auto_coding, newline='') as file_name:
              table_csv = pd.read_csv(file_name, sep=separator)   ##Pandas lector
              print(f'Warning: Trying to open the file with Magic auto-encoding {coding}')
        except:
           with open(file_csv, encoding= 'unicode_escape', newline='') as file_name:
              table_csv = pd.read_csv(file_name, sep=separator)   ##Pandas lector
              print(f'Warning: Trying to open the file with encoding "unicode_escape')

    return table_csv

#%% Main code
if __name__ == "__main__":
    from time import time
  ### Hyperparameters
    # separator = ','         ##Separator CSV fields
    # coding= 'utf-8'

##### FILES ############ FILES ############ FILES #######

  ## Input file
    name_input = "ratings_Beauty" #"ratings_Beauty" #"bbp_processed_data" #"eCommerce"
    path_input = "C:/Users/Dragg/Documents/Tecnomod/Code Gines/"
    file_csv = path_input + name_input + ".csv" 

  ## Output file
    path_output = path_input + "results/"
    file_out = path_output + "processed_" + name_input + ".csv"

# Open source CSV checking the encoding
    #table_csv = open_file_encoding(file_csv, separator, coding)
    table_csv = ensure_read_csv(file_csv)
    # TODO: This is a heuristic value. To determine the "true" one, we may need to adjust to the mean, using statistics.
    MAXIMUM_DF_SIZE_THRESHOLD = 20000 

    # (!) NOTE: The first try consumes less time, but it doesn't assure that we will have a size of at least MAXIMUM_DF_SIZE_THRESHOLD (if possible), like in the second try.

    ###### RUNTIME - TRY 1 ###
    ini = time()
    # Apply remove_rows all NaN values function & Apply remove_duplicate_rows function
    table_processed = table_csv.iloc[0:MAXIMUM_DF_SIZE_THRESHOLD,].dropna(how = 'all').drop_duplicates()
    # Export the new table to csv file
    #table_processed.to_csv(file_out, index=False, encoding= 'utf-8')
    ###### RUNTIME ###
    print(time()-ini, len(table_processed))
    
    ###### RUNTIME - TRY 2 ###
    ini = time()
    # Apply remove_rows all NaN values function & Apply remove_duplicate_rows function
    table_processed = table_csv.dropna(how = 'all').drop_duplicates().iloc[0:MAXIMUM_DF_SIZE_THRESHOLD,]
    # Export the new table to csv file
    #table_processed.to_csv(file_out, index=False, encoding= 'utf-8')
    ###### RUNTIME ###
    print(time()-ini, len(table_processed))


# Apply remove_rows all NaN values function  
    # table_processed = remove_rows_all_null(table_csv)

# Apply remove_columns by name function  
    # columns_remove1 = 'Net_Sales_3rd_Party_/_local_currency'
    # columns_remove2 = ''
    # table_processed = remove_columns_name(table_processed, columns_remove1)

# Apply remove_columns by position function  
    # columns_remove1 = 1
    # columns_remove2 = 2
    # table_processed = remove_columns_position(table_processed, columns_remove1, columns_remove2)

# Apply remove_rows at least one NaN value function  
    # table_processed = remove_rows_least_null(table_processed)

# Apply filter_rows function  
    # filter_patt = '2021'
    # table_processed = filter_rows(table_processed, filter_patt)

# Apply remove_rows function  
    # filter_patt = '|'
    # table_processed = remove_rows(table_processed, filter_patt)

# Apply get a random sample of rows function  
    # numb_rows = 25
    # random_seed = 12345
    # table_processed = random_sample_rows(table_processed, numb_rows, random_seed)

# Convert multivalue cells to atomic value cells funcction  
    # separatorMultivalue = '|'
    # columName1 = 'Sales_Document'
    # columName2 = 'Delivery'
    # table_processed = descompose_multivalues(table_processed, separatorMultivalue, columName1, columName2)

# Apply remove_duplicate_rows function  
    # table_processed = remove_duplicate_rows(table_processed)

# Convert scientific notation into its respective integer o float extended notation (default)
    # table_processed = convert_scientific_notation(table_processed)

# Refine datatypes (default)
    #table_processed = rev_datatypes(table_processed)

# Export the new table to csv file
    # table_processed.to_csv(file_out, index=False, encoding= 'utf-8')

# %%
