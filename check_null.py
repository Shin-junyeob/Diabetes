import pandas as pd
import os

# hosp/ 및 icu/ 폴더 경로 설정
base_folders = ["hosp", "icu"]

# NULL 값 개수를 저장할 딕셔너리
null_summary = {}

# 각 폴더별로 CSV 파일 처리
for folder in base_folders:
    folder_path = f"./{folder}"  # 상대 경로 기준 설정
    
    if not os.path.exists(folder_path):  # 폴더가 없으면 건너뜀
        print(f"Skipping missing folder: {folder_path}")
        continue

    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]  # 폴더 내 CSV 파일 검색

    for file in csv_files:
        file_path = os.path.join(folder_path, file)

        # NULL 값 개수를 저장할 변수
        null_counts = None

        try:
            # 청크 단위로 파일 읽기
            for chunk in pd.read_csv(file_path, chunksize=10000):  # 10,000개 행씩 로드
                chunk_null_counts = chunk.isnull().sum()

                # 첫 번째 청크일 경우 바로 할당, 이후에는 누적 합산
                if null_counts is None:
                    null_counts = chunk_null_counts
                else:
                    null_counts += chunk_null_counts

            null_summary[file] = null_counts  # 파일별 NULL 값 저장

        except Exception as e:
            print(f"Error reading {file_path}: {e}")  # 오류 발생 시 출력 후 계속 진행

# 결과 출력
for file, null_data in null_summary.items():
    print(f"File: {file}")
    print(null_data[null_data > 0])  # NULL 값이 있는 컬럼만 출력
    print("-" * 50)