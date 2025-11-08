from modules import Visualizer, CSVNaNReplacer, DataLoader, SafecastLoader, TimeSeriesPatternMiner, DataFrameSelector
import pandas as pd

def main():
    # source = "https://api.safecast.org/en-US/measurements.json?latitude=37.483&longitude=139.929&radius=10000&limit=500"
    # source = "https://u-aizu.ac.jp/~udayrage/datasets/transactionalDatabases/Transactional_T10I4D100K.csv"


    # ========================================
    # load files online or on local
    # ========================================
    # loader = DataLoader()
    # df = loader.load(source)

    
    # ========================================
    # example: load safecast timeseries data
    # ========================================
    sc_loader = SafecastLoader()
    # df = sc_loader.fetch_device_data(device_id=4824, date_from="2011-01-01", date_to="2025-10-01")
    df = pd.read_csv("./data/output/csv/safecast_data_user_4824.csv")
    
    # export to csv
    df_csv_filename = "./data/output/csv/safecast_data.csv"
    df.to_csv(df_csv_filename)
        
    print("DataFrame Loaded:")
    print(df.head())
    print(f"Shape: {df.shape}\n")
    
    
    # ========================================
    # let user to choose which 2 parameters (columns) are to be used
    # visualize selected dataframe
    # ========================================
    selector = DataFrameSelector()
    selected_df = selector.select_columns(df, timestamp="captured_at", col1="value")
    selected_df.to_csv("./data/output/csv/safecast_data_selected.csv")
    print(selected_df)
    print(f"Shape: {selected_df.shape}\n")
    
    
    # ========================================
    # pattern mining using Stumpy
    # ========================================
    miner = TimeSeriesPatternMiner(selected_df, time_col='captured_at', value_col='value')
    result = miner.pattern_miner(window_size=20, threshold=None, normalize=True, return_results=True)
    print(result)
    
    # visualizer = Visualizer(selected_df)
    # visualizer.plot_binned_histogram("value", "latitude")
    
        

if __name__ == "__main__":
    main()

