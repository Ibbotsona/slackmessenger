#!/usr/local/bin/python3.6

import requests

from settings import *


class Message:
    def __init__(self):
        self.build_success = "Build Successful"
        self.build_failed = "Build Failed"
        self.build_stopped = "Build Stopped"
        self.build_started = "Build Started"
        self.invalid_status_code = "Invalid Status Code"


class Server:

    def __init__(self):
        self.message = Message()
        self.dev_suffix = " on Development Environment"
        self.ref_suffix = " on Reference Environment"
        self.prod_suffix = " on Production Environment"

    def is_dev(self, event):
        if "Dev" in event['detail']['project-name']:
            return True

    def is_ref(self, event):
        if "Ref" in event['detail']['project-name']:
            return True

    def is_prod(self, event):
        if "Prod" in event['detail']['project-name']:
            return True

    def build_started(self, event):
        if "IN_PROGRESS" in event['detail']['build-status']:
            return True

    def build_failed(self, event):
        if "FAILED" in event['detail']['build-status']:
            return True

    def build_succeeded(self, event):
        if "SUCCEEDED" in event['detail']['build-status']:
            return True

    def build_stopped(self, event):
        if "STOPPED" in event['detail']['build-status']:
            return True

    def dev_started_handler(self, event):
        dev_build_started = self.message.build_started + self.dev_suffix
        if self.is_dev(event) and self.build_started(event):
            return dev_build_started

    def dev_failed_handler(self, event):
        dev_build_failed = self.message.build_failed + self.dev_suffix
        if self.is_dev(event) and self.build_failed(event):
            return dev_build_failed

    def dev_success_handler(self, event):
        dev_build_success = self.message.build_success + self.dev_suffix
        if self.is_dev(event) and self.build_succeeded(event):
            return dev_build_success

    def dev_stopped_handler(self, event):
        dev_build_stopped = self.message.build_stopped + self.dev_suffix
        if self.is_dev(event) and self.build_stopped(event):
            return dev_build_stopped

    def ref_started_handler(self, event):
        ref_build_started = self.message.build_started + self.ref_suffix
        if self.is_ref(event) and self.build_started(event):
            return ref_build_started

    def ref_failed_handler(self, event):
        ref_build_failed = self.message.build_failed + self.ref_suffix
        if self.is_ref(event) and self.build_failed(event):
            return ref_build_failed

    def ref_success_handler(self, event):
        ref_build_success = self.message.build_success + self.ref_suffix
        if self.is_ref(event) and self.build_succeeded(event):
            return ref_build_success

    def ref_stopped_handler(self, event):
        ref_build_stopped = self.message.build_stopped + self.ref_suffix
        if self.is_ref(event) and self.build_stopped(event):
            return ref_build_stopped

    def prod_started_handler(self, event):
        prod_build_started = self.message.build_started + self.prod_suffix
        if self.is_prod(event) and self.build_started(event):
            return prod_build_started

    def prod_failed_handler(self, event):
        prod_build_failed = self.message.build_failed + self.prod_suffix
        if self.is_prod(event) and self.build_failed(event):
            return prod_build_failed

    def prod_success_handler(self, event):
        prod_build_success = self.message.build_success + self.prod_suffix
        if self.is_prod(event) and self.build_succeeded(event):
            return prod_build_success

    def prod_stopped_handler(self, event):
        prod_build_stopped = self.message.build_stopped + self.prod_suffix
        if self.is_prod(event) and self.build_stopped(event):
            return prod_build_stopped

    def send_slack_channel_msg(self, msg):
        slack_webhook = SLACK_WEBHOOK
        message = '{{"text": "{}"}}'.format(msg)

        response = requests.post(
            slack_webhook, data=message,
            headers={'Content-type': 'application/json'}
        )

        if response != 200:
            return "Somethings gone wrong, please check your settings and try again."
        return response
