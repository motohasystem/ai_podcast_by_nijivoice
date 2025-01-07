import json
from openai import OpenAI  # type: ignore


class OpenAIGenerator:
    def __init__(self, api_key, model="gpt-4o-mini"):
        self.api_key = api_key
        self.model = model
        self.schema_json = None

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

        # JSONスキーマが設定されている場合は、スキーマファイルを読み込んでスキーマとして使用します。
        if self.schema_json:
            # ファイルを読み込む
            with open(self.schema_json, "r", encoding="utf-8") as file:
                json_schema = json.load(file)
                # print(json_schema)
                # exit(0)
        else:
            # 未指定の場合はデフォルトのスキーマを使用します。
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
