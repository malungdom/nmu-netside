#!/usr/bin/env python3
import cgi
import collections
import os
import subprocess
import textwrap
from datetime import datetime


def _c(cmd):
    return subprocess.check_output(cmd, shell=True, timeout=20000)

def update():
    upd = _c('sudo -Hu nmu /home/nmu/malungdom-staging-to-prod.sh')
    print(textwrap.dedent('''\
        X-Status: OK

        OK

        %s''') % upd.decode('utf-8'))

# import cgitb; cgitb.enable()
form = cgi.FieldStorage()

meta = collections.OrderedDict(
    ip=os.environ.get('REMOTE_ADDR'),
    lang=os.environ.get('HTTP_ACCEPT_LANGUAGE'),
    time=datetime.utcnow().isoformat(),
    ua=os.environ.get('HTTP_USER_AGENT'))

if os.environ['REQUEST_METHOD'] == 'POST':
    update()
else:
    print('\n\nNothing')
