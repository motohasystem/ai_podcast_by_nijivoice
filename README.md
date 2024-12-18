# ai_podcast_by_nijivoice
にじボイスAPIを利用したAIポッドキャスト作成ツールの試作です

# usage

main.py をそのまま呼び出すと使用方法を出力します。

    $ python main.py
    使用方法: python script.py <input_json_file> <output_folder>

サンプルで同梱した12月の対話を作るにはこのように実行します。

    $ python main.py 12月.json dialogue

# jsonの作り方

ChatGPTに渡したプロンプトを同梱します。

    > 会話JSON作成プロンプト.md

[12月.json] と同じような構造を持ったjsonが出力されれば成功です。

うまくいかない場合はプロンプトを調整したり、apiのjson modeを使ったりしてみてください。


