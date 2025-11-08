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
import PAMI.extras.dbStats.TemporalDatabase as stats
import PAMI.extras.graph.plotLineGraphFromDictionary as plt


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
    run(csv_filepath: str) -> pd.DataFrame
        Loads JSON data from file or URL, converts to transactional format,
        and runs FP-Growth algorithm.
    """

    def __init__(self, min_support: float = 0.5):
        self.min_support = min_support

        

    def run(self, csv_filepath: str, file_separator='\t') -> pd.DataFrame:
        obj=stats.TemporalDatabase(csv_filepath, sep=file_separator)
        obj.run()
        
        #Printing each of the database statistics
        print(f'Database size : {obj.getDatabaseSize()}')
        print(f'Total number of items : {obj.getTotalNumberOfItems()}')
        print(f'Database sparsity : {obj.getSparsity()}')
        print(f'Minimum Transaction Size : {obj.getMinimumTransactionLength()}')
        print(f'Average Transaction Size : {obj.getAverageTransactionLength()}')
        print(f'Maximum Transaction Size : {obj.getMaximumTransactionLength()}')
        print(f'Standard Deviation Transaction Size : {obj.getStandardDeviationTransactionLength()}')
        print(f'Variance in Transaction Sizes : {obj.getVarianceTransactionLength()}')
        
        itemFrequencies = obj.getSortedListOfItemFrequencies()
        transactionLength = obj.getTransanctionalLengthDistribution()
        
        itemFrequencies = obj.getFrequenciesInRange()
        transactionLength = obj.getTransanctionalLengthDistribution()
        plt.plotLineGraphFromDictionary(itemFrequencies, end = 100, title = 'Items\' frequency graph', xlabel = 'No of items', ylabel= 'frequency')
        plt.plotLineGraphFromDictionary(transactionLength, end = 100, title = 'transaction distribution graph', xlabel = 'transaction length', ylabel = 'frequency')
        
