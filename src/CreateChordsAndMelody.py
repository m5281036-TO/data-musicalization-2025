from mido import Message, MidiFile, MidiTrack
import numpy as np
from scipy.io.wavfile import write

class CreateChordsAndMelody:
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate


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


    def create_activation_and_brightness(roughness, voicing):
        # create roughness (activate1)
        activate1 = np.random.rand(8)
        activate1 = np.where(activate1 < roughness, 0, 1)

        # create roughness (activate2)
        activate2 = np.random.rand(8)
        activate2 = np.where(activate2 < roughness, 0, 1)

        # create brightness
        bright = np.random.rand(6)
        if voicing < 0.5:
            bright = np.where(bright > voicing * 2, -1, 0)
        else:
            bright = np.where(bright < (voicing - 0.5) * 2, 1, 0)

        return activate1, activate2, bright



    def create_midi(modeset, filename='./test_data/output/output.mid', tempo=500000):
        mid = MidiFile()
        track = MidiTrack()
        mid.tracks.append(track)
        track.append(Message('program_change', program=0, time=0))
        
        valence = 0.5
        arousal = 0.5

        mode = 7-round(valence*6)
        roughness = 1-arousal
        velocity = arousal
        voicing = valence
        loudness = (round(arousal*10))/10*40+60
        
        duration = 1
        seq = 0
        # create chord
        for seq in range(4): # create 4 bar loop
            chord = modeset[seq, :, mode]
            print(f"seq {seq}: chord === {chord}")
            
            # play all note in chord
            i = 0
            for note in chord:
                track.append(Message('note_on', note=round(note), velocity=64, time=0))
            
            # note off
            time_ticks = int(mid.ticks_per_beat * duration)
            track.append(Message('note_off', note=round(chord[0]), velocity=64, time=time_ticks)) # for 1st note in chord
            for note in chord[1:]: # from 2nd to last note in chord
                track.append(Message('note_off', note=round(note), velocity=64, time=0))

        mid.save(filename)
        print(f"MIDI saved as {filename}")


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
    modeset = create_modeset()
    create_midi(modeset)
    

    # # Cメジャースケール
    # melody = [(60, 0.5), (62, 0.5), (64, 0.5), (65, 0.5), (67, 1.0)]



    # midi_to_wav()
