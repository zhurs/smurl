from flup.server.fcgi import WSGIServer
import json
import os
import smurl.settings as settings
import smurl.db, smurl.code
import md5, cgi

def smurl_app(environ, start_response):
    form = cgi.FieldStorage(environ = environ)
    request_uri = environ['REQUEST_URI']
    if request_uri.startswith('/api/'):
        return cmd_smurl_api(environ, start_response)
    else:
        return cmd_smurl_redirect(environ, start_response)

def cmd_smurl_redirect(environ, start_response):
    url_id = smurl.code.smurl_decode(environ['REQUEST_URI'])

    con = smurl.db.getcon()
    cur = con.cursor()
    cur.execute("SELECT url FROM smurl WHERE id = ?", [url_id])
    row = cur.fetchone()

    if row:
        start_response('302 Moved', [('Location', str(row[0]))])
    else:
        start_response('404 Not Found')

    return []

def cmd_smurl_api(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(environ=environ)

    url = form.getvalue('url')
    url_hash = long(md5.new(url).hexdigest(), 16) % 2**32

    con = smurl.db.getcon()
    cur = con.cursor()
    cur.execute("SELECT id FROM smurl WHERE url_hash = ?", [url_hash])
    row = cur.fetchone()

    if row:
        url_id = row[0]
    else:
        cur.execute("INSERT INTO smurl (url_hash, url) VALUES (?, ?)", [url_hash, url])
        con.commit()
        url_id = cur.lastrowid

    small_url = 'http://smurl.ru/%s' % smurl.code.smurl_encode(url_id)
    return [json.JsonWriter().write({'smurl': small_url})]

WSGIServer(smurl_app, bindAddress = settings.SOCK, umask = 0, multithreaded=False, multiprocess=False).run()
