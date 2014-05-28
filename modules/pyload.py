from flask import jsonify, render_template, request, send_file, json
import urllib2
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
    username = get_setting_value('pyload_user')
    password = get_setting_value('pyload_password')

    url = pyload_url() + params
    r = urllib2.Request(url)
    
    sys.exit(r)
# fix the login process here.


# if im not logged in, login.
# then execute the desired api command.

    if username and password:
        base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
        r.add_header("Authorization", "Basic %s" % base64string)

    data = urllib2.urlopen(r).read()
    if dev:
        print url
        print data
    if use_json:
        data = json.JSONDecoder().decode(data)
    return data

@app.route('/xhr/pyload/')
def xhr_pyload():
    params = '/statusServer'

    try:
        pyload = pyload_api(params)

        if pyload['result'].rfind('success') >= 0:
            pyload = pyload['data']
            for time in pyload:
                for episode in pyload[time]:
                    episode['image'] = get_pic(episode['tvdbid'], 'banner')
    except:
        return render_template('pyload.html',
            pyload=pyload,
        )

    return render_template('pyload.html',
        url=pyload_url_no_api(),
        app_link=pyload_url_no_api(),
        pyload=pyload
    )


@app.route('/xhr/pyload/add_files/<pid>/<links>')
def add_files():
    params = '/addFiles/%s/%s' % (pid, links)
    
    try:
        pyload = pyload_api(params)
    except:
        raise Exception

    return pyload['message']


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

    return pyload['message']
