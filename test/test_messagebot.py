from unittest import TestCase
from unittest.mock import MagicMock, patch
import requests
import re


from slackmessenger.app.messagebot import Message, Server


class MessageTest(TestCase):

    def setUp(self):
        self.message = Message()

    def test_build_started_message(self):
        self.assertEqual(self.message.build_started, "Build Started")

    def test_build_success_message(self):
        self.assertEqual(self.message.build_success, "Build Successful")

    def test_build_failed_message(self):
        self.assertEqual(self.message.build_failed, "Build Failed")

    def test_build_stopped_message(self):
        self.assertEqual(self.message.build_stopped, "Build Stopped")


class ServerTest(TestCase):

    def setUp(self):
        self.jsonfile = {
            "source": [
                "aws.codebuild"
            ],
            "detail-type": [
                "CodeBuild Build State sChange"
            ],
            "detail": {
                "build-status": [
                    "IN_PROGRESS",
                    "SUCCEEDED",
                    "FAILED",
                    "STOPPED"
                ],
                "project-name": [
                    "Dev",
                    "Ref",
                    "Prod"
                ]
            }
        }
        self.server = Server()
        self.mock = MagicMock()

    def test_is_dev(self):
        self.assertTrue(self.server.is_dev(self.jsonfile))

    def test_is_ref(self):
        self.assertTrue(self.server.is_ref(self.jsonfile))

    def test_is_prod(self):
        self.assertTrue(self.server.is_prod(self.jsonfile))

    def test_build_started(self):
        self.assertTrue(self.server.build_started(self.jsonfile))

    def test_build_failed(self):
        self.assertTrue(self.server.build_failed(self.jsonfile))

    def test_build_succeeded(self):
        self.assertTrue(self.server.build_succeeded(self.jsonfile))

    def test_build_stopped(self):
        self.assertTrue(self.server.build_stopped(self.jsonfile))

    def test_dev_started_handler(self):
        self.assertEqual(self.server.dev_started_handler(
            self.jsonfile), "Build Started on Development Environment")

    def test_dev_failed_handler(self):
        self.assertEqual(self.server.dev_failed_handler(
            self.jsonfile), "Build Failed on Development Environment")

    def test_dev_success_handler(self):
        self.assertEqual(self.server.dev_success_handler(
            self.jsonfile), "Build Successful on Development Environment")

    def test_dev_stopped_handler(self):
        self.assertEqual(self.server.dev_stopped_handler(
            self.jsonfile), "Build Stopped on Development Environment")

    def test_ref_started_handler(self):
        self.assertEqual(self.server.ref_started_handler(
            self.jsonfile), "Build Started on Reference Environment")

    def test_ref_failed_handler(self):
        self.assertEqual(self.server.ref_failed_handler(
            self.jsonfile), "Build Failed on Reference Environment")

    def test_ref_success_handler(self):
        self.assertEqual(self.server.ref_success_handler(
            self.jsonfile), "Build Successful on Reference Environment")

    def test_ref_stopped_handler(self):
        self.assertEqual(self.server.ref_stopped_handler(
            self.jsonfile), "Build Stopped on Reference Environment")

    def test_prod_started_handler(self):
        self.assertEqual(self.server.prod_started_handler(
            self.jsonfile), "Build Started on Production Environment")

    def test_prod_failed_handler(self):
        self.assertEqual(self.server.prod_failed_handler(
            self.jsonfile), "Build Failed on Production Environment")

    def test_prod_success_handler(self):
        self.assertEqual(self.server.prod_success_handler(
            self.jsonfile), "Build Successful on Production Environment")

    def test_prod_stopped_handler(self):
        self.assertEqual(self.server.prod_stopped_handler(
            self.jsonfile), "Build Stopped on Production Environment")

    def test_send_slack_msg_success(self):
        with patch.object(requests, 'post', return_value=200) as mock_method:
            self.assertEqual(self.server.send_slack_channel_msg(
                self.server.prod_started_handler(self.jsonfile)), 200)

    def test_send_slack_msg_failed(self):
        self.mock.side_effect = Exception(
            'Somethings gone wrong, please check your settings and try again.')
        with patch.object(requests, 'post', return_value=400) as mock_method:
            self.assertEqual(self.server.send_slack_channel_msg(
                self.server.prod_started_handler(self.jsonfile)), 'Somethings gone wrong, please check your settings and try again.')
