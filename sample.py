from modules import Visualizer, TimestampConvertToDatetime, CreateChordsAndMelody, DataLoader, SafecastLoader, TimeSeriesPatternMiner, DataFrameSelector, ConvertElementToAspect, SunoMusicGenerator, ValenceArousalToEmotion
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
    # df = sc_loader.fetch_device_data(device_id=126, date_from="2011-01-01", date_to="2025-10-01")
    # or load from local file
    df_csv_filename = "./data/output/csv/safecast_data_device_126.csv"
    df = pd.read_csv(df_csv_filename)
    
    # TODO: dfのtimestamp列にある値をdatetime型に変換し、時系列順に並び替えて出力する
    # convert timestamp to datetime if needed
    # timestamp_converter = TimestampConvertToDatetime(df)
    # converted_df = timestamp_converter.timestamp_convert_to_datetime("captured_at").copy()

    # export to csv
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
        start_row=19, 
        end_row=26
        )
    selected_df.to_csv("./data/output/csv/safecast_data_selected.csv")
    print(selected_df)
    print(f"Selected dataframe shape: {selected_df.shape}\n")
    
    visualizer = Visualizer(selected_df)
    visualizer.plot_time_series_data(col_timestamp_index="captured_at", col_x_index="value", col_y_index="latitude")
    
    
    # ========================================
    # pattern mining using Stumpy
    # ========================================
    # miner = TimeSeriesPatternMiner(selected_df, time_col='captured_at', value_col='value')
    # miner.pattern_miner(window_size=10, threshold=None, normalize=True, return_results=True)
    
    
    # ========================================
    # convert values in rows to musical aspect (2 rows)
    # ========================================
    element_converter = ConvertElementToAspect(selected_df)

    # convert valence [-100, 100]
    valence_array = element_converter.convert_element_to_valence('value', min_thresh=15, max_thresh=20)
    # convert valence [0, 100]
    arousal_array = element_converter.convert_element_to_arousal('latitude', min_thresh=35, max_thresh=40)
    print(valence_array, arousal_array)

    e = ValenceArousalToEmotion(valence_array, arousal_array)
    emotion_array = e.convert_valencea_arousal_to_emotion()
    print(emotion_array)
    
    
    # ========================================
    # create chords and melody from specified valence-arousal coordinates
    # ========================================
    melody_generator = CreateChordsAndMelody()
    melody_dir_path = melody_generator.create_midi_and_wav(valence_array, arousal_array)
    
    
    # ========================================
    # connect SUNO API and generate music
    # ========================================    
    style = 'Electronic Music'
    upload_url_base = 'https://audio-eval-2025-05.web.app/input_melody/'
    upload_filenames = ["melody_1_val-100_aro90", "melody_2_val20_aro100", "melody_3_val-10_aro0", "melody_4_val100_aro0", "melody_5_val0_aro0"]

    # generate tasks
    suno_generator = SunoMusicGenerator()
    task_ids = []
    for idx, emotion_param in enumerate(emotion_array):
        upload_url = f"{upload_url_base}{upload_filenames[idx]}.mp3"
        task_ids.append(suno_generator.generate_music(emotion_param, style, upload_url))
        if idx == 4: # fail safe not to consume API resources
            break
    print(f"{len(task_ids)} task(s) processing: {task_ids}")
    # download generated tracks
    for idx, task_id in enumerate(task_ids):
        audio_url = suno_generator.poll_suno_task(task_id)
        filename = suno_generator.download_tracks(audio_url, f'{upload_filenames[idx]}')

if __name__ == "__main__":
    main()

