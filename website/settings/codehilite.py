from __future__ import absolute_import
from __future__ import unicode_literals
from website.settings import *
from website.settings.local import *

# Test codehilite with pygments

WIKI_MARKDOWN_KWARGS = {
    'extensions': [
        'codehilite',
        'footnotes',
        'attr_list',
        'headerid',
        'extra',
    ]}
