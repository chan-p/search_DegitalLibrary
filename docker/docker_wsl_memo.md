# Docker Compose

書き途中なので、ちょっとまってください

## Dockerのインストール
Docker for Macを[こちらのサイト](https://docs.docker.com/docker-for-mac/)を参考にしてインストールを行ってください。
具体的な手順はこちらのサイトにかかれていいますので、サイトを参照ください。

## Docker Composeのインストール
Docker Composeは[こちらのサイト](https://docs.docker.com/compose/install/)を参考にしてインストールを行ってください。  


## 動作

このディレクトリに移動  

以下を実行

```shell
# コンテナの起動
docker-compose up
```

dbコンテナとアプリコンテナの起動のズレで、一回エラーがでると思うので、その時には、上のコマンドを再度実行してください。



---





# 以下メモ

Docker Compose

## appサーバ

nginxで動作。

**ドキュメントルートを変更する必要あり。**

ubuntuなら `/etc/nginx/conf.d/default.conf`で指定

macなら `/usr/local/etc/nginx/nginx.conf`

設定後は`sudo service nginx restart`で再起動

## extension_apiサーバ

flaskで動作。



## docker compose

メモ。

- docker-compose.ymlの設定にttyなるものが存在。

  - ttyは docker run -t に相当←そもそもよくわかっとらん。調べる。
  - 下のリンク超参考になる。2つのコンソール間で出力を受けわたすと興奮。
  - http://takuya-1st.hatenablog.jp/entry/20101024/1287947368
  - docker -t 参考
  - https://teratail.com/questions/19477

- docker-compose.yml内で環境変数を使用

  - .envに書く
  - https://qiita.com/friedaji/items/c1894821a2c49395cfd7

- docker-composeで作成したcontainerにattach

  - docker exec -it ID_OR_NAME bash

- docker-composeの変更が反映されていない

  - docker-compose down
  - docker-compose —build up

- たまにdb接続がうまくいかない

  - dbが立ち上がらないまま、アプリを起動していることが原因

  - linksやdepends_onは起動する順序を決定するのみで、「DBの起動完了を確認してから、アプリを起動」みたいなことはしない。ひどい仕様。

  - シェルで管理する必要があるよう

    - pingを飛ばして判定、ループ。

    - https://yoshinorin.net/2017/02/19/docker-compose-wait-other-application/

      ​

Dockerコンテナの起動

以下の手順で、コンテナの起動を行います。
- Dockerfileにてmain_app(nginx&基本API), extension_apiのイメージ作成
- docker-compose.ymlを利用してアプリケーションの起動