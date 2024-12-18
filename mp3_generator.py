import os
import json
import requests

class MP3Generator:
    """
    JSONデータからMP3ファイルを生成する機能を提供するクラス。
    """
    def __init__(self, config):
        self.config = config
        # speakerとEnvConfの定数のID_CHAR_01の対応を定義する辞書
        self.speaker_id_map = {
            "武士": self.config.ID_CHAR_01,
            "運転手": self.config.ID_CHAR_02,
            # 必要に応じて他のスピーカーとIDを追加
        }

    def text_to_mp3(self, text, speaker, output_file):
        """
        指定されたテキストをMP3ファイルに変換します。
        Nijivoice APIを使用して音声を生成し、MP3ファイルをダウンロードして保存します。

        引数:
            text (str): 読み上げるテキスト。
            speaker (str): 話者の名前。
            output_file (str): 保存するMP3ファイルのパス。
        """
        # 既存のファイルがある場合はスキップ
        if os.path.exists(output_file):
            print(f"ファイルが既に存在します。スキップ: {output_file}")
            return

        # speaker_idを取得
        speaker_id = self.speaker_id_map.get(speaker)
        if not speaker_id:
            print(f"スピーカーIDが見つかりません: {speaker}")
            return

        # APIキーを取得
        api_key = self.config.API_KEY

        # Nijivoice APIを呼び出して音声生成
        response = self.call_voice_generation_api(api_key, text, speaker_id)
        if response and response.status_code == 200:
            response_json = response.json()
            audio_url = response_json.get("generatedVoice", {}).get("audioFileUrl")
            if audio_url:
                # MP3ファイルをダウンロードして保存
                self.download_mp3(audio_url, output_file)
            else:
                print("音声ファイルのURLが取得できませんでした。")
        else:
            print("音声生成APIの呼び出しに失敗しました。")

    def call_voice_generation_api(self, api_key, text, speaker_id):
        """
        Nijivoice APIを使用して音声を生成する関数。

        引数:
            api_key (str): APIキー。
            text (str): 読み上げるテキスト。
            speaker_id (str): 話者のID。

        戻り値:
            requests.Response: APIのレスポンスオブジェクト。
        """
        url = f"https://api.nijivoice.com/api/platform/v1/voice-actors/{speaker_id}/generate-voice"

        payload = {
            "format": "mp3",
            "script": text,
            "speed": "1.0"
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": api_key
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"API呼び出しエラー: {e}")
            return None

    def download_mp3(self, url, output_file):
        """
        指定されたURLからMP3ファイルをダウンロードして保存します。

        引数:
            url (str): ダウンロードするMP3ファイルのURL。
            output_file (str): 保存するMP3ファイルのパス。
        """
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(output_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"ダウンロード完了: {output_file}")
        except requests.RequestException as e:
            print(f"ダウンロードエラー: {e}")

    def process_json_to_mp3(self, json_file, output_folder):
        """
        JSONファイルを読み込み、各ダイアログノードごとにMP3ファイルを生成します。

        引数:
            json_file (str): ダイアログを含むJSONファイルのパス。
            output_folder (str): MP3ファイルを保存するフォルダのパス。
        """
        # 出力フォルダが存在しない場合は作成します。
        os.makedirs(output_folder, exist_ok=True)

        # JSONファイルを読み込みます。
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # "dialogue"キーが存在するか確認します。
        if 'dialogue' not in data:
            raise ValueError("JSONファイルに'dialogue'キーが必要です。")

        # 各ダイアログノードを処理します。
        for idx, node in enumerate(data['dialogue'], start=1):
            speaker = node.get('speaker', 'Unknown')
            line = node.get('line', '')

            # MP3ファイル名を構築します。
            output_file = os.path.join(output_folder, f"{idx:03d}_{speaker}.mp3")

            # MP3ファイルを生成します。
            self.text_to_mp3(line, speaker, output_file)

            print(f"生成されました: {output_file}")
