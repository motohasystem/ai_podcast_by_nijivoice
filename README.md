# ai_podcast_by_nijivoice
にじボイスAPIを利用したAIポッドキャスト作成ツールの試作です
このツールには、以下の２つのスクリプトを含みます。

- A. プロンプトによる対話JSONの生成
- B. 対話JSONをにじボイスAPIでmp3化

## how to run

- A. プロンプトによる対話JSONの生成

    $ python dialogue.py --prompt_file <markdown_filepath> --system_prompt_file <system_prompt_filepath> --output_file <json_filepath> --dictionary_tsv <tsv_filepath>

    例: python dialogue.py --prompt_file prompt.md --system_prompt_file system.md --output_file dialogue.json --dictionary_tsv dictionary.tsv


- B. 対話JSONをにじボイスAPIでmp3化

    $ python speech.py <input_json_file> <output_folder>

    例: python speech.py input_dialogue.json speech_folder



# setup

まずは.envファイルににじボイスのAPIキーと、キャラクターIDを定義しておきます。

> API_KEY="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
> ID_CHAR_01="dba2fa0e-f750-43ad-b9f6-d5aeaea7dc16"
> ID_CHAR_02="dc92cd01-d116-4aae-b1d5-be581588ddcc"


## usage

main.py をそのまま呼び出すと使用方法を出力します。

    $ python speech.py
    使用方法: python speech.py <input_json_file> <output_folder>

サンプルで同梱した12月の対話を作るにはこのように実行します。

    $ python speech.py 12月.json dialogue

jsonの話者の名前は手抜きしてハードコードしてしまっています。
生成されたJSONに合わせて[mp3_generator.py]のコンストラクタを書き換えてください。

```python
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
```


## jsonの作り方

同梱したcall_openai.py を利用します。

    $ python call_openai.py --prompt_file prompt.md --system_prompt_file system.md --output_file dialogue.json

[12月.json] と同じような構造を持ったjsonが出力されれば成功です。


## 利用API

このプロジェクトは「にじボイス」を使用しています。

にじボイス | AIによる感情豊かな音声生成サービス
https://nijivoice.com/


## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、LICENSEファイルを参照してください。

