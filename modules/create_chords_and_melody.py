"""
Reference:
Ehrlich, S. K., Agres, K. R., Guan, C., & Cheng, G. (2019). 
A closed-loop, music-based brain-computer interface for emotion mediation. 
PloS One, 14(3), e0213516. 
URL/DOI: https://doi.org/10.1371/journal.pone.0213516
"""

from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
import numpy as np
from scipy.io.wavfile import write
import os
import random
import time


class CreateChordsAndMelody:
    """
    CreateChordsAndMelody Class
    ---------------------------
    Converts valence and arousal values into musical sequences (chords and melodies).
    Generates MIDI files and optional WAV audio for each data point.

    Attributes
    ----------
    BARS_TO_EACH_POINT : int
        Number of bars generated for each valence-arousal data point.
    MIN_LOUDNESS : int
        Minimum note velocity for MIDI events.
    BASE_BPM : int
        Base tempo for the generated music (fixed).
    sample_rate : int
        Audio sample rate for WAV file generation.
    output_dir : str
        Directory path to save MIDI and WAV files.
    """

    BARS_TO_EACH_POINT = 4
    MIN_LOUDNESS = 50
    BASE_BPM = 60

    def __init__(self, file_save_path: str = "./data/output/generated_melody/", sample_rate: int = 44100):
        """
        Initialize the music generator.

        Parameters
        ----------
        file_save_path : str
            Base directory where generated MIDI/WAV files will be stored.
        sample_rate : int
            Audio sample rate for WAV files (default: 44100 Hz).
        """
        self.sample_rate = sample_rate
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.output_dir = os.path.join(file_save_path, timestamp)


    def create_midi_and_wav(self, valence, arousal, idx) -> str:
        """
        Generate MIDI sequences and WAV audio from valence and arousal arrays.

        Parameters
        ----------
        valence_array : list or np.ndarray
            Array of valence values (range [-100, 100]).
        arousal_array : list or np.ndarray
            Array of arousal values (range [0, 100]).

        Notes
        -----
        Each data point produces a 4-bar musical sequence.
        Music features such as mode, chord roughness, voicing, and loudness
        are influenced by normalized valence and arousal values.
        """

        def create_modeset():
            """
            Create a predefined set of musical modes and associated chord structures.

            Returns
            -------
            np.ndarray
                A 3D array containing chord notes for multiple modes.
            """
            CHORD_LIST = np.array([
                [60, 64, 55, 59],
                [62, 65, 57, 60],
                [64, 55, 59, 62],
                [60, 65, 57, 64],
                [55, 59, 62, 65],
                [57, 60, 64, 55],
                [59, 62, 65, 57]
            ])

            MODESET = np.zeros((4, CHORD_LIST.shape[1], CHORD_LIST.shape[0]))

            # Lydian mode: Dreamy, ethereal
            MODESET[0, :, 0] = CHORD_LIST[3, :]
            MODESET[1, :, 0] = CHORD_LIST[6, :]
            MODESET[2, :, 0] = CHORD_LIST[0, :]
            MODESET[3, :, 0] = CHORD_LIST[3, :]

            # Ionian mode: Bright, happy
            MODESET[0, :, 1] = CHORD_LIST[0, :]
            MODESET[1, :, 1] = CHORD_LIST[3, :]
            MODESET[2, :, 1] = CHORD_LIST[4, :]
            MODESET[3, :, 1] = CHORD_LIST[0, :]

            # Mixolydian mode: Bold, bluesy
            MODESET[0, :, 2] = CHORD_LIST[4, :]
            MODESET[1, :, 2] = CHORD_LIST[0, :]
            MODESET[2, :, 2] = CHORD_LIST[1, :]
            MODESET[3, :, 2] = CHORD_LIST[4, :]

            # Dorian mode: Cool, soulful
            MODESET[0, :, 3] = CHORD_LIST[1, :]
            MODESET[1, :, 3] = CHORD_LIST[4, :]
            MODESET[2, :, 3] = CHORD_LIST[5, :]
            MODESET[3, :, 3] = CHORD_LIST[1, :]

            # Aeolian mode: Melancholic, reflective
            MODESET[0, :, 4] = CHORD_LIST[5, :]
            MODESET[1, :, 4] = CHORD_LIST[1, :]
            MODESET[2, :, 4] = CHORD_LIST[2, :]
            MODESET[3, :, 4] = CHORD_LIST[5, :]

            # Phrygian mode: Dark, mysterious
            MODESET[0, :, 5] = CHORD_LIST[2, :]
            MODESET[1, :, 5] = CHORD_LIST[5, :]
            MODESET[2, :, 5] = CHORD_LIST[6, :]
            MODESET[3, :, 5] = CHORD_LIST[2, :]

            # Locrian mode: Dissonant, eerie
            MODESET[0, :, 6] = CHORD_LIST[6, :]
            MODESET[1, :, 6] = CHORD_LIST[2, :]
            MODESET[2, :, 6] = CHORD_LIST[3, :]
            MODESET[3, :, 6] = CHORD_LIST[6, :]

            print("modeset created")
            return MODESET

        modeset = create_modeset()

        # Generate MIDI and WAV for each valence-arousal data point
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)

        # Set fixed tempo
        tempo = bpm2tempo(self.BASE_BPM)
        track.append(MetaMessage('set_tempo', tempo=tempo, time=0))

        # Normalize valence and arousal to [0, 1]
        valence_norm = (valence + 100) / 200
        arousal_norm = max(arousal / 100, 0.1)

        # Determine musical mode and other musical parameters
        mode = 6 - round(valence_norm * 6)
        roughness = 1 - arousal_norm
        velocity = arousal_norm
        voicing = valence_norm
        loudness = round(arousal_norm * 10) / 10 * 40 + 60

        # Generate 4-bar loop per data point
        for seq in range(self.BARS_TO_EACH_POINT):
            activate1 = np.where(np.random.rand(8) < roughness, 0, 1)
            activate2 = np.where(np.random.rand(8) < roughness, 0, 1)
            bright = np.zeros(6)
            for i in range(6):
                if voicing < 0.5:
                    bright[i] = -1 if np.random.rand() > voicing * 2 else 0
                else:
                    bright[i] = 1 if np.random.rand() < (voicing - 0.5) * 2 else 0

            # --- Generate chord notes --- #
            for i in range(3):
                note = int(modeset[seq, i + 1, mode] + bright[i] * 12)
                vel = random.randint(self.MIN_LOUDNESS, int(loudness))
                track.append(Message('note_on', channel=0, note=note, velocity=vel, time=0))

            # --- Generate bass notes --- #
            base_note = int(modeset[seq, 1, mode] - (12 if voicing > 0.5 else 24))
            vel = random.randint(self.MIN_LOUDNESS, int(loudness))
            track.append(Message('note_on', channel=0, note=base_note, velocity=vel, time=0))

            # --- Generate melody notes --- #
            for tone in range(8):
                delay = int((0.3 - velocity * 0.15) * mid.ticks_per_beat * 2)

                if activate1[tone] == 1:
                    note = int(modeset[seq, 1, mode] + bright[4] * 12)
                    vel = random.randint(self.MIN_LOUDNESS, int(loudness))
                    track.append(Message('note_on', channel=0, note=note, velocity=vel, time=0))
                    track.append(Message('note_off', channel=0, note=note, velocity=vel, time=delay))

                if activate2[tone] == 1:
                    idx2 = np.random.randint(2, 4)
                    note = int(modeset[seq, idx2, mode] + bright[5] * 12)
                    vel = random.randint(self.MIN_LOUDNESS, int(loudness))
                    track.append(Message('note_on', channel=0, note=note, velocity=vel, time=0))
                    track.append(Message('note_off', channel=0, note=note, velocity=vel, time=delay))

            # --- Save MIDI file --- #
            os.makedirs(self.output_dir, exist_ok=True)
            file_name = f"melody_val{valence}_aro{arousal}.mid"
            midi_path = os.path.join(self.output_dir, file_name)
            mid.save(midi_path)
            print(f"MIDI file saved: {midi_path}")
        return self.output_dir
    
    # --- Convert MIDI to WAV --- #
    def midi_to_wav(self, midi_path, valence, arousal, idx):
        """
        Convert a MIDI file into a WAV file using simple sine wave synthesis.

        Parameters
        ----------
        midi_path : str
            Path to the MIDI file to convert.
        """
        mid = MidiFile(midi_path)
        time_accum = 0.0
        audio = np.zeros(int(mid.length * self.sample_rate))

        for msg in mid.play():
            time_accum += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                duration = 0.5
                start_sample = int(time_accum * self.sample_rate)
                end_sample = int((time_accum + duration) * self.sample_rate)
                if end_sample > len(audio):
                    end_sample = len(audio)
                wave_duration = end_sample - start_sample
                t = np.linspace(0, duration, wave_duration, False)
                freq = 440.0 * 2 ** ((msg.note - 69) / 12.0)
                wave = 0.2 * np.sin(2 * np.pi * freq * t)
                if len(wave) < wave_duration:
                    wave = np.pad(wave, (0, wave_duration - len(wave)))
                audio[start_sample:end_sample] += wave

        # Normalize and save
        audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
        wave_path = os.path.join(
            self.output_dir,
            f"melody_val{valence}_aro{arousal}.wav"
        )
        write(wave_path, self.sample_rate, audio)
        print(f"WAV file saved as {wave_path}")



if __name__ == "__main__":
    valence_array = [-100, -80, -60, -40, -20, 0, 20, 40, 60, 80, 100]
    arousal_array = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    c = CreateChordsAndMelody()
    idx = 1
    for v in range(len(valence_array)):
        for a in range(len(arousal_array)):
            c.create_midi_and_wav(valence_array[v], arousal_array[a], idx)
            idx += 1
    