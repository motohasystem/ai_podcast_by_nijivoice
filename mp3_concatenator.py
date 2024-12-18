from pydub import AudioSegment
import os

class MP3Concatenator:
    """
    指定したフォルダ内のMP3ファイルを連結するクラス。
    """
    def __init__(self, folder_path, silence_duration=2):
        self.folder_path = folder_path
        self.silence_duration = silence_duration  # 静音の秒数（デフォルト2秒）

    def concatenate_mp3_files(self, output_file):
        """
        フォルダ内のMP3ファイルを連結し、1つのMP3ファイルとして保存します。

        引数:
            output_file (str): 保存先のMP3ファイルのパス。
        """
        # フォルダ内のMP3ファイルを取得
        mp3_files = [
            os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path)
            if f.endswith('.mp3')
        ]

        if not mp3_files:
            print("指定されたフォルダにはMP3ファイルが存在しません。")
            return

        # ファイル名でソート
        mp3_files.sort()

        # 最初のファイルをベースにAudioSegmentを作成
        combined_audio = AudioSegment.from_file(mp3_files[0])

        # 残りのファイルを順次追加
        for file in mp3_files[1:]:
            audio = AudioSegment.from_file(file)
            combined_audio += audio

        # 静音を作成
        silence = AudioSegment.silent(duration=self.silence_duration * 1000)  # 秒をミリ秒に変換

        # 冒頭と末尾に静音を追加
        combined_audio = silence + combined_audio + silence

        # 連結結果を保存
        combined_audio.export(output_file, format="mp3")
        print(f"連結されたMP3ファイルが保存されました: {output_file}")

