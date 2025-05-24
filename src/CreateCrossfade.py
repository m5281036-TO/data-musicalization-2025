import glob
import numpy as np
from pydub import AudioSegment
import os

class CreateCrossFade:
     
    def __init__ (self, wav_folder_path, fade_duration_ms=3000):
        self.wav_folder_path = wav_folder_path
        self.fade_duration_ms = fade_duration_ms
        
    def create_cross_fade (self):
        wav_files = sorted(glob.glob(os.path.join(self.wav_folder_path, "*.wav")))

        # initialize empty audio segment
        combined = AudioSegment.silent(duration=0)

        # crossfading
        for i, wav_file in enumerate(wav_files):
            print(wav_file)
            audio = AudioSegment.from_wav(wav_file)
            if i == 0:
                combined = audio
            else:
                combined = combined.append(audio, crossfade=self.fade_duration_ms)

        # set fade in and out
        combined = combined.fade_in(self.fade_duration_ms).fade_out(self.fade_duration_ms)

        # save to wav file
        combined.export(os.path.join(self.wav_folder_path, (f"crossfaded_{self.fade_duration_ms}ms.wav")), format="wav")
        # print(f"crossfaded wav saved to {os.path.join(self.wav_folder_path, f"crossfaded_{self.fade_duration_ms}ms.wav")}")
        