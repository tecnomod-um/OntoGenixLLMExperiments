# -*- coding: utf-8 -*-
"""
    Created on Mon Sep 2 10:14:27 2024

    File that contains several csv files related functionalities. 

    @author: drakopablo
"""
from functools import reduce
from mimetypes import guess_type
from magic.magic import Magic  # package: python-magic-bin # https://github.com/ahupp/python-magic
from csv import Sniffer
import pandas as pd

from typing import Tuple

def list_depth(array:list) -> int|None:
    """
        Returns the depth of a list (or list of lists).
    """
    # depth = lambda L: isinstance(L, list) and max(map(depth, L))+1
    return isinstance(array, list) and max(map(list_depth, array))+1

def flat_matrix(matrix:list, max_depth:int|None=None) -> list:
    """
        Returns the flattened matrix. If no max_depth is given, it applies until the minimum depth, 1.

        Args:
            matrix: A list of lists.
            max_depth: The maximum depth to be reached. This is, 1 <= max_depth <= matrix_depth.
    """
    # Check if the max_depth flag is set
    if max_depth and max_depth > 0:
        depth = list_depth(matrix)
        if depth > max_depth+1 and depth > 1:
            return flat_matrix(list(reduce(lambda x, y: x + y, matrix, [])), max_depth)
    # else:
    return list(reduce(lambda x, y: x + y, matrix, []))

def mr_mime(file_path:str, default_encoding:str = 'utf-8', 
            default_mime_type:str = 'text/plain', verbose:bool = False) -> Tuple[str, str]:
    """
        Returns the encoding and the "mime type" of the file.

        Args:
            file_path: path of the file with its extension
            default_encoding: by default we'll use utf-8 encoding
            default_mime_type: by default we'll use text/pain mime type
            verbose: if we'd like to print the error messages or not
    """
    try:
        # Importing the packages that are just needed for this method
        # from mimetypes import guess_type
        # from magic.magic import Magic  # package: python-magic-bin # https://github.com/ahupp/python-magic

        # Create a new magic instance
        magic_mime_encoding = Magic(mime_encoding=True)
        # Get the encoding and the mime type
        encoding = magic_mime_encoding.from_file(file_path) or default_encoding
        mime_type = guess_type(file_path)[0] or default_mime_type
        # Delete the instance that won't be used anymore
        del magic_mime_encoding
        # Return encoding and mime type tuple
        return (encoding or default_encoding, mime_type or default_mime_type)
    except PermissionError as pe:
        if verbose:
            print(pe)
        return "None", "None"
    except ImportError as ie:
        if verbose:
            print(f"Failed to import Magic: {ie}")
        return "None", "None"
    
def find_csv_delimiter(filename:str, encoding='utf_8', default_delimiter:str=",") -> str:
    """ If input is of type CSV, TSV, or similar, it returns the delimiter """
    #from csv import Sniffer
    try:
        with open(filename, 'r', encoding=encoding) as fp:
            delimiter = Sniffer().sniff(fp.readline()).delimiter
        return delimiter
    except Exception as e:
        print(e)
        return default_delimiter
    
def ensure_read_csv(filename:str, verbose:bool=False) -> pd.DataFrame:
    """
        Ensures to read the specified CSV file, checking the encoding, mimetype and delimiter. 
        Also, it treats all elements as strings.

        Args:
            filename (str): The name of the CSV file.
            version (bool): If true, show more information about the method.
    """
    dataframe = {}
    try:
        encoding, _ = mr_mime(filename) # (encoding, mimetype)
        separator = find_csv_delimiter(filename, encoding) # separator === delimiter
        with open(filename, encoding=encoding) as file_name:
            dataframe = pd.read_csv(file_name, sep=separator, dtype=str, skip_blank_lines=True)
        if verbose:
            print(f'INFO: Trying to open the file with encoding "{encoding}"')
        return dataframe
    except UnicodeDecodeError:
        with open(filename, encoding='unicode_escape') as file_name:
            dataframe = pd.read_csv(file_name, sep=separator, dtype=str, skip_blank_lines=True)
        if verbose:
            print('INFO: Trying to open the file with encoding "unicode_escape"')
        return dataframe
    except Exception as e:
        print(e)
    return pd.DataFrame(dataframe)
    
