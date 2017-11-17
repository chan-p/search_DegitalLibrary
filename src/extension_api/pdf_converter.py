import MeCab
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from tqdm import tqdm
from logger import get_module_logger
logger = get_module_logger(__name__)


class PDFConverter():
    """
    PDFを扱う系
    ・PDFの読みこみ
    ・ノイズ除去
    ・形態素解析
    を行なった末、テキスト情報を返却するのが目的。
    """
    def __init__(self):
        mecab_dic = "/usr/local/lib/mecab/dic/mecab-ipadic-neologd/"
        self.__mecab = MeCab.Tagger("-Ochasen -d " + mecab_dic)
    
    def read_pretty(self, path, save_path=None):
        """
        Function: read_pdf_text
        Summary: PDFのテキストを綺麗に読み込む。ノイズ除去、形態素解析などを施す。
        Attributes: 
            @param (path):PDFのパス
            @param (save_path) default=None: テキスト情報を.txtに吐き出したい場合、ここにパス指定
        Returns: 綺麗なテキスト(String,空白区切)
        """
        logger.info("PDF:{path}を読み込みます。".format(path=path))
        text = self.read(path)
        logger.info("読み込み完了。->文字数:{}".format(len(text)))
        text = self.__pre_process(text)
        logger.info("前処理。->文字数:{}".format(len(text)))
        text = " ".join(self.__get_noun(text))
        if save_path is not None:
            self.__save_text(save_path, text)
        return text

    def read(self, path, separater="\n"):
        """
        Function: read
        Summary: PDFの素のテキストを読み込み、返却する。
        Attributes: 
            @param (path):PDFのパス
        Returns: "book_text"
        """
        return separater.join(self.read_by_page(path))
    
    def read_by_page(self, path):
        """
        Function: read_by_page
        Summary: PDFの素のテキストを読み込み、返却する。ページ毎にリストで取得する。
        Attributes: 
            @param (path):PDFのパス
        Returns: ["page1_text","page2_text",...]
        """
        result = []

        rsrcmgr = PDFResourceManager()
        outfp = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        laparams.detect_vertical = True
        device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams)

        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in tqdm(PDFPage.get_pages(fp)):
            interpreter.process_page(page)
            # バッファを取得後初期化する
            page_text = outfp.getvalue()
            result.append(page_text)
            outfp.truncate(0)
            outfp.seek(0)
        fp.close()
        device.close()
        outfp.close()
        return result
        
    def __pre_process(self, text):
        # 前処理のコードをココに記述
        return self.__delete_noise(text)
    
    def __delete_noise(self, text):
        # ノイズの除去
        noise_pattern = "(?:https?|ftp)://[A-Za-z0-9./-]*|@[A-Za-z0-9./-_]*"
        p = re.compile(r'' + noise_pattern)
        text = re.sub(p, "", text)
        text=re.sub(r'[0-9]', "", text)#数字 # |([+-]?[0-9]+\.?[0-9]*)
        text=re.sub(r'[︰-＠]', "", text)#全角記号
        text=re.sub('\n', " ", text)#改行文字
        return text
        
    def __get_noun(self, text):
        """
        文章から名詞をだけを取り出す
        @param sentence 対象の文章
        @return nouns 文章中に含まれる名詞のリスト
        """
        logger.info("名詞のみ抽出。")
        self.__mecab.parse('')
        node = self.__mecab.parseToNode(text)
        nouns = []
        while node:
            word = node.surface
            if node.feature.split(",")[0] == "名詞" and word != "の" :
                nouns.append(word)
            node = node.next
        logger.info("抽出完了。名詞数:{}".format(len(nouns)))
        return nouns
    
    def __save_words(self, path, words, separater=" "):
        self.__save_text(path, separater.join(words))
    
    def __save_text(self, path, text):
        with open(path,"w") as out:
            out.write(text)
        
        
# pdf_path = "../リーダブルコード.pdf"
# pc = PDFConverter()
# pc.read_pdf_text(pdf_path,save_path="名詞のみ.txt")