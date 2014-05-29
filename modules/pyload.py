from flask import jsonify, render_template, request, send_file, json
import urllib2
import urllib
import base64
import StringIO

import sys

from maraschino import app
from maraschino.tools import *
import maraschino

def pyload_http():
    if get_setting_value('pyload_https') == '1':
        return 'https://'
    else:
        return 'http://'


def pyload_url():
    port = get_setting_value('pyload_port')
    url_base = get_setting_value('pyload_ip')
    webroot = get_setting_value('pyload_webroot')

    if port:
        url_base = '%s:%s' % (url_base, port)

    if webroot:
        url_base = '%s/%s' % (url_base, webroot)

    url = '%s/api/' % (url_base)

    return pyload_http() + url


def pyload_url_no_api():
    port = get_setting_value('pyload_port')
    url_base = get_setting_value('pyload_ip')
    webroot = get_setting_value('pyload_webroot')

    if port:
        url_base = '%s:%s' % (url_base, port)

    if webroot:
        url_base = '%s/%s' % (url_base, webroot)

    return pyload_http() + url_base

def pyload_api(params=None, use_json=True, dev=False):
    url = 'http://localhost:8000/api/' + method    
    data = urllib.urlencode(params)
    u = urllib.urlopen(url, data)
    json_data = u.read()
    data = json.JSONDecoder().decode(json_data)
    logger.log('pyload_api::Finshed reading from pyLoad', 'DEBUG')
    return data

@app.route('/xhr/pyload')
@requires_auth
def xhr_pyload():
    params = '/statusServer'

    pyload = pyload_api(params)

    print("statusServer - " + pyload.length + "\n")

    return render_template('pyload.html',
        url=pyload_url_no_api(),
        app_link=pyload_url_no_api(),
        pyload=pyload
    )

@app.route('/xhr/pyload/kill')
def kill():
    params = '/kill'

    try:
        pyload = pyload_api(params)
    except:
        raise Exception

    return pyload['message']

@app.route('/xhr/pyload/restart')
def restart():
    params = '/restart'
    try:
        pyload = pyload_api(params)
    except:
        raise Exception

    return pyload
