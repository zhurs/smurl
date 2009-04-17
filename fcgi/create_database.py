import smurl.db

def dbcreate():
    con = smurl.db.getcon()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS domains (
                    id integer primary key autoincrement,
                    domain varchar(100) not null,
                    max_url_id integer not null,
                    unique (domain)
                    )""")
    cur.execute("""REPLACE INTO domains (id, domain, max_url_id) values (0, 'smurl.ru', 1000)""")
    con.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS urls (
                    domain_id integer not null,
                    alias varchar(100) not null,
                    url_hash bigint unsigned not null,
                    url varchar(4096) not null,
                    unique (domain_id, alias)
                    )""")
    cur.execute("""CREATE INDEX IF NOT EXISTS idx_urls_duh on urls (domain_id, url_hash)""")

dbcreate()
