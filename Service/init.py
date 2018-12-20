import sqlite3

from Service import BaseService

db_path = BaseService.get_db_path()

conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS paste
          (id BIGINT PRIMARY KEY  AUTOINCREMENT NOT NULL,
          token  VARCHAR(8)  NOT NULL,
          poster VARCHAR(30) default '',
          secret TINYINT NOT NULL default 0,
          expire 
          ;''')
conn.commit()
conn.close()
