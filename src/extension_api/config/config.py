import argparse
import configparser
CONFIG_PATH = 'config.ini'
parser = argparse.ArgumentParser(description="""
検索拡張機能用APIです。基本的にトリガーは基本アプリから与えられます。
""")
parser.add_argument('--config-path', type=str, default=CONFIG_PATH,
                    help='設定ファイルの場所')
try:
    args = parser.parse_args()
    CONFIG_PATH = args.config_path
except BaseException as e:
    print("args読み込みでエラー起きました")

print("読み込み -> {}".format(CONFIG_PATH))
config = configparser.ConfigParser()
config.read(CONFIG_PATH)
