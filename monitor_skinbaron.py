from src.utils.get_skindata import get_current_skinbaron_data
from src.utils.constants import *
import json


f = open("misc/credentials_adv.json")
data = json.load(f)
f.close()

ai_f = open('misc/accepted_items.txt', 'r')
accepted_items = ai_f.read().replace("'", "").split("\n")
ai_f.close()

t_api = data['telegram']['api_token']
t_id = data['telegram']['chat_id']
phone = ''

const = Constans(t_api, t_id, "", 0.73, 0.7)


get_current_skinbaron_data(data['skinbaron_api_credentials']['api_key'], accepted_items, const)