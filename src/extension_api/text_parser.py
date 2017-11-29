import MeCab
import re
from config import config
from tqdm import tqdm
from logger import get_module_logger
logger = get_module_logger(__name__)


class TextParser(object):
    """前処理に当たる処理を行う。"""
    # Mecabはクラス変数で管理。
    mecab_dic = config['mecab']['DIR']
    logger.info("load mecab : {}".format(mecab_dic))
    __mecab = MeCab.Tagger("-Ochasen -d " + mecab_dic)

    def __init__(self):
        super(TextParser, self).__init__()

    @classmethod
    def parse(cls, raw_data):
        """
        Function: parse
        Summary: テキスト情報をパースする
        Attributes:
          @param (raw_data):文字列か、文字列リスト。整形されていない生の情報。
        Returns: 整形後のテキスト
        """
        if isinstance(raw_data, str):
            parsed_text = cls.__pre_process(raw_data)
            return parsed_text
        elif isinstance(raw_data, list):
            logger.info("テキストをパースします...")
            return [cls.parse(raw_text) for raw_text in tqdm(raw_data)]
        raise Exception(
            "パースするデータ:{}はstr型か、strのlistである必要があります。".format(raw_data))

    @classmethod
    def __pre_process(cls, text):
        # 前処理のコードをココに記述
        return cls.__delete_noise(text)

    @classmethod
    def __delete_noise(cls, text):
        # ノイズの除去
        # TODO:情報系の本は日本語と英語は混在しやすい。しかし、英語と日本語では出現回数における重みが
        #      異なると思う（日本語の方が重い）。ので、これをどうにか解決する。
        noise_pattern = "(?:https?|ftp)://[A-Za-z0-9./-]*|@[A-Za-z0-9./-_]*"
        p = re.compile(r'' + noise_pattern)
        text = re.sub(p, "", text)
        text = re.sub(r'[0-9]', "", text)  # 数字除去 # |([+-]?[0-9]+\.?[0-9]*)
        text = re.sub(r'[︰-＠]', "", text)  # 全角記号除去
        text = re.sub('\n', " ", text)  # 改行文字除去
        text = text.lower()  # 小文字に変換
        text = " ".join(cls.__get_nouns(text))  # 名詞のみ抽出
        return text

    @classmethod
    def __get_nouns(cls, text):
        """
        文章から名詞をだけを取り出す
        @param sentence 対象の文章
        @return nouns 文章中に含まれる名詞のリスト
        """
        # logger.info("名詞のみ抽出。")
        cls.__mecab.parse('')
        node = cls.__mecab.parseToNode(text)
        nouns = []
        while node:
            word = node.surface
            info = node.feature
            # .split(",")[0]
            if "名詞" in info \
                    and cls.__is_all_not_in(["接尾", "接頭", "非自立", "代名詞", "数"],
                                            info):
                nouns.append(word)
            node = node.next
        # logger.info("抽出完了。名詞数:{}".format(len(nouns)))
        return nouns

    @staticmethod
    def __is_all_not_in(t_list, on_list):
        """
        Summary: t_listの全ての要素がon_listになければTrueを返す。
        Attributes:
          @param (t_list):InsertHere
          @param (on_list):InsertHere
        Returns: True/False
        """
        for item in t_list:
            if item in on_list:
                return False
        return True
