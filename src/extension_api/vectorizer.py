from gensim import corpora
import numpy as np
import pickle
from db import vectors
from logger import get_module_logger
logger = get_module_logger(__name__)


class LDAVectorizer():
    """LDAのベクトル化を行うもの"""

    def __init__(self, page_texts, topic_N=20, no_below=2, no_above=0.3,
                 load_name=None, save_name=None):
        self.lda, self.dictionary, _ = self.generate_model(page_texts, topic_N,
                                                           no_below, no_above,
                                                           load_name, save_name
                                                           )

    def vectorize(self, text):
        # 各トピックにおける所属確率をベクトルとする。
        if isinstance(text, str):
            text = text.split(' ')
        doc2bow = self.dictionary.doc2bow(text)
        topics = np.array(self.lda.get_document_topics(doc2bow))
        vec = [self.value_or_zero(topics, i)
               for i in range(self.lda.num_topics)]
        return np.array(vec)

    @classmethod
    def sort_by_similar(cls, by_vec, vec_list):
        if isinstance(by_vec, vectors):
            by_vec = by_vec.get_np_vector()

        if isinstance(vec_list[0], vectors):
            return sorted(vec_list, key=lambda x:
                          cls.cos_sim(x.get_np_vector(), by_vec))
        if isinstance(vec_list[0], np.ndarray):
            return sorted(vec_list, key=lambda x: cls.cos_sim(x, by_vec))

    @staticmethod
    def cos_sim(v1, v2):
        return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

    # @staticmethod
    # def cos_sim_matrix(matrix):
        """
        item-feature 行列が与えられた際に
        item 間コサイン類似度行列を求める関数
        # https://stackoverflow.com/questions/17627219/whats-the-fastest-way-in-python-to-calculate-cosine-similarity-given-sparse-mat
        """
        # d = matrix @ matrix.T  # item-vector 同士の内積を要素とする行列
        # コサイン類似度の分母に入れるための、各 item-vector の大きさの平方根
        # norm = (matrix * matrix).sum(axis=1, keepdims=True) ** .5
        # それぞれの item の大きさの平方根で割っている（なんだかスマート！）
        # return d / norm / norm.T

    @staticmethod
    def value_or_zero(topics, i):
        indexes = topics[:, 0]
        values = topics[:, 1]
        if i in indexes:
            index = np.where(indexes == i)
            return values[index][0]
        return 0

    @classmethod
    def generate_model(clf, page_texts, topic_N=20, no_below=2, no_above=0.3,
                       load_name=None, save_name=None):
        # 学習行う系。page_textsはページごとの文書。単語スペース区切り。
        dictionary, corpus = clf.generate_corpus(
            page_texts, no_below, no_above, load_name, save_name)
        from gensim.models import ldamodel
        lda = ldamodel.LdaModel(
            corpus=corpus, num_topics=topic_N, id2word=dictionary)
        return lda, dictionary, corpus

    @classmethod
    def generate_corpus(cls, page_texts, no_below, no_above,
                        load_name, save_name):
        """
        Summary: 辞書、コーパスの生成
                 辞書は    [{id  単語  df},...] の情報を持つ。
                 コーパスは [(id, df), (id, df), ...]という形式で保存される。
        Attributes:
            @param (page_texts):ページ毎の文書。単語スペース区切り。
            @param (no_below) default=2: no_below以下の出現回数の単語は無視。
            @param (no_above) default=0.3: no_above以上の文書割合に出現したワードはありふれているので、無視
            @param (load_name) default=None: 元のコーパスがあり、page_textsを追加する時。
            @param (save_name) default=None: セーブする時に名前を。
        Returns: 辞書、コーパス
        """
        # 面倒なので、とりあえずコーパス作成の大元をテキストファイルで保存しておく。
        # TODO: 非常に重くなると想定されるので、のちに改修が必要。
        #       あるいは、DBから持ってこれるようにするなど。
        if load_name is not None:
            pre_page_texts = cls.__read_page_texts("{}.txt".format(load_name))
            page_texts = pre_page_texts + page_texts

        if save_name is not None:
            cls.__save_page_texts("{}.txt".format(save_name), page_texts)

        # ページ毎の単語リスト。二重リストになる。
        wvs = [line.split(' ') for line in page_texts]
        # 辞書
        dictionary = cls.__generate_dictionary(wvs)
        # 辞書、前処理
        dictionary.filter_extremes(no_below=no_below, no_above=no_above)
        # コーパス
        corpus = cls.__generate_corpus_from_dict(wvs, dictionary)
        return dictionary, corpus

    @staticmethod
    def __read_page_texts(path):
        # 全文読み込み
        with open(path, "r") as f:
            return f.read().split('\n')

    @staticmethod
    def __save_page_texts(path, page_texts):
        # 全文書き込み
        with open(path, "w") as f:
            return f.write("\n".join(page_texts))

    @staticmethod
    def __generate_corpus_from_dict(wvs, dictionary,
                                    load_name=None, save_name=None):
        # コーパスの生成
        # doc2bowは単語の出現回数を数える。
        now_corpus = [dictionary.doc2bow(text) for text in wvs]
        corpus = now_corpus

        _ = load_name
        # TODO:ロードして追加系は面倒くさいので、後で考える。
        # if load_name is None:
        #     corpus = now_corpus
        # else:
        #     corpus = corpora.MmCorpus('{}.mm'.format(load_name))
        #     corpus.extend(now_corpus)

        # コーパスの保存
        # 後の追加を想定し、filter_extremesされる前に保存。
        if save_name is not None:
            corpora.MmCorpus.serialize('{}.mm'.format(save_name), corpus)
        return corpus

    @staticmethod
    def __generate_dictionary(wvs, load_name=None, save_name=None):
        # 辞書の生成
        if load_name is None:
            dictionary = corpora.Dictionary(wvs)
        else:
            dictionary = corpora.Dictionary.load_from_text(
                '{}.txt'.format(load_name))
            dictionary.add_documents(wvs)
        # 辞書の保存
        if save_name is not None:
            dictionary.save_as_text('{}.txt'.format(save_name))
        return dictionary

    def save(self, _dir):
        name = self.get_vec_type_name()
        path = "{}/{}.model".format(_dir, name)
        with open(path, 'wb') as f:
            pickle.dump(self, f)
            logger.info("save {} at {}".format(self.__str__(), path))

    def get_vec_type_name(self):
        return "lda{}".format(self.lda.num_topics)

    @staticmethod
    def load(path):
        with open(path, 'rb') as f:
            obj = pickle.load(f)
            logger.info("load {} from {}".format(obj.__str__(), path))
            return obj
