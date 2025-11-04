"""
pattern_mining.py
-----------------
Performs frequent pattern mining directly from a JSON file (local or remote)
using the PAMI library (FP-Growth algorithm).

Example
-------
>>> from pattern_mining import PatternMiner
>>> miner = PatternMiner(min_support=0.3)
>>> patterns = miner.run("https://example.com/data.json")
>>> print(patterns.head())
"""

import pandas as pd
import requests
import tempfile
import json
import io
import os
from PAMI.frequentPattern.basic import FPGrowth as fpg


class PatternMiner:
    """
    PatternMiner Class
    ------------------
    Executes frequent pattern mining using the PAMI library (FP-Growth algorithm)
    on data loaded directly from a JSON file.

    Parameters
    ----------
    min_support : float, default=0.5
        Minimum support threshold for pattern mining (0.0–1.0).

    Methods
    -------
    run(source: str) -> pd.DataFrame
        Loads JSON data from file or URL, converts to transactional format,
        and runs FP-Growth algorithm.
    """

    def __init__(self, min_support: float = 0.5):
        self.min_support = min_support
        

    def run(self, source: str) -> pd.DataFrame:
        sep = "\t"
        minSup = 0.005
        obj = fpg.FPGrowth(source, minSup, sep)
        obj.mine()
        obj.printResults()
        obj.save("../data/output/csv/frequentPatterns.csv")
        
        frequentPatternsDataFrame = obj.getPatternsAsDataFrame()
        return frequentPatternsDataFrame
        