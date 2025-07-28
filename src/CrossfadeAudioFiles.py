import os
from pydub import AudioSegment
from pydub.playback import play

class  CrossfadeAudioFiles:
    def crossfade_audio_files(input_path: str="../data/suno_downloads/", crossfade_duration_ms: int = 5000):
        # get mp3 files in alphabetical order
        files = sorted([f for f in os.listdir(input_path) if f.lower().endswith('.mp3')])
        print(f"files:{files}")

        if not files:
            raise ValueError("mp3 file does not exist")

        # 最初のファイルを読み込み
        combined = AudioSegment.from_mp3(os.path.join(input_path, files[0]))

        # 2番目以降のファイルを順にクロスフェードで結合
        for file in files[1:]:
            next_audio = AudioSegment.from_mp3(os.path.join(input_path, file))
            combined = combined.append(next_audio)

        # 出力
        output_path = os.path.join(input_path, "crossfade.mp3")
        combined.export(output_path, format="mp3")
        print(f"Concatinated mp3 file saved to: {output_path}")
