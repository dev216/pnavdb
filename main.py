import re
import sqlite3


class PNavDb:
    pass


db = sqlite3.connect("pnav.db")
db_cursor = db.cursor()
db_cursor.execute('''SELECT name FROM sqlite_master
                     WHERE type IN ('table','view')
                     AND name NOT LIKE 'sqlite_%'
                     UNION ALL
                     SELECT name FROM sqlite_temp_master
                     WHERE type IN ('table','view')
                     ORDER BY 1''')
table_name_tuple_list = db_cursor.fetchall()
pnavDb = PNavDb()
pnavDb.table_names = []
for table_name_tuple in table_name_tuple_list:
    table_name = table_name_tuple[0]
    pnavDb.table_names.append(table_name)
print(pnavDb.table_names)

db_cursor.execute('''SELECT sql FROM
                         (SELECT * FROM sqlite_master UNION ALL
                          SELECT * FROM sqlite_temp_master)
                     WHERE type != 'meta'
                     ORDER BY  tbl_name, type DESC, name''')
db_info = db_cursor.fetchall()
table_info_re = re.compile(r"^CREATE TABLE (\w+)(\s?)(\(.*\))")
for a_table_info in db_info:
    tmp_table_info = a_table_info[0]
    table_info_matcher = table_info_re.match(tmp_table_info)
    if table_info_matcher != None:
        # print(table_info_matcher)
        # print(table_info_matcher.group())
        table_name = table_info_matcher.group(1)
        # print(table_name)
        table_descr = table_info_matcher.group(3)
        table_descr = re.sub("\(", "", table_descr)
        table_descr = re.sub("\)", "", table_descr)
        table_descr = re.sub("\s+", " ", table_descr)
        print(table_descr.strip())
        table_columns_list_descr = re.split(",", table_descr)
        for a_table_column_descr in table_columns_list_descr:
            table_column_parts = re.split(" ", a_table_column_descr.strip())
            table_column_name = table_column_parts[0]
            print(table_column_name)

db_cursor.close()
db.close()
