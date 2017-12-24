FROM ubuntu:16.04
MAINTAINER syunyooo

# elastic実行用にjavaを入れる
ENV JAVA_HOME /usr/lib/jvm/java-8-oracle
RUN echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
    apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:webupd8team/java && \
    apt-get update && \
    apt-get install -y oracle-java8-installer

# nginx
RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y curl
RUN touch /etc/apt/sources.list.d/nginx.list
RUN echo "deb http://nginx.org/packages/ubuntu/ precise nginx" >> /etc/apt/sources.list.d/nginx.list
RUN echo "deb-src http://nginx.org/packages/ubuntu/ precise nginx" >> /etc/apt/sources.list.d/nginx.list
RUN curl http://nginx.org/keys/nginx_signing.key | apt-key add -
RUN apt-get update
RUN apt-get install -y nginx

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
# Python3 と pip3, 日本語パッケージ
RUN apt-get update \
  && apt-get install -y python3 \
                        python3-pip \
                        language-pack-ja \
                        vim \
                        python-dev \
                        libmysqlclient-dev \
                        sudo \
                        iputils-ping \
                        net-tools \
                        dnsutils

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
RUN apt-get update && apt-get install -y fonts-migmix
# フォントの設定書き換え
COPY docker_local.conf /etc/fonts/local.conf

ENV LANG ja_JP.UTF-8
ENV PYTHONIOENCODING utf_8

# ローカル時間を東京に変更
# RUN echo "Asia/Tokyo" | tee /etc/timezone \
#    dpkg-reconfigure --frontend noninteractive tzdata
ENV TZ Asia/Tokyo

# 起動時のアプリの設定
# ADD setting.ini /home/python/src/main_api/setting.ini
# ADD config/enviroment.yml /home/python/src/main_api/config/enviroment.yml

# nginxの設定
ADD default.conf /etc/nginx/conf.d/

# EXPOSE 80
# RUN sudo service nginx start
CMD ["/bin/bash"]