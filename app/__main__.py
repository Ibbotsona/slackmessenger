#!/usr/bin/python3.6
import json

from messagebot import Message, Server


def main():
    message = Message()
    server = Server()

    with open("event.json", "r") as data:
        event = json.loads(data)

    print(event)

    ref_success = server.dev_success_handler(event)
    server.send_slack_channel_msg(server.dev_failed_handler(event))


if __name__ == "__main__":
    main()
