import time
import markovify
from slackclient import SlackClient

BOT_TOKEN = os.environ.get('BOT_TOKEN', None)
#GROUP_TOKEN = os.environ.get('GROUP_TOKEN', None)
#BOT_TOKEN = ""
#GROUP_TOKEN = ""

def main():
    #Slack instance
    sc = SlackClient(BOT_TOKEN)
    if not sc.rtm_connect():
        raise Exception("Couldn't connect to slack.")

    while True:
        for slack_event in sc.rtm_read():
            if not slack_event.get('type') == "message":
                continue

            message = slack_event.get("text")
            user = slack_event.get("user")
            channel = slack_event.get("channel")

            if not message or not user:
                continue

            # Listen to commands


        # Sleep for half a second
        time.sleep(0.5)


if __name__ == '__main__':
    main()
