from modules import Visualizer, DataLoader, SafecastLoader, TimeSeriesPatternMiner, DataFrameSelector, ConvertElementToAspect, SunoMusicGenerator
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
    selected_df = selector.select_columns(
        df, 
        timestamp="captured_at", 
        col1_index="value", 
        col2_index="latitude",
        start_row=20, 
        end_row=30
        )
    selected_df.to_csv("./data/output/csv/safecast_data_selected.csv")
    print(selected_df)
    print(f"Shape: {selected_df.shape}\n")
    
    visualizer = Visualizer(selected_df)
    visualizer.plot_time_series_data(col_timestamp_index="captured_at", col_x_index="value", col_y_index="latitude")
    
    
    # ========================================
    # pattern mining using Stumpy
    # ========================================
    # miner = TimeSeriesPatternMiner(selected_df, time_col='captured_at', value_col='value')
    # result = miner.pattern_miner(window_size=20, threshold=None, normalize=True, return_results=True)
    # print(result)
    
    
    # ========================================
    # convert values in rows to musical aspect (2 rows)
    # ========================================
    element_converter = ConvertElementToAspect(selected_df)

    # convert valence [-100, 100]
    valence_array = element_converter.convert_element_to_valence('value', min_thresh=26, max_thresh=40)
    # convert valence [0, 100]
    arousal_array = element_converter.convert_element_to_arousal('latitude', min_thresh=35, max_thresh=40)
    print(valence_array, arousal_array)

    # e = ValenceArousalToEmotion(valence_array, arousal_array)
    # emotion_array = e.convert_valencea_arousal_to_emotion()
    
    
    # ========================================
    # map normalized value to musical aspect (valence-arousal emootion)
    # ========================================
    
    pass
    generater = SunoMusicGenerator()
    generater
    
    
    
    # ========================================
    # connect SUNO API and generate music
    # ========================================
    
    
    
    
        

if __name__ == "__main__":
    main()

