# verify_duckdb.py
import duckdb, os

p = r"C:\data\mart_top_cate3_by_addr3.duckdb"
print("파일 존재 여부:", os.path.exists(p))
print("파일 크기:", os.path.getsize(p) if os.path.exists(p) else -1)

con = duckdb.connect(p)
print("테이블 목록:", con.execute("SHOW TABLES").fetchall())

cnt = con.execute("SELECT COUNT(*) FROM mart_top_cate3_by_addr3").fetchone()[0]
print("총 행 수:", cnt)

print("샘플 데이터:")
print(con.execute("SELECT * FROM mart_top_cate3_by_addr3 LIMIT 5").fetchdf())
con.close()
