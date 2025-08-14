# convert_and_load_sbo.py
import os, glob
from pathlib import Path
import pandas as pd
import chardet
import mariadb

SRC = Path(r"C:\data\sbo")
DST = Path(r"C:\data\sbo_utf8")
DST.mkdir(exist_ok=True)

# ---- 1) 모든 CSV → UTF-8 변환 ----
converted = []
for fp in SRC.glob("*.csv"):
    raw = fp.read_bytes()
    enc = chardet.detect(raw)["encoding"] or "cp949"
    df = pd.read_csv(fp, encoding=enc, engine="c", dtype=str, na_filter=False)
    out = DST / fp.name
    df.to_csv(out, index=False, encoding="utf-8-sig")
    converted.append(str(out))
print(f"[CONVERT] {len(converted)} files → UTF-8 saved in {DST}")

# ---- 2) MariaDB 적재 ----
DB = dict(user="lguplus7", password="lg7p@ssw0rd~!", host="localhost", port=3310, database="cp_data")
conn = mariadb.connect(**DB, local_infile=True)
cur = conn.cursor()

# 필요하면 주석 해제해서 테이블 비우고 시작
cur.execute("TRUNCATE tb_smb_ods"); conn.commit()

load_sql = """
LOAD DATA LOCAL INFILE %s
INTO TABLE tb_smb_ods
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '\"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,
 col11,col12,col13,col14,col15,col16,col17,col18,col19,col20,
 col21,col22,col23,col24,col25,col26,col27,col28,col29,col30,
 col31,col32,col33,col34,col35,col36,col37,col38,col39);
"""

for path in converted:
    cur.execute(load_sql, (path.replace("\\","/"),))
    conn.commit()
    print(f"[LOAD] {os.path.basename(path)}")

cur.close(); conn.close()
print("[DONE] All files loaded.")
