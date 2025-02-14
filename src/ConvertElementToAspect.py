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
    
    def get_zscores (self, data):
        """
        returns z score for each value
        """
        mean = np.mean(data)
        std_dev = np.std(data)
        zscores = [(x - mean) / std_dev for x in data]
        return zscores
    
    
    def get_normalized_values (self, data, new_max, new_min):
        now_max = max(data)
        now_min = min(data)
        normalized_data = [(value - now_min) / (now_max - now_min) * (new_max - new_min)  + new_min for value in data]
        return normalized_data
    
    
    def round_with_interval (self, normalized_data, intervals):
        rounded_data = [round(value /intervals) * intervals for value in normalized_data] # round in intervals
        return rounded_data
        
    
    # ========================================
    # converting values in each element to corresponding musical aspects
    # ========================================    
    # TODO: add more musical aspects
    
    def convert_element_to_valence(self, element_name):
        element_data = self.data_all[element_name]
        print(f"'{element_name}' is assigned to 'valence [-100, 100]'")
        element_zscores = self.get_zscores(element_data) # convert each value in data segment to zscore
        
        normalized_element = self.get_normalized_values(element_zscores, self.__class__.VALENCE_MAX, self.__class__.VALENCE_MIN) # normalize all z scores into [-100, 100]
        rounded_element = self.round_with_interval(normalized_element, self.__class__.VALENCE_INTERVAL) # fit all normalized values to intervals
        return rounded_element
    
    
    def convert_element_to_arousal(self, element_name):
        element_data = self.data_all[element_name]
        print(f"'{element_name}' is assigned to 'arousal [0, 100]'")
        element_zscores = self.get_zscores(element_data) # convert each value in data segment to zscore
        
        normalized_element = self.get_normalized_values(element_zscores, self.__class__.AROUSAL_MAX, self.__class__.AROUSAL_MIN) # normalize all z scores into [0, 100]
        rounded_element = self.round_with_interval(normalized_element, self.__class__.AROUSAL_INTERVAL) # fit all normalized values to intervals
        return rounded_element

    