#!/usr/bin/python
# -*- coding: utf-8 -*-
import imaplib
import os
import re
import email
import codecs
import datetime
import calendar
import json

from email.parser import BytesParser
from email.policy import default


def main():
    with open(".credentials.json","r") as f:
        login, password = json.load(f)
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login, password)
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select()  # connect to inbox.
    # mail.select("laposte")  # using a label.
    # result, data = mail.search(None, '(SINCE "'+(datetime.date.today()-datetime.timedelta(365*3)
    #                                              ).strftime('%d-%b-%Y')+'")', '(FROM ticket-caisse@e-ticket.systeme-u.fr)')
    result, data = mail.search(None, '(FROM ticket-caisse@systeme-u.fr)')

    ids = data[0]
    len(ids)
    id_list = ids.split()
    for id in id_list:
        res, dat = mail.fetch(id, "(RFC822)")
        raw = dat[0][1]
        # email_message = email.message_from_bytes(raw)
        # subject = email_message['Subject']
        # print(str(id,"ISO-8859-1")+" "+subject)
        # for msg in email_message.get_payload():
        #         print(type(msg), msg.keys())
        #         for part in msg.walk():
        #                 print(part.get_content_type())

        new_msg = BytesParser(policy=default).parsebytes(raw)
        # print(type(new_msg))
        # print(new_msg.keys())
        for attachment in new_msg.iter_parts():
            if not 'Content-Disposition' in attachment.keys():
                continue
            # print(attachment.get_filename())
            if match := re.search("Ticket de caisse_[_0-9-]+.pdf", attachment.get_filename()):
                print(attachment['Content-Disposition'])
                filename = match.group()
                # print(attachment.items())
                payload = attachment.get_content()
                with open(f"input/u/{filename}", "wb") as f:
                    f.write(payload)

        # body = body.partition("--")[0].partition("Best Regards")[0].replace("\r\n","\n")
        # filename="data/"+subject
        # i = 1
        # while (os.path.isfile(filename)):
        #         filename=filename.rstrip("_"+str(i))+"_"+str(i+1)
        #         i=i+1
        # with codecs.open(filename,"w+","iso-8859-1") as file:
        #         file.write(body)


if __name__ == "__main__":
    main()
