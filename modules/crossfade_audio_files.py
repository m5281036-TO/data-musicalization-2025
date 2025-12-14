import os
from pydub import AudioSegment

class CrossfadeAudioFiles:
    @staticmethod
    def crossfade_audio_files(
        input_path: str = "./data/output/generated_music_suno/",
        crossfade_duration_ms: int = 5000,
        clip_total_length_ms: int = 30000  # フェードを含めた最終的な各クリップ長
    ):
        files = sorted([f for f in os.listdir(input_path) if f.lower().endswith(".mp3")])
        print(f"files: {files}")

        if len(files) < 2:
            raise ValueError("At least 2 files is needed.")

        # 各クリップの有効部分は以下になる
        trim_head_ms = 0
        trim_tail_ms = clip_total_length_ms - crossfade_duration_ms
        if trim_tail_ms <= 0:
            raise ValueError("clip_total_length_ms must be larger than crossfade_duration_ms.")

        first_audio = AudioSegment.from_mp3(os.path.join(input_path, files[0]))
        if len(first_audio) <= trim_tail_ms:
            raise ValueError(f"File too short to trim: {files[0]}")

        combined = first_audio[trim_head_ms : trim_tail_ms]

        for file in files[1:]:
            audio = AudioSegment.from_mp3(os.path.join(input_path, file))

            if len(audio) <= trim_tail_ms:
                raise ValueError(f"File too short to trim: {file}")

            trimmed = audio[trim_head_ms : trim_tail_ms]

            if len(combined) < crossfade_duration_ms or len(trimmed) < crossfade_duration_ms:
                raise ValueError(f"File too short for crossfade: {file}")

            combined = combined.append(trimmed, crossfade=crossfade_duration_ms)

        output_path = os.path.join(input_path, "crossfade/crossfade.mp3")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        combined.export(output_path, format="mp3")
        print(f"Crossfaded mp3 file saved to: {output_path}")


if __name__ == "__main__":
    fader = CrossfadeAudioFiles()
    fader.crossfade_audio_files(input_path="./data/output/generated_music_suno/20251212_electronic/seg_2")
