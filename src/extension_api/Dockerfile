FROM ubuntu:16.04
MAINTAINER syunyooo

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
# Python3 と pip3, 日本語パッケージ
RUN apt-get update \
  && apt-get install -y python3 \
                        python3-pip \
                        language-pack-ja \
                        vim \
                        python-dev \
                        libmysqlclient-dev

# mysqlのinstall
# そのままapt-getでインストールするとパスワードを聞かれる箇所で止まってしまうので、予め設定しておく。この例ではパスワードは「root」。
RUN echo "mysql-server mysql-server/root_password password root" | debconf-set-selections && \
    echo "mysql-server mysql-server/root_password_again password root" | debconf-set-selections && \
    apt-get -y install mysql-server


# BeautifulSoup4 など
COPY requirements.txt /usr/src/app/
RUN pip3 install --upgrade pip \
    && pip3 install -r /usr/src/app/requirements.txt

# 日本語のフォントのインストール
RUN apt-get install -y fonts-migmix
# フォントの設定書き換え
COPY docker_local.conf /etc/fonts/local.conf

ENV LANG ja_JP.UTF-8
ENV PYTHONIOENCODING utf_8

# ローカル時間を東京に変更
# RUN echo "Asia/Tokyo" | tee /etc/timezone \
#    dpkg-reconfigure --frontend noninteractive tzdata
ENV TZ Asia/Tokyo

# 開発用
# ENV PYTHONPATH=/Users/syunyo/Desktop/MyDev/python_dev/slack_fitness/python_app/src/
# WORKDIR $PYTHONPATH

# 実行用ではgit cloneして、パス通し、WORKDIRを設定。
# ENV PYTHONPATH=/Users/syunyo/Desktop/MyDev/python_dev/slack_fitness/python_app/src/
# WORKDIR /Users/syunyo/Desktop/MyDev/python_dev/slack_fitness/python_app/src/

CMD ["/bin/bash"]

