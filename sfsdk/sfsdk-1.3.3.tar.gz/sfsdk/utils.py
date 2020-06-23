# This file is part of the SecureFlag Platform.
# Copyright (c) 2020 SecureFlag Limited.

# This program is free software: you can redistribute it and/or modify  
# it under the terms of the GNU General Public License as published by  
# the Free Software Foundation, version 3.

# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
# General Public License for more details.

# You should have received a copy of the GNU General Public License 
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import shutil
import stat
import re
from sfsdk import log
import os
import base64
import mimetypes

re_extract_b64_data = re.compile(r'data:([a-zA-Z0-9/]+);base64,([A-Za-z0-9+/=]+)')
re_extract_src_media = re.compile(r'src\=(?:\"|\')(.+?)(?:\"|\')')
re_extract_markdown_media = re.compile(r'!\[.*?\]\((.*?)\)')

def load_and_replace_media_with_b64(base_folder, content):

    for media_path in re_extract_src_media.findall(content) + re_extract_markdown_media.findall(content):

        if not os.path.isfile(media_path):

            absolute_media_path = os.path.join(base_folder, media_path)

            if not absolute_media_path:
                continue
            
            confirmed_media_path = absolute_media_path

        else:
            confirmed_media_path = media_path

        mime_type = mimetypes.guess_type(confirmed_media_path)[0]
        
        with open(confirmed_media_path, 'rb') as stream:
            media_content = stream.read()
            b64_data = base64.b64encode(media_content).decode()

        b64_string = f'data:{mime_type};base64,{b64_data}'

        content = content.replace(media_path, b64_string)

    return content
            

def save_and_replace_b64_with_media(base_folder, content, content_name):

    for idx, b64_mime_data in enumerate(re_extract_b64_data.findall(content)):

        mime_type, b64_data = b64_mime_data

        extension = mimetypes.guess_extension(mime_type)

        file_name = f'{content_name}_{idx}{extension}'

        media_relative_path = os.path.join(
            'media',
            file_name
        )
        os.makedirs(
            os.path.join(base_folder, 'media'), 
            exist_ok = True
        )

        media_absolute_path = os.path.join(
            base_folder, media_relative_path
        )

        with open(media_absolute_path, 'wb+') as stream:
            stream.write(base64.b64decode(b64_data))

        content = content.replace(
            f'data:{mime_type};base64,{b64_data}', 
            media_relative_path
        )

        log.debug(f'Saved {extension} media file {media_relative_path}')
    
    return content

def merge_tree(src, dst, preserve_symlinks = True, ignore = None):
    if not os.path.exists(dst):
        os.makedirs(dst)
        shutil.copystat(src, dst)
    lst = os.listdir(src)
    if ignore:
        excl = ignore(src, lst)
        lst = [x for x in lst if x not in excl]
    for item in lst:
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if preserve_symlinks and os.path.islink(s):
             if os.path.lexists(d):
                 os.remove(d)
             os.symlink(os.readlink(s), d)
             try:
                 st = os.lstat(s)
                 mode = stat.S_IMODE(st.st_mode)
                 os.lchmod(d, mode)
             except:
                 pass # lchmod not available
        elif os.path.isdir(s):
            merge_tree(s, d, preserve_symlinks, ignore)
        else:
            shutil.copy2(s, d)


def recursive_del(obj, bad_key):
    if isinstance(obj, dict):
        # the call to `list` is useless for py2 but makes
        # the code py2/py3 compatible
        for key in list(obj.keys()):
            if key == bad_key:
                del obj[key]
            else:
                recursive_del(obj[key], bad_key)
    elif isinstance(obj, list):
        for i in reversed(range(len(obj))):
            recursive_del(obj[i], bad_key)
    else:
        pass

def prettypath(p):
    return p.replace(os.path.expanduser('~'), '~', 1)