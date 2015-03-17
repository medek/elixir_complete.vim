# Copyright (c) 2014, Gavin Massey <mdk@mystacktrace.org>
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
import time
import socket
from . import utils
from . import server_list
from . import message

class ECClient(object):
    def __init__(self, user_options):
        self._server_meta = {'project root': user_options['project root']}
        self._plugin_root = user_options['plugin root']
        self._user_notified_about_crash = False
        self._server_stdout = None
        self._server_stderr = None
        self._server_socket = None
        self._server_popen = None
        self._server_list = server_list.ServerList(os.path.join(self._plugin_root, "config/server_list.json"))
        self._setup_server()

    def _new_server(self):
        server_port = utils.get_unused_port()
        args = [ utils.path_to_server(), '--port={0}'.format(server_port),
                '--root={0}'.format(self._server_meta['project root'])]
 
        #until elixir_complete get's a LoggerFileBackend, just eat up std{in,out}
        with open(os.devnull, "w") as fnull:
            print "launching server"
            self._server_popen = utils.safe_popen(args, stdout =fnull, stderr =fnull)

        self._server_socket = utils.loop_connect(server_port, 5)

        self._server_meta['port'] = server_port
        self._server_meta['cache'] = False
        self._server_list.add_server(self._server_meta)

    def _setup_server(self):
        srv = self._server_list.server_running(self._server_meta['project root'])
        print srv
        if srv != None:
            try:
                self._server_socket = socket.create_connection(('localhost', srv['port']))
                self._server_meta = srv
                return
            except socket.error:
                print "couldn't connect to existing server (dead?)"
        self._new_server()

    def is_server_alive(self):
        return message.is_alive(self._server_socket)

    def _server_cleanup(self):
        if self.is_server_alive():
            message.halt_server(self._server_socket)
            self._server_socket.close()

    def restart_server(self):
        self._server_cleanup()
        self._setup_server()

    def line_complete(self, line, column, filename, string):
        message.line_complete(self._server_socket,
                              line, column, filename, string)
