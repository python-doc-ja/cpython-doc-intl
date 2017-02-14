#!/usr/bin/env python
# coding: utf-8

from __future__ import with_statement

import os
from glob import glob
import gdata.projecthosting.client # install from google

# 実際に利用するときは DRY = 0 にする.
DRY = 1

# 登録しようとしている issue に統一して付ける label
DEFAULT_LABELS = ["Type-Task", "Milestone-26ja2", "Target-2.6.6"]

_USER = 'example@gmail.com'
_PASSWORD = 'secretstring'

_client = None

def get_client(user=None, password=None):
    global _client
    if _client is None:
        _client = _create_client(user, password)
    return _client

def _create_client(user=None, password=None):
    """Build a ProjectHostingClinet object from ``settings.USER``
    and ``settings.PASSWORD``."""

    user = user or _USER
    password = password or _PASSWORD

    client = gdata.projecthosting.client.ProjectHostingClient()
    client.client_login(user, password,
                        source='PyDocJa Batch Issue Creater',
                        service='code')
    return client

def register_issue(module, title, client=None):
    client = client or get_client()
    issue_title = u"%s/%s の翻訳 (2.6.6)" % (module, title)
    client.add_issue('python-doc-ja', issue_title, issue_title, "---",
                    labels=DEFAULT_LABELS + ['Module-' + module.title()])

def usage(exit=False):
    print "Usage: register_issue.py directory_contains_diff module_name"
    print "Example: register_issue.py diff/library library"
    if exit:
        import sys
        sys.exit()

def main():
    import sys
    if len(sys.argv) != 3:
        usage(True)
    from glob import iglob
    mod_name = sys.argv[2]
    print >>sys.stderr, "Registering module:", mod_name
    for diff_file in iglob(sys.argv[1] + '/*.rst.diff'):
        name = os.path.basename(diff_file)[:-9]
        print >>sys.stderr, "Registering:", name
        if not DRY:
            register_issue(mod_name, name)

if __name__ == '__main__':
    main()
