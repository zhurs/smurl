import sys, os
import re, md5, cgi

sys.path.insert(0, '/home/zhur/www/site1/webapp/ext/json-py')
sys.path.insert(0, '/home/zhur/www/site1/webapp')
import json

import smurl.settings as settings
import smurl.db, smurl.code

def smurl_app(environ, start_response):
    form = cgi.FieldStorage(environ = environ)
    request_uri = environ['REQUEST_URI']
    if request_uri.startswith('/api/'):
        return cmd_smurl_api(environ, start_response)
    else:
        return cmd_smurl_redirect(environ, start_response)

def cmd_smurl_redirect(environ, start_response):
    con = smurl.db.getcon()
    cur = con.cursor()

    environ['HTTP_HOST'] = environ['HTTP_HOST'].replace('1.zhur.cz8.ru', 'smurl.ru') 

    cur.execute("SELECT domain_id FROM domains WHERE domain = %s", [environ['HTTP_HOST'].lower()])
    row = cur.fetchone()
    url = ''
    if row:
        domain_id = row[0]

        alias = smurl.code.clean(environ['REQUEST_URI']);
        cur.execute("SELECT url FROM urls WHERE domain_id = %s and alias = %s", [domain_id, alias])
        row = cur.fetchone()
        if row:
            url = str(row[0])

    if url != '':
        start_response('302 Moved', [('Location', str(row[0]))])
    else:
        start_response('404 Not Found', [])

    return []

def cmd_smurl_api(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(environ=environ)

    errors = []

    domain = 'smurl.ru'
    subdomain = form.getfirst('subdomain', '').lower()
    if subdomain != '':
        if re.match(r"^[a-zA-Z0-9-]+$", subdomain):
            domain = subdomain + '.' + domain
        else:
            errors.append('incorrect subdomain "%s"' % subdomain)

    alias = form.getfirst('alias', '')
    if alias != '' and not re.match(r"^[a-zA-Z0-9-]+$", alias):
        errors.append('incorrect alias "%s"' % alias)

    url = form.getfirst('url', '')
    if not re.match(r'^https?:\/\/((\d+\.){3}\d+|([a-zA-Z0-9-]+\.)+[a-z]{2,10})(:\d+)?($|#|\/|\?)', url):
        errors.append('incorrect url "%s"' % url)

    if len(errors) == 0:
        con = smurl.db.getcon()
        cur = con.cursor()

        domain_row = get_domain(con, domain)

        if alias != '':
            cur.execute("SELECT url FROM urls WHERE domain_id = %s and alias = %s", [domain_row['domain_id'], alias])
            row = cur.fetchone()
            if row == None:
                add_url(con, url, domain_row['id'], alias)
            elif row[0] != url:
                errors.append('alias already busy "%s"' % alias)
        else:
            alias = add_url_auto(con, url, domain_row['domain_id'], domain_row['max_url_id'])
            if alias == '':
                error.append('cant find free alias')

    if len(errors):
        return [json.JsonWriter().write({'errors': errors})]
    else:
        small_url = 'http://%s/%s' % (domain, alias)
        return [json.JsonWriter().write({'smurl': small_url.encode("latin1")})]

def get_domain(con, domain):
    cur = con.cursor()
    cur.execute("SELECT domain_id, max_url_id FROM domains WHERE domain = %s", [domain])
    row = cur.fetchone()
    if row == None:
        cur.execute("INSERT INTO domains (domain, max_url_id) VALUES (%s, 0)", [str(domain)])
        con.commit()
        return dict(domain_id = con.lastinsertid, max_url_id = 0)
    else:
        return dict(domain_id = row[0], max_url_id = row[1])

def get_url_hash(url):
    return long(md5.new(url).hexdigest(), 16) % 2**32

def add_url(con, url, domain_id, alias):
    cur = con.cursor()
    url_hash = get_url_hash(url)
    cur.execute("INSERT INTO urls (domain_id, alias, url_hash, url) VALUES (%s, %s, %s, %s)", [domain_id, alias, url_hash, url])
    con.commit()
    return alias

def add_url_auto(con, url, domain_id, max_url_id):
    cur = con.cursor()
    url_hash = get_url_hash(url)
    cur.execute("SELECT alias FROM urls WHERE domain_id = %s and url_hash = %s", [domain_id, url_hash])
    row = cur.fetchone()
    if row != None:
        alias = row[0]
    else:
        alias = ''
        for j in range(100):
            max_url_id = max_url_id + 1
            try_alias = smurl.code.encode(max_url_id)
            try:
                cur.execute("INSERT INTO urls (domain_id, alias, url_hash, url) VALUES (%s, %s, %s, %s)", [domain_id, try_alias, url_hash, url])
                alias = try_alias
                break
            except:
                None
        cur.execute("UPDATE domains SET max_url_id = %s WHERE domain_id = %s", [max_url_id, domain_id])
        con.commit()
    return alias

application = smurl_app
#WSGIServer(smurl_app, bindAddress = settings.SOCK, umask = 0, multithreaded=False, multiprocess=False).run()
