import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


"""
This class is to diplay histograms from user specified data segment.
"""
class DisplayHistogram:
    def __init__(self, data_to_be_displayed):
        self.data = data_to_be_displayed


    def display(self):
        
        data_list = {
            'Temperature': self.data['temperature'],
            'Precipitation': self.data['precipitation'],
            'Sunlight': self.data['sunlight']
        }

        for key in data_list:
            indices = np.arange(1, len(data_list[key])+1) # make indices for display
            plt.figure(figsize=(6, 3))
            plt.bar(indices, data_list[key])
            plt.title(key)
            plt.ylabel('Days')
            plt.ylabel(key)
            plt.show()

            # Display histogram
            plt.hist(data_list[key], bins=40, facecolor='orangered', edgecolor='black')
            plt.title('Histogram of ' + key)
            plt.xlabel(key)
            plt.ylabel('Frequency')
            plt.show()
            