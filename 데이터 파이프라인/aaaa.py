import duckdb
import os
import pandas as pd

duck_con = duckdb.connect(r"c:\data\mart_top_cate3_by_addr3.duckdb")



duck_con.sql("SELECT COUNT(1) AS cnt FROM tb_smb_file").show()
duck_con.sql('SELECT * FROM tb_smb_file LIMIT 10').show()