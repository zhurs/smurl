from pysqlite2 import dbapi2 as sqlite
import smurl.settings as settings

def getcon():
    return sqlite.connect(settings.DB)

def getcur():
    con = sqlite.connect(settings.DB)
    return con.cursor()

