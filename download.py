#!/usr/bin/python
# -*- coding: utf-8 -*-
import imaplib
import re
import json

from email.parser import BytesParser
from email.policy import default


def main():
    with open(".credentials.json","r") as f:
        login, password = json.load(f)
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login, password)
    mail.select()  # connect to inbox.
    # mail.select("laposte")  # using a label.
    result, data = mail.search(None, '(FROM ticket-caisse@systeme-u.fr)') # ('OK', [b'657 721 ...'])

    ids = data[0]
    id_list = ids.split()
    for id in id_list:
        res, dat = mail.fetch(id, "(RFC822)")
        raw = dat[0][1]
        new_msg = BytesParser(policy=default).parsebytes(raw)
        for attachment in new_msg.iter_parts():
            if 'Content-Disposition' not in attachment.keys():
                continue
            if match := re.search("Ticket de caisse_[_0-9-]+.pdf", attachment.get_filename()):
                with open(f"input/u/{match.group()}", "wb") as f:
                    f.write(attachment.get_content())

if __name__ == "__main__":
    main()
