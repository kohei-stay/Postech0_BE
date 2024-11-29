import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

# .envファイルをロード
load_dotenv()

# データベース接続情報の設定
config = {
    'host': 'tech0-db-step4-studentrdb-9.mysql.database.azure.com',  # データベースのホスト名
    'user': 'tech0gen7student',  # データベースのユーザー名
    'password': os.getenv('MYSQL_PASSWORD', 'F4XyhpicGw6P'),  # 環境変数からパスワードを取得
    'database': 'siryou_pos_db',  # 使用するデータベース名
    'client_flags': [mysql.connector.ClientFlag.SSL],  # SSL接続を使用するためのフラグ
}

# 環境に応じて証明書パスを設定
if os.environ.get('AZURE_ENVIRONMENT') == 'true':  # Azure環境の場合
    config['ssl_ca'] = 'D:/home/site/certificate/DigiCertGlobalRootCA.crt.pem'
else:  # ローカル環境の場合
    config['ssl_ca'] = '/Users/koheikanai/certificate/DigiCertGlobalRootCA.crt.pem'  # ローカルの証明書パスを指定

# データベース接続と確認処理
try:
    conn = mysql.connector.connect(**config)  # データベース接続
    print("Connection established")  # 接続成功メッセージを表示

    cursor = conn.cursor()  # カーソルオブジェクトを作成

    # Step 1: テーブル構造を確認
    print("\nChecking table structure...")
    cursor.execute("DESCRIBE users;")  # usersテーブルの構造を取得
    table_structure = cursor.fetchall()
    for column in table_structure:
        print(column)

    # Step 2: テーブルのデータ内容を確認
    print("\nChecking table data...")
    cursor.execute("SELECT username, email, password FROM users;")
    rows = cursor.fetchall()
    print("Current table data:")
    for row in rows:
        print(row)

    # Step 3: 認証チェック
    print("\nRunning authentication check...")
    # テーブルから取得したデータを辞書形式に変換
    users = {
        username: {"email": email, "password": password}
        for username, email, password in rows
    }

    # テスト用の入力データ
    input_username = "lego"
    input_password = "password456"
    input_email = "lego@example.com"

    # 認証ロジック
    if (
        input_username in users
        and users[input_username]["password"] == input_password
        and users[input_username]["email"] == input_email
    ):
        print(f"ようこそ！{input_username}さん")
    else:
        print("認証失敗")

    # 接続を閉じる
    cursor.close()
    conn.close()
    print("\nDatabase connection closed.")

except mysql.connector.Error as err:  # エラー発生時の処理
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("ユーザー名またはパスワードに誤りがあります")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("データベースが存在しません")
    else:
        print(f"接続エラー: {err}")
