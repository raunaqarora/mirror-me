import time
import json
import markovify
import re
from slackclient import SlackClient

BOT_TOKEN = ""      #Fill in
GROUP_TOKEN = ""    #Fill in

global MESSAGE_QUERY            #Might need fixing
MESSAGE_QUERY = 'in:random'
MESSAGE_PAGE_SIZE = 100
DEBUG = True

def store_database(obj):
    with open('message_db.json', 'w') as json_file:
        json_file.write(json.dumps(obj))

    return True

def load_database():
    try:
        with open('message_db.json', 'r') as json_file:
            messages = json.loads(json_file.read())
    except IOError:
        with open('message_db.json', 'w') as json_file:
            json_file.write('{}')
        messages = {}

    return messages

def send_query(client, page=1):
    if DEBUG:
        print ("requesting page {}".format(page))

    return client.api_call('search.messages', query = MESSAGE_QUERY, count = MESSAGE_PAGE_SIZE, page = page)

def build_text_model():
    if DEBUG:
        print ("Building new model...")

    messages = load_database()
    return markovify.Text(" ".join(messages.values()), state_size=2)

def format_message(original):
    if original is None:
        return 'None'

    cleaned_message = re.sub(r'<(htt.*)>', '\1', original)
    return cleaned_message

def add_messages(message_db, new_messages):
    for match in new_messages['messages']['matches']:
        message_db[match['permalink']] = match['text']

    return message_db


def update_db(sc, channel):
    sc.rtm_send_message(channel, "Feeding on your messages...")
    group_sc = SlackClient(GROUP_TOKEN)
    messages_db = load_database()
    starting_count = len(messages_db.keys())
    new_messages = send_query(group_sc)
    total_pages = new_messages['messages']['paging']['pages']
    messages_db = add_messages(messages_db, new_messages)
    if total_pages > 1:
        for page in range(2, total_pages + 1):
            new_messages = send_query(group_sc, page=page)
            messages_db = add_messages(messages_db, new_messages)
    final_count = len(messages_db.keys())
    new_message_count = final_count - starting_count
    if final_count > starting_count:
        store_database(messages_db)
        sc.rtm_send_message(channel, "Thank you human, for giving me the power of {} new messages!".format(
            new_message_count
        ))
    else:
        sc.rtm_send_message(channel, "No new messages to eat :(")

    if DEBUG:
        print("Start: {}".format(starting_count), "Final: {}".format(final_count),
              "New: {}".format(new_message_count))
    del group_sc
    return new_message_count



def main():

    global MESSAGE_QUERY
    model = build_text_model()
    sc = SlackClient(BOT_TOKEN)

    if not sc.rtm_connect():
        raise Exception("Connection to slack failed")

    while True:
        for slack_event in sc.rtm_read():
            if not slack_event.get('type') == "message":
                continue

            message = slack_event.get("text")
            user = slack_event.get("user")
            channel = slack_event.get("channel")

            if not message or not user:
                continue

            if "mirror-me" in message.lower():
                MESSAGE_QUERY += ' from:'
                MESSAGE_QUERY += user
                markov_chain = model.make_sentence()
                sc.rtm_send_message(channel, format_message(markov_chain))

            if "feed mirror-me" in message.lower():
                MESSAGE_QUERY += ' from:'
                MESSAGE_QUERY += user
                if update_db(sc, channel) > 0:
                    model = build_text_model()

        time.sleep(0.5)


if __name__ == '__main__':
    main()
