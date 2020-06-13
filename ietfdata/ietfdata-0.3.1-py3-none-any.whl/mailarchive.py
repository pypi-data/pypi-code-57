# Copyright (C) 2020 University of Glasgow
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import hashlib
import json
import re
import email

from typing        import List, Optional, Tuple, Dict, Iterator, Type, TypeVar, Any
from pathlib       import Path
from email.message import EmailMessage
from imapclient    import IMAPClient
from progress.bar  import Bar

# =================================================================================================

def parse_archived_at(archived_at : str) -> (str, str):
    start = archived_at.find("://mailarchive.ietf.org/arch/msg")
    uri   = archived_at[start+33:].strip()

    mailing_list = uri[:uri.find("/")]
    message_hash = uri[uri.find("/")+1:]
    return (mailing_list, message_hash)


class MailingList:
    pass


class MailArchive:

    # ---------------------------------------------------------------------------------------------
    # Private helper methods:



    def _cache_list(self, mailing_list: str):
        cache_folder = Path(self._cache_dir, "mailing-lists", "imap", mailing_list)
        cache_folder.mkdir(parents=True, exist_ok=True)

        imap = IMAPClient(host='imap.ietf.org', ssl=False, use_uid=True)
        imap.login("anonymous", "anonymous")
        imap.select_folder("Shared Folders/" + mailing_list, readonly=True)
        msg_list = imap.search()
        progress = Bar("{:20}".format(mailing_list), max = len(msg_list))
        for msg_id in msg_list:
            progress.next()
            cache_file = Path(cache_folder, "{:06d}".format(msg_id))
            if not cache_file.exists():
                msg = imap.fetch(msg_id, ["RFC822"])
                e = email.message_from_bytes(msg[msg_id][b"RFC822"])
                if e["Archived-At"] is not None:
                    mailing_list, message_hash = parse_archived_at(e["Archived-At"])
                    archive_file = Path(self._cache_dir, "mailing-lists", "arch", "msg", mailing_list, message_hash)
                    archive_file.parent.mkdir(parents=True, exist_ok=True)
                    archive_file.symlink_to(F"../../../imap/{mailing_list}/{msg_id:06}")
                with open(cache_file, "wb") as outf:
                    outf.write(msg[msg_id][b"RFC822"])


        progress.finish()
        imap.unselect_folder()
        imap.logout()



    # ---------------------------------------------------------------------------------------------
    # Public API follows:

    def __init__(self, cache_dir: Path):
        self._cache_dir = cache_dir


    def mailing_list_names(self) -> Iterator[str]:
        imap = IMAPClient(host='imap.ietf.org', ssl=False, use_uid=True)
        imap.login("anonymous", "anonymous")
        for f in imap.list_folders():
            yield f
        imap.logout()


    def mailing_list(self, mailing_list_name: str) -> MailingList:
        pass


    def message_from_archived_at(self, archived_at) -> EmailMessage:
        pass

    # Relation to ReviewAssignment.mailarch_url in ietfdata?


    # Formal messages that can be searched for:
    # - "I-D Action:"
    # - "Document Action:"
    # - "Protocol Action:"
    # - "WG Action:"
    # - "WG Review:"
    # - "Last Call:"
    # - "<wg name> Virtual Meeting"
    # - "RFCxxxx on"
    # - RFC errata announcements
    # - <directorate> last call review
    # - <directorate> telechat review 
    # - IESG ballot position announcements
    # (all sometime preceded by "Correction:" or "REVISED")
    # From: addresses have varied over time
    # many of these will need to be implemented in a helper class, that
    # has access to the datatracker, RFC index, and mailing list archives.



# =================================================================================================

if __name__ == '__main__':
    archive = MailArchive(cache_dir=Path("cache"))
    archive._cache_list("rfced-future")
    archive._cache_list("taps")
    archive._cache_list("rmcat")

# vim: set tw=0 ai:
