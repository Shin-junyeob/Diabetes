import pandas as pd
import os

# 분석할 폴더 목록
folders = ["hosp/", "icu/"]

def detect_dtype(df, col):
    """컬럼 데이터 타입을 분석하여 MySQL 적합한 타입 추천"""
    try:
        # INT형 확인
        if pd.api.types.is_integer_dtype(df[col]):
            return "INT"
        # FLOAT형 확인
        elif pd.api.types.is_float_dtype(df[col]):
            return "FLOAT"
        # 날짜/시간형 확인
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            return "DATETIME"
        # 문자열형 (VARCHAR)
        else:
            max_len = df[col].astype(str).str.len().max()
            return f"VARCHAR({max_len})"
    except Exception:
        return "TEXT"

def find_primary_key(df):
    """Primary Key 후보 찾기"""
    unique_cols = [col for col in df.columns if df[col].nunique() == df.shape[0]]
    return unique_cols if unique_cols else ["No Unique Key Found"]

# 각 폴더(hosp, icu)를 순회하며 CSV 파일을 분석
for folder in folders:
    if not os.path.exists(folder):
        print(f"❌ Warning: {folder} does not exist. Skipping...")
        continue

    csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]

    for file in csv_files:
        file_path = os.path.join(folder, file)
        output_txt = os.path.join(folder, file.replace('.csv', '.txt'))

        print(f"Processing {file} in {folder} ...")

        try:
            # CSV 파일 읽기 (처음 10,000개 행만 샘플 분석)
            df = pd.read_csv(file_path, nrows=10000)

            # 컬럼별 데이터 타입 분석
            column_types = {col: detect_dtype(df, col) for col in df.columns}

            # Primary Key 후보 찾기
            primary_keys = find_primary_key(df)
            primary_key_str = "Primary Key Candidates: " + ", ".join(primary_keys)

            # 결과를 텍스트 파일로 저장
            with open(output_txt, 'w') as f:
                for col, dtype in column_types.items():
                    f.write(f"{col}: {dtype}\n")
                f.write("\n" + primary_key_str + "\n")

            print(f"✅ Saved column types and primary key info to {output_txt}")

        except Exception as e:
            print(f"❌ Error processing {file} in {folder}: {e}")