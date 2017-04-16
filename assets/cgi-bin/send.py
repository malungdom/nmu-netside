#!/usr/bin/env python3
import cgi
import collections
import json
import os
import re
import smtplib
import textwrap
from datetime import datetime
from email.message import EmailMessage
from urllib.parse import urlsplit


TO_EMAIL = os.environ['TO_EMAIL']
BCC_EMAIL = os.environ.get('BCC_EMAIL')
SAVEFILE = os.environ.get('SAVEFILE', '/var/tmp/postings.txt')


def save_data(data, realm):
    with open(SAVEFILE, 'a') as f:
        f.write(json.dumps(data, indent=2))


def send_email(data, realm, subject):
    if not subject:
        # Not worth sending then
        return
    msg = EmailMessage()
    msg['Subject'] = '[netside:%s] %s' % (realm, subject)
    msg['From'] = 'noreply@nynorsk.no'
    msg['To'] = TO_EMAIL
    msg['Bcc'] = BCC_EMAIL
    body = ['%s:  %s' % (k, v) for k, v in data.items() if k[0] != '_']
    msg.set_content(textwrap.dedent("""\
    %s

    -- netsida
    """) % '\n'.join(body))
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)


def redirect(location, type_):
    if not location and 'HTTP_REFERER' in os.environ:
        location = urlsplit(os.environ['HTTP_REFERER'], 'http').path
    location = re.sub(r'[^\w/]', '', location or '/')
    if type_:
        location += '?%s=1' % type_
    print(textwrap.dedent('''\
        Location: %s

        Redir.''') % location)


# import cgitb; cgitb.enable()
form = cgi.FieldStorage()

_type = form.getfirst('_type', '')
meta = collections.OrderedDict(
    type=_type,
    ip=os.environ.get('REMOTE_ADDR'),
    lang=os.environ.get('HTTP_ACCEPT_LANGUAGE'),
    time=datetime.utcnow().isoformat(),
    ua=os.environ.get('HTTP_USER_AGENT'))
data = collections.OrderedDict(_meta=meta)
first_value = ''
# fill in data gotten from form
for k in form.list:
    if k.name.startswith('_'):
        continue
    data[k.name] = form.getfirst(k.name)
    if not first_value:
        first_value = data[k.name]

save_data(data, _type)
send_email(data, _type, first_value)
redirect(form.getfirst('_next', ''), _type)
