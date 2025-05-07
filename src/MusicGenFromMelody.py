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
    
    def __init__ (self, output_dir, duration=8):
        os.environ["PATH"] += os.pathsep + '/opt/homebrew/bin/ffmpeg'
        print(shutil.which("ffmpeg"))  # if None, ffmpeg do not found
        self.output_dir = output_dir
        self.duration = duration
        
    
    def music_gen_from_melody (self, melody_path, description, idx):
        print(f"-------- Generating --------\nprompt: {description}\nmelody: {melody_path}\n")

        model = MusicGen.get_pretrained('melody')
        model.set_generation_params(duration=self.duration)

        melody, sr = torchaudio.load(melody_path)
        # generates using the melody from the given audio and the provided descriptions.
        wav = model.generate_with_chroma([description], melody, sr)

        # loudness normalization at -14 db LUFS.
        audio_path = os.path.join(self.output_dir, f"{idx}.wav")
        audio_write(f'{audio_path}', wav.cpu(), model.sample_rate, strategy="loudness")

