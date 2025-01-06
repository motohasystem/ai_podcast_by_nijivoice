import os
import sys
import json
from openai import OpenAI  # type: ignore


class OpenAIGenerator:
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def generate_text(self, prompt_file_path, systemprompt_file_path=""):
        # 指定されたmdファイルを読み込み、プロンプトとして使用します。
        with open(prompt_file_path, "r", encoding="utf-8") as file:
            prompt = file.read()

        if systemprompt_file_path:
            with open(systemprompt_file_path, "r", encoding="utf-8") as file:
                system_prompt = file.read()
        else:
            system_prompt = ""

        # OpenAI APIを使用してテキストを生成します。
        response = self.call_openai_api(prompt, system_prompt)
        return response

    def call_openai_api(self, prompt, system_prompt=""):
        """
        OpenAI APIを使用してテキストを生成します。
        """
        import openai

        openai.api_key = self.api_key
        client = OpenAI()

        json_schema = {
            "type": "json_schema",
            "json_schema": {
                "name": "dialogue_schema",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "dialogue": {
                            "type": "array",
                            "description": "A collection of dialogue entries.",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "speaker": {
                                        "type": "string",
                                        "description": "The name of the speaker.",
                                        "enum": [
                                            "Grreka",
                                            "Jelly",
                                        ],
                                    },
                                    "line": {
                                        "type": "string",
                                        "description": "The line spoken by the speaker.",
                                    },
                                },
                                "required": ["speaker", "line"],
                                "additionalProperties": False,
                            },
                        }
                    },
                    "required": ["dialogue"],
                    "additionalProperties": False,
                },
            },
        }

        # プロンプト用のメッセージを作成
        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            },
        ]
        if system_prompt != "":
            messages.insert(
                0,
                {
                    "role": "system",
                    "content": system_prompt,
                },
            )

        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                # model="gpt-4o-mini",
                messages=messages,  # type: ignore
                response_format=json_schema,  # type: ignore
                temperature=1,
                max_completion_tokens=4096,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API呼び出しエラー: {e}")
            return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenAI APIを使用してテキストを生成します。"
    )
    parser.add_argument(
        "--prompt_file",
        required=True,
        help="プロンプトファイルのパスを指定します。",
    )
    parser.add_argument(
        "--output_file",
        required=True,
        help="生成されたテキストを保存するJSONファイルのパスを指定します。",
    )
    parser.add_argument(
        "--system_prompt_file",
        required=False,
        default="",
        help="システムプロンプトを指定するオプションです。",
    )

    args = parser.parse_args()

    # 環境変数からAPIキーを取得
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("エラー: OPENAI_API_KEYが設定されていません。")
        sys.exit(1)

    # OpenAIGeneratorを初期化してテキストを生成
    generator = OpenAIGenerator(api_key)
    generated_text = generator.generate_text(args.prompt_file, args.system_prompt_file)

    if generated_text:
        print("生成されたテキスト:")
        print(generated_text)

        # 生成されたテキストをJSON形式で保存
        try:
            with open(args.output_file, "w", encoding="utf-8") as json_file:
                json_file.write(
                    json.dumps(json.loads(generated_text), indent=4, ensure_ascii=False)
                )

            print(f"生成されたテキストが{args.output_file}に保存されました。")
        except Exception as e:
            print(f"JSONファイル保存エラー: {e}")
    else:
        print("テキスト生成に失敗しました。")
