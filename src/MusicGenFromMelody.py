import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write


class MusicGenFromMelody:
    """
    This code is from the following reference: 
    https://github.com/facebookresearch/audiocraft/blob/main/docs/MUSICGEN.md
    
    """
    
    def __init__ (self, melody_path, duration):
        self.melody_path = melody_path
        self.duration = duration
        
    
    def music_gen_from_melody (self, prompt_array):
        print(f"Generating melody from prompt of {len(prompt_array)}")
        model = MusicGen.get_pretrained('facebook/musicgen-melody')
        model.set_generation_params(duration=self.duration)  # set duration
        wav = model.generate(prompt_array)  # generate from discrption

        melody, sr = torchaudio.load(self.melody_path)
        # generates using the melody from the given audio and the provided descriptions.
        wav = model.generate_with_chroma(prompt_array, melody[None].expand(3, -1, -1), sr)

        for idx, one_wav in enumerate(wav):
            # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
            audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)
            