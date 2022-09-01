#!/usr/bin/env python3
import cgi
import collections
import json
import os
import pprint
import re
import smtplib
import sys
import textwrap
from datetime import datetime
from email.message import EmailMessage
from urllib.parse import urlsplit


DEBUG = os.environ.get('DEBUG')
TO_EMAIL = os.environ.get('TO_EMAIL')
BCC_EMAIL = os.environ.get('BCC_EMAIL')
SAVEFILE = os.environ.get('SAVEFILE', '/var/tmp/postings.txt')
if not DEBUG and not TO_EMAIL:
    raise Exception('Must set DEBUG or TO_EMAIL')


def stderr(msg):
    pprint.pprint(msg, stream=sys.stderr)


def save_data(data, realm):
    stderr(data)
    with open(SAVEFILE, 'a') as f:
        f.write(json.dumps(data, indent=2))


def send_email(data, realm, subject):
    if not subject:
        # Not worth sending then
        return
    msg = EmailMessage()
    msg['Subject'] = '[Nettsida: %s] %s' % (realm, subject)
    msg['From'] = 'norsk+fosse@malungdom.no'
    msg['To'] = TO_EMAIL
    body = ['%s:  %s' % (k, v) for k, v in data.items() if k[0] != '_']
    msg.set_content(textwrap.dedent("""\
    %s

    -- nettsida
    """) % '\n'.join(body))
    from_email = data.get('epost', data.get('email'))
    if from_email:
        msg['Reply-To'] = from_email
    if DEBUG:
        stderr(msg.as_string())
        return
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg, to_addrs=[TO_EMAIL, BCC_EMAIL])


def redirect(location, success):
    if not location and 'HTTP_REFERER' in os.environ:
        location = urlsplit(os.environ['HTTP_REFERER'], 'http').path
    location = re.sub(r'[^\w/-]', '', location or '/')
    if success:
        location += '?success=%s' % success
    print(textwrap.dedent('''\
        Location: {loc}

        Redir to: {loc}''').format(loc=location))


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
subject = first_value and first_value.splitlines()[0] or ''
send_email(data, _type, subject[:64])
redirect(form.getfirst('_next', ''), _type)
