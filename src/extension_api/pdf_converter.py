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
    を行なった末、テキスト情報を返却するのが目的。
    """

    def __init__(self):
        super(PDFConverter, self).__init__()

    @classmethod
    def read(cls, path, separater="\n"):
        """
        Function: read
        Summary: PDFの素のテキストを読み込み、返却する。
        Attributes:
            @param (path):PDFのパス
        Returns: "book_text"
        """
        return separater.join(cls.read_by_page(path))

    @staticmethod
    def read_by_page(path):
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

    @classmethod
    def save_texts(cls, path, texts, separater="\n"):
        cls.save_text(path, separater.join(texts))

    @staticmethod
    def save_text(path, text):
        with open(path, "w") as out:
            out.write(text)


# pdf_path = "../リーダブルコード.pdf"
# pc = PDFConverter()
# pc.read_pdf_text(pdf_path,save_path="名詞のみ.txt")
