import os
import sys
import json
from dotenv import load_dotenv
from mp3_generator import MP3Generator
from mp3_concatenator import MP3Concatenator

class EnvConfig:
    """
    環境変数を管理するクラス。
    初期化時に環境変数をロードし、必要な値を設定します。
    """
    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("API_KEY")
        self.ID_CHAR_01 = os.getenv("ID_CHAR_01")
        self.ID_CHAR_02 = os.getenv("ID_CHAR_02")

if __name__ == "__main__":
    # 環境変数をロードして設定を作成します。
    config = EnvConfig()

    # スクリプトが正しい引数で呼び出されているか確認します。
    if len(sys.argv) != 3:
        print("使用方法: python script.py <input_json_file> <output_folder>")
        sys.exit(1)

    input_json = sys.argv[1]
    output_dir = sys.argv[2]

    # MP3Generatorインスタンスを作成して処理を実行します。
    generator = MP3Generator(config)

    try:
        generator.process_json_to_mp3(input_json, output_dir)
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)

    # 連結クラスを使用してMP3ファイルを結合
    concatenator = MP3Concatenator(folder_path=output_dir, silence_duration=2)
    concatenated_output = os.path.join(output_dir, "combined_output.mp3")

    try:
        concatenator.concatenate_mp3_files(concatenated_output)
    except Exception as e:
        print(f"連結エラー: {e}")
        sys.exit(1)
