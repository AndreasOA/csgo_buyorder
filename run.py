from src.get_skindata import *
import discord
import json
import pandas as pd
import argparse
import time
import threading
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument('acceptable_discount', type=float)
args = parser.parse_args()

f = open("misc/credentials1.json")
data = json.load(f)
f.close()
client = discord.Client()

TOKEN = data['discord_credentials']['token']
GUILD = int(data['discord_credentials']['guild'])
CHANNEL_ID = int(data['discord_credentials']['channel_id'])
SB_API_KEY = data['skinbaron_api_credentials']['api_key']
AWS_ACCESS_KEY = data['aws']['access_id']
AWS_KEY = data['aws']['key']
SLEEP_TIME_DEL = 15
GATEWAY = ApiGateway("https://api.skinport.com", access_key_id=AWS_ACCESS_KEY, access_key_secret=AWS_KEY)
GATEWAY.start()
SESSION = requests.Session()
SESSION.mount("https://api.skinport.com", GATEWAY)

def t1(channel, accepted_items, discount, session):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(get_current_skinport_data(channel, accepted_items, discount, session))
    loop.close()

def t2(api_key, channel, accepted_items, discount, session):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(get_current_skinbaron_data(api_key, channel, accepted_items, discount, session))
    loop.close()


async def main():
    f1= loop.create_task(get_current_skinport_data(channel, accepted_items, args.acceptable_discount, SESSION))
    f2 = loop.create_task(get_current_skinbaron_data(SB_API_KEY, channel, accepted_items, args.acceptable_discount, SESSION))
    await asyncio.wait([f1, f2])

@client.event
async def on_ready():
    # ====================================================================
    # Discord Setup
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    # ====================================================================
    # Read accepted items and prices
    ai_f = open('misc/accepted_items.txt', 'r')
    accepted_items = ai_f.read().replace("'", "").split("\n")
    ai_f.close()
    # ====================================================================
    # Read string for end of run
    split_f = open('misc/split_string.txt', 'r')
    split_f.close()
    # ====================================================================
    # Set params
    # ====================================================================
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    

        

client.run(TOKEN)
