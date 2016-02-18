from __future__ import absolute_import
from __future__ import unicode_literals
from website.settings import *
from website.settings.local import *

INSTALLED_APPS += ['sendfile']

WIKI_ATTACHMENTS_USE_SENDFILE = True


SENDFILE_BACKEND = 'sendfile.backends.development'
# SENDFILE_URL = None #Not needed
# SENDFILE_ROOT = None #Not needed
