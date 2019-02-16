import json
import requests
import pydash
import logging
from keys import URL


def get_url(url):
    print('get_url')

    response = requests.get(url)
    content = response.content.decode("utf8")

    print(content)
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def get_updates():
    url = URL + "get_updates"
    js = get_json_from_url(URL)
    return js

def get_last_chat_id_text(updates):
    print(updates)
    
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]

    print (text)
    print(chat_id)

    return (text, chat_id)

def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

text, chat = get_last_chat_id_and_text(get_updates())
send_message(text, chat)
