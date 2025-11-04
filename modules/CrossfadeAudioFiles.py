import os
from pydub import AudioSegment

class CrossfadeAudioFiles:
    @staticmethod
    def crossfade_audio_files(input_path: str = "../data/suno_downloads/", crossfade_duration_ms: int = 20000):
        # mp3ファイルをアルファベット順に取得
        files = sorted([f for f in os.listdir(input_path) if f.lower().endswith('.mp3')])
        print(f"files: {files}")

        if len(files) < 2:
            raise ValueError("At least 2 files is needed.")

        # 最初のファイルを読み込み
        audio1 = AudioSegment.from_mp3(os.path.join(input_path, files[0]))
        if len(audio1) > 60000: # if over 1 min
            combined = audio1[:60000]

        for file in files[1:]:
            next_audio = AudioSegment.from_mp3(os.path.join(input_path, file))
            if len(next_audio) > 60000: # if over 1 min
                next_audio = next_audio[:60000]

            # 両方のファイルが十分な長さであるか確認
            if len(combined) < crossfade_duration_ms or len(next_audio) < crossfade_duration_ms:
                raise ValueError(f"ファイルがクロスフェードに必要な長さより短い: {file}")

            # クロスフェードで結合
            combined = combined.append(next_audio, crossfade=crossfade_duration_ms)

        # 出力
        output_path = os.path.join(input_path, "crossfade/crossfade.mp3")
        combined.export(output_path, format="mp3")
        print(f"Crossfaded mp3 file saved to: {output_path}")
