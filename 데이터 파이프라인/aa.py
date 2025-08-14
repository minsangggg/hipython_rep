import pandas as pd
import chardet
import glob
import os

folder = r"C:\data\sbo"
files = glob.glob(os.path.join(folder, "*.csv"))

for file in files:
    with open(file, 'rb') as f:
        result = chardet.detect(f.read(100000))  # 100KB만 샘플로
    detected_encoding = result['encoding']
    print(f"{file} → 감지된 인코딩: {detected_encoding}")

    df = pd.read_csv(file, encoding=detected_encoding, engine="c", low_memory=False)
    new_name = os.path.splitext(file)[0] + "_utf8.csv"
    df.to_csv(new_name, index=False, encoding="utf-8-sig")
    print(f"변환 완료 → {new_name}")
