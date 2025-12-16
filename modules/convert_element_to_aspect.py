import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class ConvertElementToAspect:
    """
    ConvertElementToAspect Class
    ----------------------------
    This class converts numerical data (e.g., from sensor or measurement data)
    into corresponding musical emotion parameters such as *valence* and *arousal*.

    It provides normalization, rounding with defined intervals, and conversion
    methods to map arbitrary numeric inputs into structured scales suitable for
    emotional or musical representation.

    Attributes
    ----------
    VALENCE_MAX : int
        Maximum value of valence (emotional positivity), fixed at 100.
    VALENCE_MIN : int
        Minimum value of valence (emotional negativity), fixed at -100.
    VALENCE_INTERVAL : int
        Interval for rounding valence values, fixed at 10.
    AROUSAL_MAX : int
        Maximum value of arousal (emotional activation level), fixed at 100.
    AROUSAL_MIN : int
        Minimum value of arousal, fixed at 0.
    AROUSAL_INTERVAL : int
        Interval for rounding arousal values, fixed at 5.
    BPM_MAX : int
        Maximum BPM value for normalization (not currently used).
    BPM_MIN : int
        Minimum BPM value for normalization (not currently used).
    """

    # Define mapping scales for valence and arousal
    VALENCE_MAX = 100
    VALENCE_MIN = -100
    VALENCE_INTERVAL = 10

    AROUSAL_MAX = 100
    AROUSAL_MIN = 0
    AROUSAL_INTERVAL = 5

    BPM_MAX = 180
    BPM_MIN = 60

    def __init__(self, data_all):
        """
        Initialize the converter with an input dataset.

        Parameters
        ----------
        data_all : pd.DataFrame
            Input dataset containing numerical elements to be converted.
        """
        self.data_all = data_all

    def round_with_interval(self, normalized_val, intervals):
        """
        Round a normalized value to the nearest specified interval.

        Parameters
        ----------
        normalized_val : float
            The normalized numerical value.
        intervals : float
            Interval step used for rounding.

        Returns
        -------
        float
            Rounded value adjusted to the specified interval.
        """
        rounded_data = round(normalized_val / intervals) * intervals
        return rounded_data

    def get_normalized_value(self, val, val_max, val_min, new_max, new_min, intervals):
        """
        Normalize a value within a defined range and map it to a new range.

        Parameters
        ----------
        val : float
            Original value to normalize.
        val_max : float
            Maximum value of the original scale.
        val_min : float
            Minimum value of the original scale.
        new_max : float
            Target maximum value of the new scale.
        new_min : float
            Target minimum value of the new scale.
        intervals : float
            Interval used for rounding.

        Returns
        -------
        float
            Normalized and rounded value within the new range.
        """
        normalized_val = (val - val_min) / (val_max - val_min) * (new_max - new_min) + new_min
        rounded_val = self.round_with_interval(normalized_val, intervals)
        return rounded_val

    # ========================================
    # Conversion of elements to emotional aspects
    # ========================================

    def convert_element_to_valence(self, element_name, min_thresh, max_thresh, isInverted=False):
        """
        Convert values of a specified element into valence values
        mapped within [-100, 100].

        Parameters
        ----------
        element_name : str
            Name of the column to convert.
        max_thresh : float
            Maximum threshold value of the element.
        min_thresh : float
            Minimum threshold value of the element.
        isInverted : bool, optional
            Whether to invert the valence mapping (default: False).

        Returns
        -------
        list
            List of mapped valence values.
        """
        valence_array = []
        element_data = self.data_all[element_name]

        for val in element_data:
            if val >= max_thresh:
                valence_array.append(self.VALENCE_MAX)
            elif val < min_thresh:
                valence_array.append(self.VALENCE_MIN)
            else:
                valence_array.append(
                    self.get_normalized_value(val, max_thresh, min_thresh,
                                              self.VALENCE_MAX, self.VALENCE_MIN,
                                              self.VALENCE_INTERVAL)
                )

        if isInverted:
            valence_array = [val * (-1) for val in valence_array]
            print(f"'{element_name}' [{min_thresh}, {max_thresh}] is mapped to 'valence [-100, 100]' (inverted)")
        else:
            print(f"'{element_name}' [{min_thresh}, {max_thresh}] is mapped to 'valence [-100, 100]'")

        return valence_array

    def convert_element_to_arousal(self, element_name, min_thresh, max_thresh, isInverted=False):
        """
        Convert values of a specified element into arousal values
        mapped within [0, 100].

        Parameters
        ----------
        element_name : str
            Name of the column to convert.
        max_thresh : float
            Maximum threshold value of the element.
        min_thresh : float
            Minimum threshold value of the element.
        isInverted : bool, optional
            Whether to invert the arousal mapping (default: False).

        Returns
        -------
        list
            List of mapped arousal values.
        """
        arousal_array = []
        element_data = self.data_all[element_name]

        for val in element_data:
            if val >= max_thresh:
                arousal_array.append(self.AROUSAL_MAX)
            elif val < min_thresh:
                arousal_array.append(self.AROUSAL_MIN)
            else:
                arousal_array.append(
                    self.get_normalized_value(val, max_thresh, min_thresh,
                                              self.AROUSAL_MAX, self.AROUSAL_MIN,
                                              self.AROUSAL_INTERVAL)
                )

        if isInverted:
            arousal_array = [val * (-1) for val in arousal_array]
            print(f"'{element_name}' [{max_thresh}, {min_thresh}] is mapped to 'arousal [0, 100]' (inverted)")
        else:
            print(f"'{element_name}' [{max_thresh}, {min_thresh}] is mapped to 'arousal [0, 100]'")

        return arousal_array

    # ========================================
    # Generate text-based prompts for each converted value pair
    # ========================================

    def get_prompt_text(self, valence_array, arousal_array, music_genre):
        """
        Generate descriptive textual prompts combining musical genre and emotion mapping.

        Parameters
        ----------
        valence_array : list
            Sequence of valence values.
        arousal_array : list
            Sequence of arousal values.
        music_genre : str
            Target music genre to include in the description.

        Returns
        -------
        list
            List of generated descriptive prompt strings.
        """
        if len(valence_array) != len(arousal_array):
            raise ValueError("Mismatch between valence and arousal array lengths.")

        prompt_array = [
            f"{music_genre}, {valence_array[i]}% of valence, and {arousal_array[i]}% of arousal"
            for i in range(len(valence_array))
        ]
        print(f"{len(prompt_array)} prompt(s) created: \n{prompt_array}")
        return prompt_array
