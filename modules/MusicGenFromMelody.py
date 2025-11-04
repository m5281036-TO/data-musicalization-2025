import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import shutil
import os


class MusicGenFromMelody:
    """
    This code is from the following reference: 
    https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md
    
    """
    
    def __init__ (self, input_dir, output_dir, duration=8):
        os.environ["PATH"] += os.pathsep + '/opt/homebrew/bin/ffmpeg'
        if shutil.which("ffmpeg")  == None: # if None, ffmpeg do not found
            raise ValueError("ffmpeg does not installed or path is not enabled")
        
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        self.model = MusicGen.get_pretrained('melody')
        self.model.set_generation_params(duration=duration)
        
    
    def music_gen_from_melody (self, melody_path, description, idx):        
        print(f"-------- Generating --------\nprompt: {description}\nmelody: {melody_path}\n") 
        
        melody, sr = torchaudio.load(melody_path)
        # generates using the melody from the given audio and the provided descriptions.
        print("\nmodel created, generating audio...")
        wav = self.model.generate_with_chroma([description], melody, sr)
        
        # set wav dimension
        if wav.dim() == 3 and wav.size(0) == 1:
            wav = wav.squeeze(0)  # [1, C, T] → [C, T]
        elif wav.dim() > 2:
            raise ValueError(f"Unexpected wav shape: {wav.shape}")
        print("wav dimension ok")
        
        # loudness normalization at -14 db LUFS.
        output_audio_name = os.path.splitext(os.path.basename(melody_path))[0]
        output_audio_path = os.path.join(self.output_dir, f"{output_audio_name}.wav")
        audio_write(f'{output_audio_path}', wav.cpu(), self.model.sample_rate, strategy="loudness")
        print(f"MusicGen output file saved: {output_audio_path}")
        
        