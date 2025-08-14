import requests
import mariadb
import sys

# DB 연결
try:
    conn_tar = mariadb.connect(
        user="lguplus7",
        password="lg7p@ssw0rd~!",
        host="localhost",
        port=3310,
        database="cp_data"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

tar_cur = conn_tar.cursor()  # <-- 여기서 커서 생성

# URL
req_url = (
    "https://apihub.kma.go.kr/api/typ01/url/stn_inf.php"
    "?inf=AWS&stn=&tm=202211300900&help=1&authKey=uXEt-y3SSYqxLfst0gmKTA"
)

resp = requests.get(req_url, timeout=30)
resp.encoding = resp.encoding or "euc-kr"  # 인코딩 보정
org_text = resp.text

insert_sql = """
INSERT INTO tb_weather_tcn
(STN_ID, LON, LAT, STN_SP, HT, HT_WD, LAU_ID, STN_AD, STN_KO, STN_EN, FCT_ID, LAW_ID, BASIN,
 addr1, addr2, addr3, org_addr, create_dt)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s,%s, %s, NOW())
"""

cnt = 0
for raw in org_text.splitlines():
    line = raw.strip()
    if not line or line.startswith("#") or set(line) <= set("- "):
        continue

    toks = line.split()
    if len(toks) < 12 or not toks[0].isdigit():
        continue

    # 앞 8개
    STN_ID = toks[0]
    LON    = toks[1]
    LAT    = toks[2]
    STN_SP = toks[3]
    HT     = toks[4]
    HT_WD  = toks[5]
    LAU_ID = toks[6]
    STN_AD = "0"

    # 뒤 3개
    BASIN  = toks[-1]
    LAW_ID = toks[-2]
    FCT_ID = toks[-3]

    # 중간: KO, EN
    mid = toks[8:-3]
    if not mid:
        STN_KO, STN_EN = "0", "0"
    else:
        STN_KO = mid[0]
        STN_EN = " ".join(mid[1:]) if len(mid) > 1 else "----"

    addr1, addr2, addr3 = "0", "0", "0"
    ORG_ADDR = raw

    tar_cur.execute(
        insert_sql,
        (STN_ID, LON, LAT, STN_SP, HT, HT_WD, LAU_ID, STN_AD,
         STN_KO, STN_EN, FCT_ID, LAW_ID, BASIN,
         addr1, addr2, addr3, ORG_ADDR)
    )
    cnt += 1

conn_tar.commit()
print(f"inserted rows: {cnt}")
tar_cur.close()
conn_tar.close()
