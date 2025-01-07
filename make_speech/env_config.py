import os
from dotenv import load_dotenv


class EnvConfig:
    """
    環境変数を管理するクラス。
    初期化時に環境変数をロードし、必要な値を設定します。
    """

    def __init__(self):
        load_dotenv()
        self.API_KEY = os.getenv("NIJIVOICE_API_KEY")
        self.ID_CHAR_01 = os.getenv("NIJIVOICE_ID_CHAR_01")
        self.ID_CHAR_02 = os.getenv("NIJIVOICE_ID_CHAR_02")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
