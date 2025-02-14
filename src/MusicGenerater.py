import torchaudio
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

class MusicGenerater:
    
    def __init__ (self, prompt):
        self.prompt = prompt
    
    def generate_music_from_prompt(self):
        model = MusicGen.get_pretrained('facebook/musicgen-small')
        model.set_generation_params(duration=15)  # generate 8 seconds.
        output_wav = model.generate(self.prompt)
        
        # output_wav = model.generate_unconditional(4)    # generates 4 audio samples

        # melody, sr = torchaudio.load('./assets/bach.mp3')
        # # generates using the melody from the given audio and the provided descriptions.
        # wav = model.generate_with_chroma(descriptions, melody[None].expand(3, -1, -1), sr)

        # for idx, one_wav in enumerate(wav):
        #     # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        #     audio_write(f'{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", loudness_compressor=True)