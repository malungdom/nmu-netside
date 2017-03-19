# -*- coding: utf-8 -*-
import os.path
import requests

from lektor.pluginsystem import Plugin
from jinja2 import Markup


class ExternalImagesPlugin(Plugin):
    name = u'External images'
    description = u'Downloads images into content on build'

    def on_setup_env(self):
        config = self.get_config()
        default_remote = config.get('config.default')
        content_path = os.path.join(self.env.root_path, 'content')
        for setup, remote_fn in config.iteritems():
            if setup.startswith('config.'):
                continue
            out_path, out_fn = setup.split('.', 1)
            new_path = os.path.sep.join((content_path, out_path, out_fn))
            new_path = os.path.normpath(new_path)
            if os.path.isfile(new_path):
                continue
            if not remote_fn:
                remote_fn = out_fn
            resource_uri = default_remote + remote_fn
            print "%s -> %s" % (resource_uri, new_path)
            response = requests.get(resource_uri)
            with open(new_path, 'wb') as fp:
                fp.write(response.content)
