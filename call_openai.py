import os
import sys
import json
from openai import OpenAI  # type: ignore


class OpenAIGenerator:
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.api_key = api_key
        self.model = model

    def generate_text(self, prompt_file_path):
        # 指定されたmdファイルを読み込み、プロンプトとして使用します。
        with open(prompt_file_path, "r", encoding="utf-8") as file:
            prompt = file.read()

        # OpenAI APIを使用してテキストを生成します。
        response = self.call_openai_api(prompt)
        return response

    def call_openai_api(self, prompt):
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
                                            "お姉さん（おちゃらけた運転手）",
                                            "お兄さん（落ち着いた雰囲気の武士）",
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

        try:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}],
                    }
                ],
                response_format=json_schema,
                temperature=1,
                max_completion_tokens=2048,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API呼び出しエラー: {e}")
            return None


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("使用方法: python call_openai.py <prompt_file_path> <output_json_file>")
        sys.exit(1)

    prompt_file_path = sys.argv[1]
    output_json_file = sys.argv[2]

    # 環境変数からAPIキーを取得
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("エラー: OPENAI_API_KEYが設定されていません。")
        sys.exit(1)

    # OpenAIGeneratorを初期化してテキストを生成
    generator = OpenAIGenerator(api_key)
    generated_text = generator.generate_text(prompt_file_path)

    if generated_text:
        print("生成されたテキスト:")
        print(generated_text)

        # 生成されたテキストをJSON形式で保存
        try:
            with open(output_json_file, "w", encoding="utf-8") as json_file:
                json_file.write(
                    json.dumps(json.loads(generated_text), indent=4, ensure_ascii=False)
                )

                # json_file.write(generated_text)
                # json.dump(
                #     {"generated_text": generated_text},
                #     json_file,
                #     ensure_ascii=False,
                #     indent=4,
                # )
            print(f"生成されたテキストが{output_json_file}に保存されました。")
        except Exception as e:
            print(f"JSONファイル保存エラー: {e}")
    else:
        print("テキスト生成に失敗しました。")
