"Copyright (c) 2014, Gavin Massey <mdk@mystacktrace.org>
"
"Permission to use, copy, modify, and/or distribute this software for any
"purpose with or without fee is hereby granted, provided that the above
"copyright notice and this permission notice appear in all copies.
"
"THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
"WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
"MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
"ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
"WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
"ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
"OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
let s:save_cpo = &cpo
set cpo&vim

let s:script_folder_path = escape(expand('<sfile>:p:h'),'\')
let s:python_folder_path = s:script_folder_path . '/../python/'

function! elixir_complete#Enable()
  if &diff
    return
  endif

  call s:SetupPython()
endfunction

function! s:SetupPython() abort
  py import sys
  py import vim
  exe 'python sys.path.insert(0, "' . s:python_folder_path .'")'
  py from ecclient.ecclient import ECClient
  "XXX: hack till the real stuff exists
  exe 'python user_options = {"project root": "' . getcwd() . '"}'
  py ecc_state = ECClient(user_options)
  return 1
endfunction
