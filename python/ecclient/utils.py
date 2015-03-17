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
import sys
import socket
import subprocess
import time

def on_windows():
    return sys.platform == 'win32'

def on_cygwin():
    return sys.platform == 'cygwin'

def get_unused_port():
    sock = socket.socket()
    sock.bind(('',0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def path_to_server():
    dir_of_current_script = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(dir_of_current_script, '../../extern/elixir_complete/elixir_complete')

def safe_popen(*args, **kwargs):
    if kwargs.get('stdin') is None:
        kwargs['stdin'] = subprocess.PIPE if on_windows() else None

    return subprocess.Popen(*args, **kwargs)

#Doesn't work on windows
def pid_active(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True

def test_connection(port):
    try:
        sock = socket.create_connection(('localhost', port))
    except socket.error:
        return False
    else:
        sock.close()
        return True

def loop_connect(port, timeout):
    start = time.time()
    sock = None
    loop = True
    while loop:
        try:
            sock = socket.create_connection(('localhost', port))
        except socket.error:
            if time.time() - start > timeout:
                return None
        else:
            return sock

    return sock

def atomic_rename(src, dest):
    #Here's where things get weird
    #Need to use kernel32.MoveFileEx for atomic move operations
    #And even then it might not be atomic...
    #TODO: Find out if this actually works on windows :P
    if on_windows():
        from ctypes import *
        #0x1 == MOVEFILE_REPLACE_EXISTING
        ret = windll.kernel32.MoveFileExW(c_wchar_p(src), c_wchar_p(dest), c_uint(0x1))
        if ret == 0:
            print "Something went wrong talking to windows..."
            return False
        else:
            return True
    else:
        try:
            os.rename(src, dest)
        except OSError:
            print "Error renaming file"
            return False
        else:
            return True
