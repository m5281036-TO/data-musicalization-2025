from mido import Message, MidiFile, MidiTrack
import numpy as np
from scipy.io.wavfile import write
import random
import time

class CreateChordsAndMelody:
    
    BARS_TO_EACH_POINT = 4 # create 4 bar melodies for each data point
    MIN_LOUDNESS = 50 # set minimal loudness
    DEFAULT_SAMPLE_RATE = 44100
    
    def __init__(self, sample_rate=DEFAULT_SAMPLE_RATE):
        self.sample_rate = sample_rate
        self.activate1 = 0
        self.activate2 = 0


    def create_modeset(self):
        CHORD_LIST = np.array([[60,  64,  55,  59],
                [62,  65,  57,  60],
                [64,  55,  59,  62],
                [60,  65,  57,  64],
                [55,  59,  62,  65],
                [57,  60,  64,  55],
                [59,  62,  65,  57]])
    
        # MODESET = [idx, [chord], mode type]
        MODESET = np.zeros((4, CHORD_LIST.shape[1], CHORD_LIST.shape[0]))

        # Lydian mode
        MODESET[0, :, 0] = CHORD_LIST[3, :]
        MODESET[1, :, 0] = CHORD_LIST[6, :]
        MODESET[2, :, 0] = CHORD_LIST[0, :]
        MODESET[3, :, 0] = CHORD_LIST[3, :]

        # Ionian mode
        MODESET[0, :, 1] = CHORD_LIST[0, :]
        MODESET[1, :, 1] = CHORD_LIST[3, :]
        MODESET[2, :, 1] = CHORD_LIST[4, :]
        MODESET[3, :, 1] = CHORD_LIST[0, :]

        # Mixolydian mode
        MODESET[0, :, 2] = CHORD_LIST[4, :]
        MODESET[1, :, 2] = CHORD_LIST[0, :]
        MODESET[2, :, 2] = CHORD_LIST[1, :]
        MODESET[3, :, 2] = CHORD_LIST[4, :]

        # Dorian mode
        MODESET[0, :, 3] = CHORD_LIST[1, :]
        MODESET[1, :, 3] = CHORD_LIST[4, :]
        MODESET[2, :, 3] = CHORD_LIST[5, :]
        MODESET[3, :, 3] = CHORD_LIST[1, :]

        # Aeolian mode
        MODESET[0, :, 4] = CHORD_LIST[5, :]
        MODESET[1, :, 4] = CHORD_LIST[1, :]
        MODESET[2, :, 4] = CHORD_LIST[2, :]
        MODESET[3, :, 4] = CHORD_LIST[5, :]

        # Phrygian mode
        MODESET[0, :, 5] = CHORD_LIST[2, :]
        MODESET[1, :, 5] = CHORD_LIST[5, :]
        MODESET[2, :, 5] = CHORD_LIST[6, :]
        MODESET[3, :, 5] = CHORD_LIST[2, :]

        # Locrian mode
        MODESET[0, :, 6] = CHORD_LIST[6, :]
        MODESET[1, :, 6] = CHORD_LIST[2, :]
        MODESET[2, :, 6] = CHORD_LIST[3, :]
        MODESET[3, :, 6] = CHORD_LIST[6, :]
        print("modeset created")
        return MODESET


    def create_activation_and_brightness(self, roughness, voicing):
        # create roughness (activate1)
        self.activate1 = np.random.rand(8)
        self.activate1 = np.where(self.activate1 < roughness, 0, 1)

        # create roughness (activate2)
        self.activate2 = np.random.rand(8)
        self.activate2 = np.where(self.activate2 < roughness, 0, 1)

        self.bright = np.random.rand(6)
        self.bright_adjusted = []

        for val in self.bright:
            if voicing < 0.5:
                if val > voicing * 2:
                    self.bright_adjusted.append(-1)
                else:
                    self.bright_adjusted.append(0)
            else:
                if val < (voicing - 0.5) * 2:
                    self.bright_adjusted.append(1)
                else:
                    self.bright_adjusted.append(0)


    def create_midi(self, modeset, valence_array, arousal_array, filename='../data/output/chords.mid', tempo=500000):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        
        for idx in range(len(valence_array)):
            for seq in range(4):
                print(f"idx === {idx}, seq === {seq}")
                valence = valence_array[idx]
                arousal = arousal_array[idx]

                mode = 7 - round(valence * 6)
                roughness = 1 - arousal
                velocity = arousal
                voicing = valence
                loudness = round(arousal * 10) / 10 * 40 + 60

                activate1 = np.where(np.random.rand(8) < roughness, 0, 1)
                activate2 = np.where(np.random.rand(8) < roughness, 0, 1)

                bright = np.zeros(6)
                for i in range(6):
                    if voicing < 0.5:
                        bright[i] = -1 if np.random.rand() > voicing * 2 else 0
                    else:
                        bright[i] = 1 if np.random.rand() < (voicing - 0.5) * 2 else 0

                # --- generate notes for chords --- #
                for i in range(3):
                    note = int(modeset[seq, i + 1, mode] + bright[i] * 12)
                    vel = random.randint(self.MIN_LOUDNESS, int(loudness))
                    track.append(Message('note_on', channel=0, note=note, velocity=vel, time=0))

                # --- generate notes for bass --- #
                base_note = int(modeset[seq, 1, mode] - (12 if voicing > 0.5 else 24))
                vel = random.randint(self.MIN_LOUDNESS, int(loudness))
                track.append(Message('note_on', channel=0, note=base_note, velocity=vel, time=0))

                # --- generate notes for tone (melody) --- #
                for tone in range(8):
                    delay = int((0.3 - velocity * 0.15) * mid.ticks_per_beat)

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

            idx += 1

        mid.save(filename)



    def midi_to_wav(midi_path='./test_data/output/output.mid', wav_path='output.wav'):
        mid = MidiFile(midi_path)
        time = 0.0
        audio = np.zeros(int(mid.length * SAMPLE_RATE))

        for msg in mid.play():
            time += msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                duration = 0.5  # 固定長
                start_sample = int(time * SAMPLE_RATE)
                end_sample = int((time + duration) * SAMPLE_RATE)
                freq = 440.0 * 2 ** ((msg.note - 69) / 12.0)
                t = np.linspace(0, duration, end_sample - start_sample, False)
                wave = 0.2 * np.sin(2 * np.pi * freq * t)

                audio[start_sample:end_sample] += wave

        # 正規化
        audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
        write(wav_path, SAMPLE_RATE, audio)
        print(f"WAV saved as {wav_path}")



# main
valence_array = [0.2, 0.4, 1]
arousal_array = [0.2, 0.4, 1]
c = CreateChordsAndMelody()
modeset = c.create_modeset()
c.create_midi(modeset,valence_array,arousal_array)
# midi_to_wav()
