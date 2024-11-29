##app.py
from fastapi import FastAPI
from fastapi import FastAPI, Request, HTTPException  # FastAPIの主要モジュールとHTTP例外をインポート
from fastapi.responses import JSONResponse  # JSONレスポンスを返すためのモジュールをインポート
from fastapi.middleware.cors import CORSMiddleware  # CORSミドルウェアをインポート
import mysql.connector  # MySQLデータベースとの接続を行うためのモジュールをインポート
from mysql.connector import errorcode  # MySQLエラーコードの管理モジュールをインポート
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

# CORSの設定を追加。全てのオリジン、メソッド、ヘッダーを許可


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジン（アクセス元）を許可
    allow_credentials=True,  # Cookieなどの認証情報を許可
    allow_methods=["*"],  # すべてのHTTPメソッドを許可（GET, POST, PUT, DELETEなど）
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# データベース接続情報の設定（接続先、ユーザー名、パスワード、データベース名、SSLの設定）

config = {
    'host': 'tech0-db-step4-studentrdb-9.mysql.database.azure.com',  # データベースのホスト名
    'user': 'tech0gen7student',  # データベースのユーザー名
    'password': os.getenv('MYSQL_PASSWORD', 'F4XyhpicGw6P'),  # 環境変数からパスワードを取得
    'database': 'siryou_pos_db',  # 使用するデータベース名
    'client_flags': [mysql.connector.ClientFlag.SSL],  # SSL接続を使用するためのフラグ
    'ssl_ca': '/home/site/site/certificate/DigiCertGlobalRootCA.crt.pem'  # SSL証明書ファイルのパス
}

# データベース接続を行い、ユーザー情報を取得する関数
def get_users_from_db(username):
    try:
        # データベース接続を確立
        conn = mysql.connector.connect(**config)
        print("Connection established")  # 接続成功のメッセージを表示

        cursor = conn.cursor()  # カーソルを作成
        # ユーザー情報を取得するSQLクエリ（実際のテーブル名とカラム名に変更が必要）
        query = "SELECT username, password FROM users WHERE username = %s;"
        print("テスト")
        cursor.execute(query,(username,))  # SQLクエリを実行
        print("テスト2")
        # 取得したデータを辞書形式に変換（ユーザー名をキー、パスワードを値として保存）
        users = {username: password for username, password in cursor.fetchall()}
        print("テスト3")
        cursor.close()  # カーソルを閉じる
        conn.close()  # 接続を閉じる
        return users  # 取得したユーザー情報を返す

    except mysql.connector.Error as err:
        # エラーが発生した場合の処理
        print(f"Error connecting to the database: {err}")  # エラーメッセージを表示
        return {}  # 空の辞書を返す

@app.get("/")
def read_root():
    return {"Hello": "World"}

# /nightにアクセスがあった場合に実行される関数
@app.get("/night")
async def hello_night_world():
    return "Good night!"  # シンプルなテキストメッセージを返す

# /night/{id} にアクセスがあった場合に実行される関数
@app.get("/night/{id}")
async def good_night(id: str):
    # {id} にはユーザーから送られてきた文字列が入る
    return f'{id}さん、「早く寝てね」'  # 受け取ったidを使ってカスタムメッセージを返す

# '/login'エンドポイントを定義し、POSTメソッドのみを許可します
@app.post("/login")
async def login(request: Request):

    # リクエストのJSONデータを非同期で取得します
    data = await request.json()
    
    # JSONデータから'username'を取得します。存在しない場合はNoneを返します
    username = data.get('email')
    
    # JSONデータから'password'を取得します。存在しない場合はNoneを返します
    password = data.get('password')
    
    # データベースからユーザー情報を取得
    users = get_users_from_db(username)
    print(f"Fetched users from DB: {users}")
    print(f"Received Username: {username}")
    print(f"Received Password: {password}")
    
    # ユーザー名がusers辞書に存在し、かつパスワードが一致するか確認します
    if username in users and users[username] == password:
        # 認証成功の場合、歓迎メッセージを含むJSONレスポンスを返します
        return JSONResponse(content={'message': f'ようこそ！{username}さん'})
    else:
        # 認証失敗の場合、エラーメッセージを含むJSONレスポンスと
        # HTTP status code 401（Unauthorized）を返します
        raise HTTPException(status_code=401, detail="認証失敗")
    
