from modules import Visualizer, TimestampConvertToDatetime, CreateChordsAndMelody, DataLoader, SafecastLoader, TimeSeriesPatternAnalyzer, DataFrameSelector, ConvertElementToAspect, RandomSegmentPicker, SunoMusicGenerator, ValenceArousalToEmotion, FilterCommonTimestampRange, TimeAlignedDataMerger
import pandas as pd

def main():
    # ========================================
    # load files online or on local
    # ========================================
    loader = DataLoader()
    source1 = "https://api.safecast.org/en-US/measurements.json?latitude=41.8535&longitude=12.4790&radius=1000&limit=500"
    source2 = "https://api.safecast.org/en-US/measurements.json?latitude=39.0287&longitude=-76.5834&radius=1000&limit=500"
    # df1 = loader.load(source1)
    # df2 = loader.load(source2)

    
    # ========================================
    # example: load safecast timeseries data
    # ========================================
    sc_loader = SafecastLoader(time_sort=False, timestamp_index_name='captured_at', page_limit=1000)
    # df2 = sc_loader.fetch_device_data(user_id=6, date_from="2015-10-24", date_to="2016-08-01")
    # df2.to_csv("./data/output/csv/safecast_user_6.csv")
    
    # or load from existing csv file
    # df = pd.read_csv("./data/output/csv/safecast_device_126.csv")
    
    # # or load from local file
    df1 = pd.read_csv("./data/output/csv/safecast_device_126.csv")
    df2 = pd.read_csv("./data/output/csv/safecast_user_6.csv")
    
    # # TODO: dfのtimestamp列にある値をdatetime型に変換し、時系列順に並び替えて出力する
    # # convert timestamp to datetime if needed
    # # timestamp_converter = TimestampConvertToDatetime(df)
    # # converted_df = timestamp_converter.timestamp_convert_to_datetime("captured_at").copy()

    # # export to csv
    # df1_filtered.to_csv(df1_csv_filename)
    # print("DataFrame Loaded:")
    # print(df1_filtered)
    # print(f"Shape: {df2_filtered.shape}\n")
    
    # df2_filtered.to_csv(df2_csv_filename)
    # print("DataFrame Loaded:")
    # print(df2_filtered)
    # print(f"Shape: {df2_filtered.shape}\n")
    
    # ========================================
    # Visualization
    # ========================================
    # filter only overlapped segment
    filter = FilterCommonTimestampRange(df1, df2)
    df1_filtered, df2_filtered = filter.filter_common_timestamp_range(col_timestamp_index1="captured_at", col_timestamp_index2="captured_at")
    
    visualizer = Visualizer(df1_filtered, df2_filtered)
    visualizer.plot_time_series(col_timestamp_index="captured_at", value_index1="value", value_index2="value")
    
    # merge 2 filtered dataframes
    time_merger = TimeAlignedDataMerger()
    df_merged = time_merger.merge(df1_filtered, "captured_at", df2_filtered, "captured_at")
    print(df_merged)
    
    visualizer = Visualizer(df1_filtered, df2_filtered)
    visualizer.plot_time_series(col_timestamp_index="captured_at", value_index1="value", value_index2="value")
    
    
    # # ========================================
    # # Run through pattern miner (stumpy)
    # # ========================================
    # analyzer = TimeSeriesPatternAnalyzer(df1_filtered, df2_filtered)

    # # Extract overlapping interval → resample
    # ts1, ts2 = analyzer.resample_and_align(
    #     col_timestamp="captured_at",
    #     col_value1="value",
    #     col_value2="value",
    #     freq="30S",
    #     method="interpolate"
    # )
    # # STUMPY cross matrix profile
    # window = 50
    # profile = analyzer.compute_cross_matrix_profile(ts1, ts2, window_size=window)

    # print(profile)
    
    # ========================================
    # convert values in rows to musical aspect (2 rows)
    # ========================================
    element_converter = ConvertElementToAspect(sampled_df)

    # convert valence [-100, 100]
    valence_array = element_converter.convert_element_to_valence('value', min_thresh=15, max_thresh=20)
    # convert valence [0, 100]
    arousal_array = element_converter.convert_element_to_arousal('precipitation', min_thresh=0, max_thresh=30)
    print(valence_array, arousal_array)

    e = ValenceArousalToEmotion(valence_array, arousal_array)
    emotion_array = e.convert_valencea_arousal_to_emotion()
    print(emotion_array)
    
    
    # ========================================
    # create chords and melody from specified valence-arousal coordinates
    # ========================================
    # melody_generator = CreateChordsAndMelody()
    # melody_dir_path = melody_generator.create_midi_and_wav(valence_array, arousal_array)
    
    # ========================================
    # connect SUNO API and generate music
    # ========================================    
    style = 'Electronic Music'
    upload_url_base = 'https://audio-eval-2025-05.web.app/input_melody/'
    upload_filenames = ["melody_1_val-100_aro0", "melody_2_val-100_aro65", "melody_3_val-20_aro65", "melody_4_val20_aro100", "melody_5_val100_aro100", "melody_6_val-20_aro100", "melody_7_val100_aro15"]

    # generate tasks
    suno_generator = SunoMusicGenerator()
    task_ids = []
    for idx, emotion_param in enumerate(emotion_array):
        upload_url = f"{upload_url_base}{upload_filenames[idx]}.mp3"
        task_ids.append(suno_generator.generate_music(emotion_param, style, upload_url))
        if idx == 10: # fail safe not to consume API resources
            break
    print(f"{len(task_ids)} task(s) processing: {task_ids}")
    # download generated tracks
    for idx, task_id in enumerate(task_ids):
        audio_url = suno_generator.poll_suno_task(task_id)
        downloaded_filename = suno_generator.download_tracks(audio_url, upload_filenames[idx])
        print(f"{downloaded_filename} downloaded")

if __name__ == "__main__":
    main()

