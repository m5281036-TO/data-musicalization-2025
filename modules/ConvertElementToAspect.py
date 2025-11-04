import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class ConvertElementToAspect:
    
    # valence -> [-100, 100], 10 interval (20 steps)
    VALENCE_MAX = 100
    VALENCE_MIN = -100
    VALENCE_INTERVAL = 10
    
    # arousal -> [0, 100], 5 interval (20 steps)
    AROUSAL_MAX = 100
    AROUSAL_MIN = 0
    AROUSAL_INTERVAL = 5
    
    BPM_MAX = 180
    BPM_MIN = 60


    def __init__ (self, data_all):
        self.data_all = data_all


    # ========================================
    # mathmatic utilities
    # ========================================
    
    # def get_zscores (self, data):
    #     """
    #     returns z score for each value
    #     """
    #     mean = np.mean(data)
    #     std_dev = np.std(data)
    #     zscores = [(x - mean) / std_dev for x in data]
    #     return zscores
    
    
    def round_with_interval (self, normalized_val, intervals):
        rounded_data = round(normalized_val /intervals) * intervals # round in intervals
        return rounded_data
    
    
    def get_normalized_value (self, val, val_max, val_min, new_max, new_min, intervals):
        normalized_val = (val - val_min) / (val_max - val_min) * (new_max - new_min) + new_min
        rounded_val = self.round_with_interval(normalized_val, intervals)
        return rounded_val
        
    
    # ========================================
    # converting values in each element to corresponding musical aspects
    # ========================================    
    # TODO: add more musical aspects
    
    def convert_element_to_valence(self, element_name, max_thresh, min_thresh, isInverted=False): 
        valence_array = []
        element_data = self.data_all[element_name]
        for val in element_data: # clip to maximum value
            if val >= max_thresh: 
                valence_array.append(self.VALENCE_MAX)
            elif val < min_thresh:
                valence_array.append(self.VALENCE_MIN)
            else:
                valence_array.append(self.get_normalized_value(val, max_thresh, min_thresh, self.VALENCE_MAX, self.VALENCE_MIN, self.VALENCE_INTERVAL))
        
        # inversion (default = False)
        if isInverted == True:
            valence_array = [val * (-1) for val in valence_array]
            print(f"'{element_name}' [{max_thresh}, {min_thresh}] is mapped to 'valence [0, 100]' (inverted)")
        else:
            print(f"'{element_name}' [{max_thresh}, {min_thresh}] is mapped to 'arousal [0, 100]'")
        
        return valence_array
    
    
    def convert_element_to_arousal(self, element_name, max_thresh, min_thresh, isInverted=False):
        arousal_array = []
        element_data = self.data_all[element_name]
        for val in element_data: # clip to maximum value
            if val >= max_thresh: 
                arousal_array.append(self.AROUSAL_MAX)
            elif val < min_thresh:
                arousal_array.append(self.AROUSAL_MIN)
            else:
                arousal_array.append(self.get_normalized_value(val, max_thresh, min_thresh, self.AROUSAL_MAX, self.AROUSAL_MIN, self.AROUSAL_INTERVAL))
        
        # inversion (default = False)
        if isInverted == True:
            arousal_array = [val * (-1) for val in arousal_array]
            print(f"'{element_name}' [{max_thresh}, {min_thresh}] is mapped to 'arousal [0, 100]' (inverted)")
        else:
            print(f"'{element_name}' [{max_thresh}, {min_thresh}] is mapped to 'arousal [0, 100]'")
        
        return arousal_array
    
    
    # ========================================
    # generate text-based prompt from converted values in musical aspect
    # ========================================
    
    def get_prompt_text (self, valence_array, arousal_array, music_genre):
        if len(valence_array) != len(arousal_array): # unmatch error handling
            raise ValueError("unmatch number of valence array and arousal array")

        num_prompt = len(valence_array)
        prompt_array = [f"{music_genre}, {valence_array[i]}% of valence, and {arousal_array[i]}% of arousal"for i in range(len(valence_array))]
        print(f"{num_prompt} prompt(s) is created: \n{prompt_array}")
        return prompt_array