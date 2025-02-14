"""
This class loads data from user-specified csv file 
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd

# TODO: let user to choose data
class FileLoader: 

    def __init__(self, file_path):
        self.file_path = file_path


    def load_csv(self): 
        try:
            # check if the file exist
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"Error: The file at {self.file_path} does not exist.")
                
            # load file
            self.loaded_data = pd.read_csv(self.file_path)
            print(f"File loaded successfully: {self.file_path} ")
            self.size = loaded_data.shape # store size of data
            return self.loaded_data
            
        # error catch
        except FileNotFoundError as e: # file not found error
            print(e) 
        except pd.errors.ParserError as e:
            print(f"Error parsing the file: {e}")  # CSV analysis error
        except Exception as e:
            print(f"An unexpected error occurred: {e}")  # other error
        return None
            
    
    def get_elements(self):
        """
        This method checks if data is loaded then returns elements from header
        """
        if hasattr(self, 'loaded_data'): # check if data is loaded in 'load_csv' method
            elements = self.loaded_data.columns.tolist() # get elements in header and stores in list
            return elements
        else:
            raise ValueError("CSV file not loaded. Please load the CSV file first.")
        