import MySQLdb
import smurl.settings as settings

def getcon():
    return MySQLdb.connect(user="dbu_zhur_1",passwd="e6InK0BMfXz",db="db_zhur_1")

