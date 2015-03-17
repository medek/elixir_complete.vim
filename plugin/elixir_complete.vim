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

function! s:restore_cpo()
  let &cpo = s:save_cpo
  unlet s:save_cpo
endfunction

if exists( "g:loaded_elixir_complete" )
  call s:restore_cpo()
  finish
elseif !has('python')
  echohl WarningMsg |
        \ echomsg "elixir_complete unavailable: requires vim compiled with " .
        \ "Python 2.x support" | 
        \ echohl None
  call s:restore_cpo()
  finish
endif

let s:script_folder_path = escape(expand('<sfile>:p:h'),'\')
let s:python_folder_path = s:script_folder_path . '/../python/'
let s:elixir_complete_path = s:script_folder_path . '/../extern/elixir_complete/'

let g:loaded_elixir_complete = 1

augroup elixir_completeStart
  autocmd!
  autocmd VimEnter * call elixir_complete#Enable()
augroup END

call s:restore_cpo()
