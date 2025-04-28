import torchaudio
from transformers import AutoProcessor, MusicgenForConditionalGeneration
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from IPython.display import Audio
import datetime
import scipy
import os


class MusicGenerater:
    
    """
    the methods in this class is implemented accoding to MusicGen.
    please refer to: 
    https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md
    for more information
    """
    MODEL_HEADER = 'facebook/musicgen-'
    
    def __init__ (self, model_size):
        self.model_name = self.MODEL_HEADER + model_size
    
    
    def set_model (self):
        model_name = self.model_name
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = MusicgenForConditionalGeneration.from_pretrained(model_name)
        self.sampling_rate = self.model.config.audio_encoder.sampling_rate
        print(f"MusicGen model is set to {model_name}")
        
        
    def save_wav_file(self, dir_path, valence, arousal, music_genre): 
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(f"folder {dir_path} is created")
        file_name = f"{music_genre}_val_{valence}_aro_{arousal}.wav"
        file_path_full = os.path.join(dir_path, file_name)
        scipy.io.wavfile.write(file_path_full, rate=self.sampling_rate, data=self.audio_values[0, 0].numpy())
        
        # check if the file is saved correctly
        if os.path.isfile(file_path_full) == False:
            raise ValueError(f"An error occured and fil is not saved to the directory{dir_path}")
        print(f"file saved to: {file_path_full}\n")

    
    def generate_music_from_prompt(self, prompt_array, val_aro_array, music_genre, is_save_to_files=False, dir_path=None):
        self.set_model()
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d-%H-%M-%S")
        
        for i, prompt in enumerate(prompt_array):
            print(f"Generating music {i+1}/{len(prompt_array)} ======================\nprompt: '{prompt}'")
            
            # generate audio from prompt
            inputs = self.processor(
                text=[prompt],
                padding=True,
                return_tensors="pt",
            )
            self.audio_values = self.model.generate(**inputs, max_new_tokens=256)
            
            # set audio playable in notebook
            Audio(self.audio_values[0].numpy(), rate=self.sampling_rate)
            
            # saving feature
            if is_save_to_files == True:
                if dir_path == None:
                    raise ValueError("argument 'save_to_file' is True but file path is not defined")
                
                dir_path_with_time = os.path.join(dir_path, formatted_time)
                valence = val_aro_array[0, i]
                arousal = val_aro_array[1, i]
                self.save_wav_file(dir_path_with_time, valence, arousal, music_genre)
                