#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import httplib2
import apiclient
import mimetypes
import smtplib
import requests

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
import traceback

# ref: https://www.google.com/settings/security/lesssecureapps
MAIL_FROM = ''
GMAIL_PASSWORD = ''
MAIL_TO = ''


def create_message(mail_from, mail_to, subject, content, paths):
    message = MIMEMultipart()
    message["from"] = mail_from
    message["to"] = mail_to
    message["subject"] = subject
    message["Date"] = formatdate(localtime=True)
    message.attach(MIMEText(content))

    for path in paths:
        content_type, encoding = mimetypes.guess_type(path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)
            if main_type == 'text':
                fp = open(path)
                msg = MIMEText(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(path, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(path, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(path, 'rb')
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(path))
        message.attach(msg)

    return message


def distribute_csv_by_json(csv_paths):
    # csv =via mail=> server developer
    scopes = ['https://www.googleapis.com/auth/gmail.compose', 'https://www.googleapis.com/auth/gmail.send']
    credentials = get_credentials(JSON_KEYFILE_FPATH, scopes)
    credentials = credentials.create_delegated(MAIL_FROM)
    http = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build("gmail", "v1", http=http)
    message = create_message(
        mail_from=MAIL_FROM,
        mail_to=MAIL_TO,
        subject='[automatic] apply this files',
        content='hello world!',
        paths=csv_paths
    )

    try:
        result = service.users().messages().send(
            userId=MAIL_FROM,
            body={'raw': str(base64.urlsafe_b64encode(message.as_string().encode("utf-8")), "utf-8")}
        ).execute()
        print("Message Id: {}".format(result["id"]))

    except apiclient.errors.HttpError:
        traceback.print_exc()



if __name__ == "__main__":
    message = create_message(
        mail_from=MAIL_FROM,
        mail_to=MAIL_TO,
        subject='subject',
        content='contents',
        paths=[]
    )

    gmail_user = MAIL_FROM
    gmail_pwd = GMAIL_PASSWORD
    gmail_server = smtplib.SMTP("smtp.gmail.com", 587)
    gmail_server.ehlo()
    gmail_server.starttls()
    gmail_server.ehlo()
    gmail_server.login(gmail_user,gmail_pwd)
    gmail_server.sendmail(gmail_user, MAIL_TO, message.as_string())
    gmail_server.close()
