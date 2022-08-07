#!/usr/bin/env python3
import os
import subprocess
import sys
from http.server import HTTPServer
from http.server import CGIHTTPRequestHandler

# If you want to test/develop the CGI scripts, just run this:
#   ./run_cgi.py
# And go to http://127.0.0.1:9999
# cgi-scripts runs, their output shown in your terminal

#set DEBUG env var
os.environ['DEBUG'] = '1'

if len(sys.argv) <= 1:
    out_dir = subprocess.check_output(
        ['lektor', 'project-info', '--output-path'])
else:
    out_dir = sys.argv[1]
os.chdir(out_dir.strip())
for script in os.listdir('cgi-bin'):
    os.chmod('cgi-bin/%s' % script, 0o777)

PORT = 9999

httpd = HTTPServer(('', PORT), CGIHTTPRequestHandler)
print('serving at port', PORT)
httpd.serve_forever()
