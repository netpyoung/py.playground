#!/usr/bin/env python
# -*- coding: utf-8 -*-

import httplib2


# ref: https://console.developers.google.com/
MASTER_SHEET_ID = ''

### FUNC
def get_credentials(json_keyfile_fpath, scopes):
    return ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_fpath, scopes=scopes)


def download_client_master(google_sheet_id, output_fpath):
    scopes = ['https://www.googleapis.com/auth/drive']
    credentials = get_credentials(JSON_KEYFILE_FPATH, scopes)
    http = credentials.authorize(httplib2.Http())
    drive = discovery.build('drive', 'v3', http=http)
    with open(output_fpath, 'wb') as f:
        resp = drive.files().export(fileId=google_sheet_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet').execute()
        f.write(resp)
    return output_fpath
