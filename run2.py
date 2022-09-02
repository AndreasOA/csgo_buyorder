from src.get_skindata import *
import requests
import json
import argparse
import threading

parser = argparse.ArgumentParser()
parser.add_argument('acceptable_discount', type=float)
args = parser.parse_args()

ai_f = open('misc/accepted_items.txt', 'r')
accepted_items = ai_f.read().replace("'", "").split("\n")
ai_f.close()

f = open("misc/credentials1.json")
data = json.load(f)
f.close()

SB_API_KEY = data['skinbaron_api_credentials']['api_key']
AWS_ACCESS_KEY = data['aws']['access_id']
AWS_KEY = data['aws']['key']
TELEGRAM_API_TOKEN = data['telegram']['api_token']
TELEGRAM_CHAT_ID = data['telegram']['chat_id']
SLEEP_TIME_DEL = 15
GATEWAY = ApiGateway("https://api.skinport.com", access_key_id=AWS_ACCESS_KEY, access_key_secret=AWS_KEY)
GATEWAY.start()
SESSION = requests.Session()
SESSION.mount("https://api.skinport.com", GATEWAY)


t1 = threading.Thread(target=get_current_skinport_data, args=(accepted_items, args.acceptable_discount, SESSION,))
t2 = threading.Thread(target=get_current_skinbaron_data, args=(SB_API_KEY, accepted_items, args.acceptable_discount, SESSION,))
t1.start()
t2.start()