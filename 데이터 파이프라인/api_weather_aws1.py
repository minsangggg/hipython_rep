# tb_weather_aws1.py
import os, csv, json, time, requests
from datetime import datetime, timedelta, timezone
import mariadb

# ========= 설정 =========
RUN_FOREVER = True  # 한 번만 실행하려면 False
API_KEY = os.getenv("KMA_API_KEY") or "uXEt-y3SSYqxLfst0gmKTA"  # 환경변수 우선, 없으면 하드코드 키 사용
BASE_URL = "https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min"
PARAMS_BASE = {"stn": "0", "disp": "1", "help": "2"}  # CSV + 값만(컬럼 헤더 1줄)

DB = dict(user="lguplus7", password="lg7p@ssw0rd~!", host="localhost", port=3310, database="cp_data")

UPSERT_SQL = """
INSERT INTO tb_weather_aws1
(yyyymmddhhmi, stn, wd1, ws1, wds, wss, wd10, ws10, ta, re,
 rn_15m, rn_60m, rn_12h, rn_day, hm, pa, ps, td, org_data, update_dt)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE
  wd1=VALUES(wd1), ws1=VALUES(ws1), wds=VALUES(wds), wss=VALUES(wss),
  wd10=VALUES(wd10), ws10=VALUES(ws10), ta=VALUES(ta), re=VALUES(re),
  rn_15m=VALUES(rn_15m), rn_60m=VALUES(rn_60m), rn_12h=VALUES(rn_12h), rn_day=VALUES(rn_day),
  hm=VALUES(hm), pa=VALUES(pa), ps=VALUES(ps), td=VALUES(td),
  org_data=VALUES(org_data), update_dt=VALUES(update_dt);
"""

def fetch_csv_for_minute(kst_min_dt: datetime) -> str:
    """tm1=tm2=해당분, 전 지점(stn=0) CSV 응답"""
    tm = kst_min_dt.strftime("%Y%m%d%H%M")
    params = {**PARAMS_BASE, "authKey": API_KEY, "tm1": tm, "tm2": tm}
    r = requests.get(BASE_URL, params=params, timeout=30)
    r.raise_for_status()
    return r.text

# 1) DictReader 대신, 포지션 기반 파서로 교체
def parse_csv_positional(text: str):
    """
    KMA 응답이 컬럼명 없이 값만 올 때(지금 상황) 안전하게 파싱.
    예상 컬럼 순서(전 지점 매분): 
    [YYMMDDHHMI, STN, WD1, WS1, WDS, WSS, WD10, WS10, TA, RE,
     RN-15m, RN-60m, RN-12H, RN-DAY, HM, PA, PS, TD, (= 품질표시?)]
    뒤의 '=' 같은 품질표시는 버림.
    """
    rows = []
    for ln in text.splitlines():
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        # CSV 분리
        parts = [p.strip() for p in ln.split(",")]
        # 데이터 라인 판정: 첫 값이 12자리 숫자(yyyymmddhhmi)
        if not (len(parts) >= 18 and parts[0].isdigit() and len(parts[0]) == 12):
            # 헤더/설명 라인은 스킵
            continue

        # '=' 같은 마지막 토큰은 버림
        if parts[-1] == "=":
            parts = parts[:-1]

        # 필요한 18개까지만 사용
        parts = parts[:18]

        # 포지션 매핑
        row = {
            "YYMMDDHHMI": parts[0],
            "STN":        parts[1],
            "WD1":        parts[2],
            "WS1":        parts[3],
            "WDS":        parts[4],
            "WSS":        parts[5],
            "WD10":       parts[6],
            "WS10":       parts[7],
            "TA":         parts[8],
            "RE":         parts[9],
            "RN-15m":     parts[10],
            "RN-60m":     parts[11],
            "RN-12H":     parts[12],
            "RN-DAY":     parts[13],
            "HM":         parts[14],
            "PA":         parts[15],
            "PS":         parts[16],
            "TD":         parts[17],
        }
        rows.append(row)
    return rows


def get_api(row: dict, *keys: str, default="0"):
    """RN-60m/RN_60m 등 표기 차이를 흡수"""
    for k in keys:
        if k in row and row[k] != "":
            return row[k]
    return default

def zpad4(v: str) -> str:
    return str(v).zfill(4)

def run_once():
    # 직전 분(반영 지연 방지)
    kst = timezone(timedelta(hours=9))
    target = datetime.now(tz=kst).replace(second=0, microsecond=0) - timedelta(minutes=1)
    ymdhm = target.strftime("%Y%m%d%H%M")

    raw = fetch_csv_for_minute(target)
    rows = parse_csv_positional(raw)
    
    if rows:
        print(rows[0].keys())
        print(rows[0])
        
    if not rows:
        print(f"[EMPTY] {ymdhm}")
        return

    # 첫 실행 때 헤더 한번 확인(필요시 주석 해제)
    # print("[HEADER]", ",".join(rows[0].keys()))

    payload = []
    for r in rows:
        # API 헤더명 → DB 컬럼 순서로 값 매핑
        stn = zpad4(get_api(r, "STN"))
        wd1 = get_api(r, "WD1")
        ws1 = get_api(r, "WS1")
        wds = get_api(r, "WDS")
        wss = get_api(r, "WSS")
        wd10 = get_api(r, "WD10")
        ws10 = get_api(r, "WS10")
        ta = get_api(r, "TA")
        re_ = get_api(r, "RE")
        rn_15m = get_api(r, "RN-15m", "RN_15m")
        rn_60m = get_api(r, "RN-60m", "RN_60m")
        rn_12h = get_api(r, "RN-12H", "RN-12h", "RN_12h")
        rn_day = get_api(r, "RN-DAY", "RN_day")
        hm = get_api(r, "HM")
        pa = get_api(r, "PA")
        ps = get_api(r, "PS")
        td = get_api(r, "TD")

        org_json = json.dumps(r, ensure_ascii=False)

        payload.append((
            ymdhm, stn, wd1, ws1, wds, wss, wd10, ws10, ta, re_,
            rn_15m, rn_60m, rn_12h, rn_day, hm, pa, ps, td, org_json, ymdhm
        ))

    with mariadb.connect(**DB) as conn:
        cur = conn.cursor()
        cur.executemany(UPSERT_SQL, payload)
        conn.commit()
        print(f"[UPSERT] {ymdhm} rows={len(payload)}")

if __name__ == "__main__":
    # 중복 방지 유니크 키 권장(수동 적용)
    #   ALTER TABLE tb_weather_aws1 ADD UNIQUE KEY uq_time_stn (yyyymmddhhmi, stn);
    run_once()
    if RUN_FOREVER:
        while True:
            # 매분 정각 정렬
            now = datetime.now()
            time.sleep(max(1, 60 - now.second))
            run_once()
 