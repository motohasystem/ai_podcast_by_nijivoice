import os
import sys
import json

from openai_generator import OpenAIGenerator


class TextGenerator:
    def __init__(self, api_key):
        self.generator = OpenAIGenerator(api_key)
        self.alert_words = []
        self.schema_json = None  # JSONスキーマファイルのパス

    def set_schema_json(self, schema_json):
        self.schema_json = schema_json
        self.generator.schema_json = schema_json

    def run(self):
        self.generate_and_save_text(
            prompt_file=args.prompt_file,
            system_prompt_file=args.system_prompt_file,
            output_file=args.output_file,
        )

    def generate_and_save_text(self, prompt_file, system_prompt_file, output_file):
        generated_text = self.generator.generate_text(prompt_file, system_prompt_file)

        if generated_text:
            print("生成されたテキスト:")
            print(generated_text)

            # 生成されたテキストをJSON形式で保存
            try:
                with open(output_file, "w", encoding="utf-8") as json_file:
                    json_file.write(
                        json.dumps(
                            json.loads(generated_text), indent=4, ensure_ascii=False
                        )
                    )

                print(f"生成されたテキストが{output_file}に保存されました。")
            except Exception as e:
                print(f"JSONファイル保存エラー: {e}")
        else:
            print("テキスト生成に失敗しました。")

    # 生成されたJSONテキストを辞書に従って英単語の展開処理をする
    def process_generated_text(self, generated_json, dictionary_tsv, output_file):
        # 辞書の読み込み
        dictionary = {}
        if dictionary_tsv:
            with open(dictionary_tsv, "r", encoding="utf-8") as file:
                for line in file:
                    word, expansion = line.strip().split("\t")
                    dictionary[word] = expansion
        else:
            print("辞書ファイルが指定されていません。")
            return

        try:
            with open(generated_json, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"JSONデコードエラー: {e}")
            return

        # プロンプトに従って処理を実行
        node_treated = []
        for node in data["dialogue"]:
            speaker = node.get("speaker", "Unknown")
            line = node.get("line", "")

            # 処理を実行
            # print(f"{speaker}: {line}")
            for key, value in dictionary.items():
                if key in line:
                    # print(f"  {key} -> {value}")
                    line = line.replace(key, value)

            # node_treatedに追加
            node_treated.append({"speaker": speaker, "line": line})

            # 処理結果に、未処理のアルファベット文字列が含まれている場合はアラートを出力
            import re

            matches = re.findall(r"[a-zA-Z]+", line)
            if matches:
                for match in matches:
                    # msg = f"  アラート: 未処理のアルファベット文字列 '{match}' が含まれています。"
                    # print(msg)
                    self.alert_words.append(match)

        # 処理結果を保存
        data["dialogue"] = node_treated
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


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
    parser.add_argument(
        "--dictionary_tsv",
        required=False,
        default="",
        help="辞書ファイルのパスを指定するオプションです。",
    )
    parser.add_argument(
        "--schema_json",
        required=False,
        default="",
        help="JSONスキーマを定義したJSONファイルを指定するオプションです。",
    )

    args = parser.parse_args()

    # 環境変数からAPIキーを取得
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("エラー: OPENAI_API_KEYが設定されていません。")
        sys.exit(1)

    # TextGeneratorを初期化してテキストを生成
    generator = TextGenerator(api_key)

    # JSONスキーマが指定されている場合は、スキーマファイルパスをgeneratorにセットする
    if args.schema_json:
        generator.set_schema_json(args.schema_json)

    generator.run()

    # 生成されたテキストを処理
    output_treated = args.output_file.replace(".json", "_treated.json")
    generator.process_generated_text(
        args.output_file, args.dictionary_tsv, output_treated
    )

    # 出力メッセージを表示
    print(f"処理結果が{output_treated}に保存されました。")

    # アラート単語がある場合は出力
    if generator.alert_words:
        # 同じ単語は重複して表示しない
        generator.alert_words = list(set(generator.alert_words))
        print("英単語アラート:")
        for word in generator.alert_words:
            print(f"  {word}")
    else:
        print("英単語アラートはありません。")
