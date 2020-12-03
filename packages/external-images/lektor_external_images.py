# -*- coding: utf-8 -*-
import os.path
import requests

from lektor.pluginsystem import Plugin
from jinja2 import Markup


class ExternalImagesPlugin(Plugin):
    name = u'External images'
    description = u'Downloads images into content on build'

    def on_setup_env(self, extra_flags):
        print(extra_flags)
        config = self.get_config()
        default_remote = ''
        content_path = os.path.join(self.env.root_path, 'content')
        for setup, remote_fn in config.iteritems():
            out_path, out_fn = setup.split('.', 1)
            if out_fn == 'default':
                default_remote = remote_fn;
                continue
            new_path = os.path.sep.join((content_path, out_path, out_fn))
            new_path = os.path.normpath(new_path)
            if os.path.isfile(new_path):
                continue
            if not remote_fn:
                remote_fn = out_fn
            resource_uri = remote_fn
            if 'http' not in resource_uri:
                resource_uri = default_remote + resource_uri
            print("{} -> {}".format(resource_uri, new_path))
            response = requests.get(resource_uri)
            with open(new_path, 'wb') as fp:
                fp.write(response.content)
