from mido import Message, MidiFile, MidiTrack, MetaMessage ,bpm2tempo
import numpy as np
from scipy.io.wavfile import write
import os
import random
import time


class CreateChordsAndMelody:
    
    BARS_TO_EACH_POINT = 4 # create 4 bar melodies for each data point
    MIN_LOUDNESS = 50 # set minimal loudness
    BASE_BPM = 60 # the tempt of music is not controlled based on the value in valence/arousal
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        # for saving files
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.output_dir = os.path.join(f"../data/output", timestamp)


    def create_midi_and_wav(self, valence_array, arousal_array):
        def create_modeset():
            CHORD_LIST = np.array([[60,  64,  55,  59],
                    [62,  65,  57,  60],
                    [64,  55,  59,  62],
                    [60,  65,  57,  64],
                    [55,  59,  62,  65],
                    [57,  60,  64,  55],
                    [59,  62,  65,  57]])
        
            # MODESET = [idx, [chord], mode type]
            MODESET = np.zeros((4, CHORD_LIST.shape[1], CHORD_LIST.shape[0]))

            # Lydian mode: Dreamy, ethereal, floaty, slightly unstable
            MODESET[0, :, 0] = CHORD_LIST[3, :]
            MODESET[1, :, 0] = CHORD_LIST[6, :]
            MODESET[2, :, 0] = CHORD_LIST[0, :]
            MODESET[3, :, 0] = CHORD_LIST[3, :]

            # Ionian mode: Bright, happy, stable, uplifting
            MODESET[0, :, 1] = CHORD_LIST[0, :]
            MODESET[1, :, 1] = CHORD_LIST[3, :]
            MODESET[2, :, 1] = CHORD_LIST[4, :]
            MODESET[3, :, 1] = CHORD_LIST[0, :]

            # Mixolydian mode: Bold, festive, gritty, bluesy
            MODESET[0, :, 2] = CHORD_LIST[4, :]
            MODESET[1, :, 2] = CHORD_LIST[0, :]
            MODESET[2, :, 2] = CHORD_LIST[1, :]
            MODESET[3, :, 2] = CHORD_LIST[4, :]

            # Dorian mode: Cool, hopeful, soulful, introspective
            MODESET[0, :, 3] = CHORD_LIST[1, :]
            MODESET[1, :, 3] = CHORD_LIST[4, :]
            MODESET[2, :, 3] = CHORD_LIST[5, :]
            MODESET[3, :, 3] = CHORD_LIST[1, :]

            # Aeolian mode: Melancholic, somber, emotional, reflective
            MODESET[0, :, 4] = CHORD_LIST[5, :]
            MODESET[1, :, 4] = CHORD_LIST[1, :]
            MODESET[2, :, 4] = CHORD_LIST[2, :]
            MODESET[3, :, 4] = CHORD_LIST[5, :]

            # Phrygian mode: Tense, dark, exotic, mysterious
            MODESET[0, :, 5] = CHORD_LIST[2, :]
            MODESET[1, :, 5] = CHORD_LIST[5, :]
            MODESET[2, :, 5] = CHORD_LIST[6, :]
            MODESET[3, :, 5] = CHORD_LIST[2, :]

            # Locrian mode: Dissonant, unstable, eerie, unsettling
            MODESET[0, :, 6] = CHORD_LIST[6, :]
            MODESET[1, :, 6] = CHORD_LIST[2, :]
            MODESET[2, :, 6] = CHORD_LIST[3, :]
            MODESET[3, :, 6] = CHORD_LIST[6, :]
            print("modeset created")
            return MODESET        
        
        
        modeset = create_modeset()

        for idx in range(len(valence_array)):
            mid = MidiFile()
            track = MidiTrack()
            mid.tracks.append(track)
            
            # tempo setting
            tempo = bpm2tempo(self.BASE_BPM)
            track.append(MetaMessage('set_tempo', tempo=tempo, time=0))
        
            valence_norm = (valence_array[idx] + 100) / 200 # [-100, 100] -> normalize to [0, 1]
            if arousal_array[idx] != 0:
                arousal_norm = arousal_array[idx] / 100 # [0, 100] -> normalize to [0, 1]
            else:
                arousal_norm = 0.1
            
            mode = 6 - round(valence_norm * 6)
            roughness = 1 - arousal_norm
            velocity = arousal_norm
            voicing = valence_norm
            loudness = round(arousal_norm * 10) / 10 * 40 + 60

            # create 4 bar loop per valence-arousal point
            for seq in range(self.BARS_TO_EACH_POINT): 
                activate1 = np.where(np.random.rand(8) < roughness, 0, 1) # probability(0) = roughness
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
                    delay = int((0.3 - velocity * 0.15) * mid.ticks_per_beat * 2) # length of th melody

                    if activate1[tone] == 1:
                        note = int(modeset[seq, 1, mode] + bright[4] * 12)
                        vel = random.randint(self.MIN_LOUDNESS, int(loudness))
                        track.append(Message('note_on', channel=0, note=note, velocity=vel, time=0))
                        track.append(Message('note_off', channel=0, note=note, velocity=vel, time=delay)) # turn off notes after delay

                    if activate2[tone] == 1:
                        idx2 = np.random.randint(2, 4)
                        note = int(modeset[seq, idx2, mode] + bright[5] * 12)
                        vel = random.randint(self.MIN_LOUDNESS, int(loudness))
                        track.append(Message('note_on', channel=0, note=note, velocity=vel, time=0))
                        track.append(Message('note_off', channel=0, note=note, velocity=vel, time=delay)) # turn off notes after delay

            # save to file (.mid)
            os.makedirs(self.output_dir, exist_ok=True)  # make directory if it does not exist
            file_name = f"melody_{idx+1}_val{valence_array[idx]}_aro{arousal_array[idx]}.mid"
            midi_path = os.path.join(self.output_dir, file_name)
            mid.save(midi_path)
            print(f"MIDI file saved: {midi_path}")


            def midi_to_wav(midi_path):
                mid = MidiFile(midi_path)
                
                time = 0.0
                audio = np.zeros(int(mid.length * self.sample_rate))

                for msg in mid.play():
                    time += msg.time
                    if msg.type == 'note_on' and msg.velocity > 0:
                        duration = 0.5  # 固定長
                        start_sample = int(time * self.sample_rate)
                        end_sample = int((time + duration) * self.sample_rate)

                        # end_sampleがaudioの長さを超えないように調整
                        if end_sample > len(audio):
                            end_sample = len(audio)
                        
                        # 波形の長さを調整
                        wave_duration = end_sample - start_sample
                        t = np.linspace(0, duration, wave_duration, False)
                        freq = 440.0 * 2 ** ((msg.note - 69) / 12.0)
                        wave = 0.2 * np.sin(2 * np.pi * freq * t)

                        # 波形の長さが一致するように調整
                        if len(wave) < wave_duration:
                            wave = np.pad(wave, (0, wave_duration - len(wave)))

                        audio[start_sample:end_sample] += wave

                # 正規化
                audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
                wave_path = os.path.join(self.output_dir, f"melody_{idx+1}_val{valence_array[idx]}_aro{arousal_array[idx]}.wav")
                write(wave_path, self.sample_rate, audio)
                print(f"WAV file saved as {wave_path}")
                
            midi_to_wav(midi_path)
            
    def get_output_directory_path (self):
        return self.output_dir