from modules import Visualizer, TimestampConvertToDatetime, CreateChordsAndMelody, DataLoader, SafecastLoader, TimeSeriesPatternAnalyzer, DataFrameSelector, ConvertElementToAspect, RandomSegmentPicker, SunoMusicGenerator, ValenceArousalToEmotion, FilterCommonTimestampRange, TimeAlignedDataMerger, CrossfadeAudioFiles
import pandas as pd
import time

def main():
    SYSTEM_DATE = time.strftime("%Y_%m%d") # used to generate directory timestamp-based path
    print(SYSTEM_DATE)
    
    NUM_SEGMENT_IN_SECTION = 7
    
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
    df_merged.to_csv("./data/output/csv/df_merged.csv")
    print(df_merged)
    
    # ========================================
    # pick random continous segments
    # ========================================
    picker = RandomSegmentPicker(df_merged, num_rows=NUM_SEGMENT_IN_SECTION)
    
    for idx in range(3): 
        df_random_7 = picker.pick_random_segment(isNormalized=True)
        df_random_7.to_csv(f"./data/cache/df_random_7_{idx+1}.csv")
        print(df_random_7)
        visualizer = Visualizer(df_random_7, df_random_7)
        visualizer.plot_time_series(
            col_timestamp_index="captured_at", 
            value_index1="value1", 
            value_index2="value2", 
            isSave=True, 
            output_dir=f"./data/cache/", 
            filename=f"df_random_7_{idx+1}.png"
            )
    
    
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
    valence_list = []
    arousal_list = []
    emotion_list = []
    for idx in range(3):
        random_segment_path = f"./data/cache/1215_05/df_random_7_{idx+1}.csv"
        df_random_7 = pd.read_csv(random_segment_path)
        element_converter = ConvertElementToAspect(df_random_7)

        # convert valence [-100, 100]
        valence_list.append(element_converter.convert_element_to_valence('value1', min_thresh=df_random_7["value1"].min(), max_thresh=df_random_7["value1"].max()))
        # convert valence [0, 100]
        arousal_list.append(element_converter.convert_element_to_arousal('value2', min_thresh=df_random_7["value2"].min(), max_thresh=df_random_7["value2"].max()))
            
    print(f"\nvalence_list: {valence_list}\n arousal_list: {arousal_list}")
    
    e = ValenceArousalToEmotion(valence_list, arousal_list)
    emotion_list = e.convert_valence_arousal_to_emotion()

    print(emotion_list)
    
    
    # ========================================
    # create chords and melody from specified valence-arousal coordinates
    # ========================================
    # melody_generator = CreateChordsAndMelody()
    # melody_dir_path = melody_generator.create_midi_and_wav(valence_array, arousal_array)
    
    # ========================================
    # connect SUNO API and generate music
    # ======================================== 
    style = 'Electronic Music'
    suno_generator = SunoMusicGenerator(style=style)
    upload_url_base = 'https://audio-eval-2025-05.web.app/experiment_stimuli_1212/'
    task_ids = []
    upload_filenames = []

    for idx_row in range(len(emotion_list)):
        for idx_col in range(len(emotion_list[0])):
            upload_filename = f"melody_val{valence_list[idx_row][idx_col]}_aro{arousal_list[idx_row][idx_col]}.wav"
            upload_filenames.append(upload_filename)
            text_prompt = emotion_list[idx_row][idx_col]
            upload_url = f"{upload_url_base}{upload_filename}"
            print(upload_url, text_prompt)
            
            # create tasks
            task_ids.append(suno_generator.generate_music(text_prompt, upload_url))
            time.sleep(0.8) # in order to avoid API rate limitation
        
        print(idx)

    
    # actually download tracks when finished
    for idx, task_id in enumerate(task_ids):
        audio_url = suno_generator.poll_suno_task(task_id, interval=30)
        downloaded_filename = suno_generator.download_tracks(audio_url, download_filename=f"{idx+1}_{upload_filenames[idx]}")
        print(f"{downloaded_filename} downloaded")


if __name__ == "__main__":
    main()

