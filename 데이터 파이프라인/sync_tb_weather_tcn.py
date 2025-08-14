# sync_tb_weather_tcn.py
import sys
import pymysql
import mariadb

# 원격(소스): PyMySQL 사용
SRC = dict(host="192.168.14.38", port=3310, user="lguplus7",
           password="lg7p@ssw0rd~!", database="cp_data", charset="utf8mb4",
           cursorclass=pymysql.cursors.Cursor)

# 로컬(타깃): mariadb 사용
DST = dict(host="127.0.0.1", port=3310, user="lguplus7",
           password="lg7p@ssw0rd~!", database="cp_data")

SELECT_SQL = """
SELECT STN_ID, LON, LAT, STN_SP, HT, HT_WD, LAU_ID, STN_AD,
       STN_KO, STN_EN, FCT_ID, LAW_ID, BASIN,
       addr1, addr2, addr3, org_addr, create_dt
FROM tb_weather_tcn
"""

UPSERT_SQL = """
INSERT INTO tb_weather_tcn
(STN_ID, LON, LAT, STN_SP, HT, HT_WD, LAU_ID, STN_AD,
 STN_KO, STN_EN, FCT_ID, LAW_ID, BASIN,
 addr1, addr2, addr3, org_addr, create_dt)
VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
ON DUPLICATE KEY UPDATE
 LON=VALUES(LON), LAT=VALUES(LAT), STN_SP=VALUES(STN_SP), HT=VALUES(HT),
 HT_WD=VALUES(HT_WD), LAU_ID=VALUES(LAU_ID), STN_AD=VALUES(STN_AD),
 STN_KO=VALUES(STN_KO), STN_EN=VALUES(STN_EN), FCT_ID=VALUES(FCT_ID),
 LAW_ID=VALUES(LAW_ID), BASIN=VALUES(BASIN),
 addr1=VALUES(addr1), addr2=VALUES(addr2), addr3=VALUES(addr3),
 org_addr=VALUES(org_addr), create_dt=VALUES(create_dt)
"""

def main():
    try:
        src = pymysql.connect(**SRC)
        dst = mariadb.connect(**DST)
    except Exception as e:
        print("DB connect error:", e); sys.exit(1)

    sc = src.cursor()
    dc = dst.cursor()

    sc.execute(SELECT_SQL)

    total = 0
    while True:
        rows = sc.fetchmany(1000)
        if not rows:
            break
        dc.executemany(UPSERT_SQL, rows)
        dst.commit()
        total += len(rows)
        print(f"[MERGE] +{len(rows)} (acc={total})")

    sc.close(); src.close()
    dc.close(); dst.close()
    print(f"[DONE] merged rows: {total}")

if __name__ == "__main__":
    main()
