
import mariadb
import sys
import os
import json

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

tar_cur = conn_tar.cursor()

json_path = r'C:\data\ts_data'

# ✅ 하위 폴더까지 재귀적으로 모든 .json 수집
json_file_list = []
for root, _, files in os.walk(json_path):
    for f in files:
        if f.lower().endswith('.json'):
            json_file_list.append(os.path.join(root, f))

print(f"found json files: {len(json_file_list)}")

insert_sql = """
INSERT INTO tb_cp(document_id, contents_title, sentence_id, sentence_title, sentence_text, json_data, create_dt)
VALUES (?,?,?,?,?,?,NOW())
"""

for file_path in json_file_list:
    print(f'json_file = {file_path}')

    # BOM 이슈 대비: utf-8-sig 권장
    with open(file_path, encoding='utf-8-sig') as json_file:
        json_dic = json.load(json_file)

    # 키 접근(없는 경우 대비해서 필요시 get으로 바꿔도 됨)
    document_id = json_dic['info'][0]['document_id']
    contents_title = json_dic['annotation'][0]['contents_title']
    sentence_id = json_dic['annotation'][0]['contents'][0]['sentence_id']
    sentence_title = json_dic['annotation'][0]['contents'][0]['sentence_title']
    sentence_text = json_dic['annotation'][0]['contents'][0]['sentence_text']

    tar_cur.execute(
        insert_sql,
        (document_id, contents_title, sentence_id, sentence_title, sentence_text, json.dumps(json_dic, ensure_ascii=False))
    )

# 성능/일관성 측면에서 루프 끝에 한 번 커밋
conn_tar.commit()
print('insert into tb_cp done')

tar_cur.close()
conn_tar.close()