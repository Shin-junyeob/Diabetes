import pandas as pd
import mysql.connector

# MySQL 연결
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # ← 실제 MySQL 유저명
    password="m2rong^^",  # ← 실제 MySQL 비밀번호
    database="hosp"  # ← hosp 스키마 사용
)
cursor = conn.cursor()

# CSV 파일 불러오기 (UTF-8 인코딩)
df = pd.read_csv("./hosp/admissions_utf-8.csv", encoding="utf-8")
df = df.where(pd.notna(df), None)

# 테이블 컬럼명 확인 (MySQL admissions 테이블에 맞게 변경해야 함)
columns = ['hadm_id', 'subject_id', 'admittime', 'dischtime', 'deathtime', 'admission_type', 'admission_location', 'discharge_location', 'insurance', 'language', 'marital_status', 'race', 'edregtime', 'edouttime', 'hospital_expire_flag']  # admissions 테이블 컬럼명으로 변경

# INSERT SQL 문 구성
sql = f"INSERT INTO admissions ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"

# 데이터 삽입
for _, row in df.iterrows():
    values_list = [tuple(row) for _, row in df.iterrows()]
    cursor.executemany(sql, values_list)

# 커밋 및 연결 종료
conn.commit()
cursor.close()
conn.close()