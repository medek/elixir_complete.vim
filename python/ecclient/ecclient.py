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

class ECClient(object):
    def __init__(self, user_options):
        self._user_options = user_options
        self._user_notified_about_crash = False
        self._server_stdout = None
        self._server_stderr = None
        self._server_popen = None
        self._server_socket = None
        self._setup_server()

    def _setup_server(self):
        #TODO:Attempt to reconnect if there's an existing server for the dir
        server_port = utils.get_unused_port()
        print server_port
        args = [ utils.path_to_server(), '--port={0}'.format(server_port),
                 '--root={0}'.format(self._user_options['project root'])]
        #until elixir_complete get's a LoggerFileBackend, just eat up std{in,out}
        with open(os.devnull, "w") as fnull:
            self._server_popen = utils.safe_popen(args, stdout =fnull, stderr =fnull)
        time.sleep(1) #need to sleep so elixir_complete has time to listen
        self._server_socket = socket.create_connection(('localhost', server_port), timeout=5000)

    def is_server_alive(self):
        ret = self._server_popen.poll()
        return ret is None

    def server_pid(self):
        if not self._server_popen:
            return -1 #I hope nobody tries to use this in a kill command!
        return self._server_popen.pid

    def _server_cleanup(self):
        if self.is_server_alive():
            self._server_socket.close()
            self._server_popen.terminate()

    def restart_server(self):
        self._server_cleanup()
        self._setup_server()

