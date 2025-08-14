from urllib.parse import quote_plus
from sqlalchemy import create_engine
import pandas as pd, duckdb, os

print(">>> ATTACH 방식으로 DuckDB 생성 시작")

# 1) MySQL → DataFrame
pwd = quote_plus("lg7p@ssw0rd~!")
engine = create_engine(f"mysql+pymysql://lguplus7:{pwd}@localhost:3310/cp_data?charset=utf8mb4")
df = pd.read_sql("SELECT * FROM mart_top_cate3_by_addr3", engine)
print("MySQL rows:", len(df))

# 2) DuckDB 파일 경로 (C:\data)
duckdb_path = r"C:\data\mart_top_cate3_by_addr3.duckdb"
os.makedirs(os.path.dirname(duckdb_path), exist_ok=True)
print("DuckDB path:", duckdb_path)

# 3) 메모리 → 파일 DB로 ATTACH 후 저장
con = duckdb.connect(database=":memory:", read_only=False)
con.register("df", df)
con.execute(f"ATTACH '{duckdb_path}' AS d (READ_ONLY FALSE)")
con.execute("CREATE SCHEMA IF NOT EXISTS d.main")
con.execute("CREATE OR REPLACE TABLE d.mart_top_cate3_by_addr3 AS SELECT * FROM df")
rows = con.execute("SELECT COUNT(*) FROM d.mart_top_cate3_by_addr3").fetchone()[0]
con.close()

print("saved rows:", rows)
print("file exists:", os.path.exists(duckdb_path), "size:", os.path.getsize(duckdb_path) if os.path.exists(duckdb_path) else -1)
