import smurl.db

def dbcreate():
    cur = smurl.db.getcur()
    cur.execute("""CREATE TABLE IF NOT EXISTS smurl (
                    id integer primary key autoincrement,
                    url_hash bigint unsigned not null,
                    url varchar(4096) not null,
                    unique (url_hash)
                    )""")

dbcreate()
