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

import requests


DEBUG = os.environ.get('DEBUG')
TO_EMAIL = os.environ.get('TO_EMAIL')
BCC_EMAIL = os.environ.get('BCC_EMAIL')
SAVEFILE = os.environ.get('SAVEFILE', '/var/tmp/postings.txt')
TURNSTILE_SECRET_KEY = os.environ.get('TURNSTILE_SECRET_KEY')

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

def allowed_by_cloudflare_turnstile(token, meta):
    if not TURNSTILE_SECRET_KEY and token:
        return True
    try:
        response = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify',
                data={
                    'secret': TURNSTILE_SECRET_KEY,
                    'response': token,
                    'remoteip': meta['ip']
                })
        if DEBUG:
            stderr("Cloudflare Turnstile response: " + r.text)
        r = response.json()
        return r['success']
    except:
        # If we're having issues, let everything with a token through
        return bool(token)


# import cgitb; cgitb.enable()
form = cgi.FieldStorage()

_type = form.getfirst('_type', '')
token = form.getfirst('cf-turnstile-response', '')
meta = collections.OrderedDict(
    type=_type,
    turnstile_token=token,
    ip=os.environ.get('REMOTE_ADDR'),
    lang=os.environ.get('HTTP_ACCEPT_LANGUAGE'),
    time=datetime.utcnow().isoformat(),
    ua=os.environ.get('HTTP_USER_AGENT'))
data = collections.OrderedDict(_meta=meta)
first_value = ''
# fill in data gotten from form
for k in form.list:
    if k.name.startswith('_') or k.name.startswith('cf-turnstile'):
        continue
    data[k.name] = form.getfirst(k.name)
    if not first_value:
        first_value = data[k.name]

allowed = allowed_by_cloudflare_turnstile(token, meta)
data['_meta']['turnstile_allowed'] = allowed;

save_data(data, _type)
subject = first_value and first_value.splitlines()[0] or ''
if allowed or token:
    short_subj = ('' if allowed else 'SPAM: ') + subject[:64]
    send_email(data, _type, short_subj)
    redirect(form.getfirst('_next', ''), _type)
else:
    print(textwrap.dedent('''\
        X-test: yep

        <!doctype html>
        <meta charset=utf-8>
        <h1>Ikkje sendt</h1>
        Me trur du er ein «bot», diverre. :(
        Me orsakar so mykje om det er feil.
        Ta kontakt på epost eller via telefon
        dersom det er feil.''').format())
