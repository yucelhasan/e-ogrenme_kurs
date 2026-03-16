import pyodbc
import os
from dotenv import load_dotenv
from pathlib import Path

# .env dosyasını oku
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

# Bağlantı bilgileri (master üzerinden bağlanıp yeni db açacağız)
server = os.environ.get('DB_HOST')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_PASSWORD')

# SQL Server'a bağlan (autocommit=True şarttır)
conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=master;UID={user};PWD={password}'

try:
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    # YENİ VERİTABANI OLUŞTURMA KOMUTU
    cursor.execute("CREATE DATABASE lms_db")
    print("TEBRİKLER: 'lms_db' veritabanı AWS üzerinde başarıyla oluşturuldu!")

except Exception as e:
    print("Hata oluştu:", e)
finally:
    if 'conn' in locals():
        conn.close()