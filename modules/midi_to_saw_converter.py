import os
import numpy as np
from mido import MidiFile
from scipy.io.wavfile import write

class MidiToSawWavConverter:
    def __init__(
        self,
        input_folder: str,
        output_folder: str,
        sample_rate: int = 44100,
        decay: float = 0.2,
        release: float = 0.3
    ):
        self.input_folder = input_folder
        self.output_folder = output_folder
        self.sample_rate = sample_rate
        self.decay = decay
        self.release = release

        os.makedirs(self.output_folder, exist_ok=True)

    def _saw_wave(self, frequency, duration):
        t = np.linspace(0, duration, int(self.sample_rate * duration), endpoint=False)
        return 2 * (t * frequency - np.floor(0.5 + t * frequency))

    def _apply_envelope(self, signal):
        length = len(signal)
        decay_samples = int(self.decay * self.sample_rate)
        release_samples = int(self.release * self.sample_rate)

        envelope = np.ones(length, dtype=np.float32)

        # Decay phase
        if decay_samples > 0 and decay_samples < length:
            decay_curve = np.linspace(1.0, 0.8, decay_samples)
            envelope[:decay_samples] = decay_curve

        # Release phase
        if release_samples > 0:
            start = max(0, length - release_samples)
            release_curve = np.linspace(0.8, 0.0, length - start)
            envelope[start:] = release_curve

        return signal * envelope

    def _note_to_freq(self, midi_note):
        return 440.0 * (2 ** ((midi_note - 69) / 12))

    def _render_midi(self, midi_path):
        midi = MidiFile(midi_path)
        track_audio = np.zeros(1, dtype=np.float32)
        current_time = 0.0

        for msg in midi:
            current_time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                freq = self._note_to_freq(msg.note)

                tone_duration = 0.5 + self.release
                raw_tone = self._saw_wave(freq, tone_duration)
                tone = self._apply_envelope(raw_tone)

                start = int(current_time * self.sample_rate)

                if start + len(tone) > len(track_audio):
                    track_audio = np.pad(track_audio, (0, start + len(tone) - len(track_audio)))

                track_audio[start:start+len(tone)] += tone.astype(np.float32)

        if np.max(np.abs(track_audio)) > 0:
            track_audio = track_audio / np.max(np.abs(track_audio)) * 0.9

        return track_audio

    def convert_all(self):
        for file in os.listdir(self.input_folder):
            if file.lower().endswith(".mid") or file.lower().endswith(".midi"):
                midi_path = os.path.join(self.input_folder, file)
                audio = self._render_midi(midi_path)
                wav_name = os.path.splitext(file)[0] + ".wav"
                wav_path = os.path.join(self.output_folder, wav_name)
                write(wav_path, self.sample_rate, audio.astype(np.float32))


if __name__ == "__main__":
    m = MidiToSawWavConverter(input_folder='./data/output/generated_melody/20251212_163639/', output_folder = './data/output/generated_melody/20251212_163639/saw/')
    m.convert_all()