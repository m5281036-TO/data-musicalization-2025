"""
This class picks the user specified number of samples in data, then returns picked data samples as list
"""

import pandas as pd 

class RandomDataPicker:
    
    def __init__(self, loaded_data):
        self.loaded_data = loaded_data
        

    def check_duplicates(self, value_to_check, unique_values):
        if value_to_check in unique_values:
            return True
        else:
            return False
        
    
    def is_possible_to_pick_without_duplicates(self, num_random_picked, exclude_duplicate): 
        unique_value = self.loaded_data[exclude_duplicate].drop_duplicates()
        if len(unique_value) < 10:
            raise ValueError (f"Unique row is less than {num_random_picked}. Try changing dataset or try without 'exclude_dupliate' option")
    
        
    def get_random_data_samples(self, num_random_picked, exclude_duplicate=False):
        unique_values = [] # array to exclude duplicates
        
        if exclude_duplicate == False:
            picked_rows = self.loaded_data.sample(n=10)
            print(f"{num_random_picked} samples of data are randomly picked\n{picked_rows}")
            
        else: # when exlude_duplicates is specified
            picked_rows = pd.DataFrame(columns=self.loaded_data.columns) # generate empty data frame copying header info from loaded data
            while(len(picked_rows) < num_random_picked): # continues until picked_df has specified number of rows
                random_row = self.loaded_data.sample(n=1)
                unique_values = set(unique_values)
                
                # duplication check
                value_to_check = random_row.iloc[0, random_row.columns.get_loc(exclude_duplicate)]
                if self.check_duplicates(value_to_check, unique_values) == False:
                    unique_values.add(value_to_check)
                    picked_rows = pd.concat([picked_rows, pd.DataFrame(random_row)], ignore_index=True) # concatinate without header
            print(f"{num_random_picked} samples of data are randomly picked\n(picked values in element '{exclude_duplicate}' is unique (no duplication))\n{picked_rows}")    
                
        return picked_rows