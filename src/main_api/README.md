 # WSL Degital Library
WSL内のPDFを共有するシステム

## 起動方法
* server.py  
db02と通信して必要なデータを取得、jsに返す  
起動コマンド：nohup python server.py &
* elasticsearch  
データ取得の高速化のため導入  
起動コマンド：nohup ../elasticsearch-2.3.4/bin/elasticsearch &  
* nginx  
webサーバーとして機能させるため導入したミドルウェア  
起動コマンド：sudo nginx  
再起動コマンド：sudo nginx -s reload

## ファイル説明
* server.py  
pythonで書かれたサーバースクリプト  
mysqlやelasticsearchからデータを取得する

* setting.ini  
server.pyのconfigファイル

* yellow_filenames.csv  
yellowからファイル名を取得するとデータベース一致しないことがある  
それを防ぐため、yellowのscansnapフォルダ内のファイル名一覧保存しておく

* index.html  
nginxが反映させるメインのhtml  
jsで動的な挙動にしているため、基本的にhtmlスクリプトはこれのみ

* test_dlPDF  
PDFとダウンロード用にzipが保存されている

* models  
server.pyでmysqlやelasticsearchと通信する際に必要となるモデルが書かれたスクリプト

* images  
画像が保存されている

* config/enviroment.yml  
jsがサーバーと通信する際のIPといったconfigファイル
