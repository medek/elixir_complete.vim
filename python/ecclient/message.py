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
import socket
import json

def halt_server(sock):
    try:
        sock.send('HaltServer\n')
    except socket.error: #eh, it's probably dead :P
        return True
    else:
        ret = json.loads(sock.recv(4096))
        return ret['result'] == 'ok'

def is_alive(sock):
    try:
        sock.send('IsAlive\n')
    except socket.error:
        return False
    else:
        ret = json.loads(sock.recv(4096))
        return ret['result'] == 'ok'

def line_complete(sock, line, column, filename, string):
    try:
        request = json.dumps({'file': filename, 'line':line,
                              'column':column, 'string':string})

        sock.send('LineComplete {0}\n'.format(request))
    except socket.error:
        return None
    else:
        ret = json.loads(sock.recv(4096))
        if ret['result'] != 'ok':
            return None
        return ret['completion']
