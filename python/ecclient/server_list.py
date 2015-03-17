# Copyright (c) 2015, Gavin Massey <mdk@mystacktrace.org>
# 
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
import os
import tempfile
import json
from . import utils
# a single server entry is just:
# {'project root': path, 'port': int, 'cache': boolean}
# If syncing and whatnot becomes a problem I'll just backend this with sqlite

class ServerList(object):
    def __init__(self, fileloc):
        self._fileloc = fileloc
        self._servers = self.read_file()

    def read_file(self):
        try:
            f = open(self._fileloc, 'rb')
        except IOError:
            print "Couldn't get server list at {0}".format(fileloc)
            return []

        srv = json.load(f)
        f.close()
        if len(srv) > 0:
            srv = [s for s in srv if utils.test_connection(s['port'])]

        return srv

    def add_server(self, server):
        self._servers += [server]
        return self.write_file()

    def remove_server(self, server):
        self._servers = [srv for srv in self._servers if server == srv]
        return self.write_file()

    def write_file(self):
        try:
            f = tempfile.NamedTemporaryFile(dir=os.path.dirname(self._fileloc),
                                            delete=False)
            json.dump(self._servers, f)
            f.close()
            utils.atomic_rename(f.name, self._fileloc)
        except IOError:
            print "Couldn't open {0} for writing".format(fileloc)
            return False
        return True

    def server_running(self, project_root):
        for x in self._servers:
            if x['project root'] == project_root:
                return x
        return None

