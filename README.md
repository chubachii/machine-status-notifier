# 1. 環境構築

### venv

~~~terminal
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
~~~

# 2. TOKEN の編集
[LINE Notify](https://notify-bot.line.me) にアクセスし、通知を送信したいトークルームに対するトークンを発行する。 
発行したトークンを **config.json**にコピー＆ペーストする。

# 3. プログラムの実行

~~~terminal
python3 src/main.py
~~~