import smurl.db

def dbcreate():
    con = smurl.db.getcon()
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS domains (
                    domain_id int unsigned not null primary key auto_increment,
                    domain varchar(100) not null,
                    max_url_id int unsigned not null,
                    unique key (domain)
                    ) ENGINE=InnoDB""")
    cur.execute("""REPLACE INTO domains (domain_id, domain, max_url_id) values (0, 'smurl.ru', 1000)""")
    con.commit()
    cur.execute("""CREATE TABLE IF NOT EXISTS urls (
                    domain_id int unsigned not null,
                    alias varchar(100) not null,
                    url_hash bigint unsigned not null,
                    url varchar(4096) not null,
                    unique (domain_id, alias),
                    index (domain_id, url_hash)
                    ) ENGINE=InnoDB""")

dbcreate()
