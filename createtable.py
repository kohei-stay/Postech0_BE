import os
import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv

# .envファイルをロード
load_dotenv()

# 接続設定
config = {
    'host': 'tech0-db-step4-studentrdb-9.mysql.database.azure.com',
    'user': 'tech0gen7student',
    'password': os.getenv('MYSQL_PASSWORD', 'F4XyhpicGw6P'),  # デフォルトパスワード
    'database': 'siryou_pos_db',
    'client_flags': [mysql.connector.ClientFlag.SSL],
    'ssl_ca': '/Users/koheikanai/certificate/DigiCertGlobalRootCA.crt.pem'
}

try:
    conn = mysql.connector.connect(**config)
    print("Connection established")
    cursor = conn.cursor()

    # 既存のusersテーブルを削除
    cursor.execute("DROP TABLE IF EXISTS users;")
    print("Dropped existing users table (if existed).")

    # 新しいusersテーブルを作成
    cursor.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    );
    """)
    print("Created new users table.")

    # 辞書データ
    users = {
        'yagimasa': {'password': 'password123', 'email': 'yagimasa@example.com'},
        'lego': {'password': 'password456', 'email': 'lego@example.com'},
        'siryo': {'password': 'password789', 'email': 'siryo@example.com'}
    }

    # 辞書データをテーブルに挿入
    for username, details in users.items():
        cursor.execute("""
        INSERT INTO users (username, email, password)
        VALUES (%s, %s, %s);
        """, (username, details['email'], details['password']))
        print(f"Inserted user: {username}")

    # トランザクションをコミット
    conn.commit()
    print("All users have been inserted.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    print("Connection closed.")
