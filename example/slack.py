#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ref: https://github.com/os/slacker
from slacker import Slacker


# ref: https://api.slack.com/tokens
# ref: https://api.slack.com/docs/oauth-test-tokens
SLACK_TOKEN = ''
SLACK_CHANNEL_NAME = '#channel'


def distribute_csv_by_slack(csv_paths):
    slack = Slacker(SLACK_TOKEN)
    slack.chat.post_message(SLACK_CHANNEL_NAME, 'helloworld!')
    for csv_path in csv_paths:
        print(csv_path)
        slack.files.upload(csv_path, channels=SLACK_CHANNEL_NAME)
