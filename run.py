from src.get_skindata import *
import discord
import json
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('acceptable_discount', type=float)
args = parser.parse_args()

f = open("misc/credentials.json")
data = json.load(f)
f.close()
client = discord.Client()

TOKEN = data['discord_credentials']['token']
GUILD = int(data['discord_credentials']['guild'])
CHANNEL_ID = int(data['discord_credentials']['channel_id'])
SB_API_KEY = data['skinbaron_api_credentials']['api_key']
SLEEP_TIME_DEL = 15


@client.event
async def on_ready():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    sent_messages = []
    ai_f = open('misc/accepted_items.txt', 'r')
    accepted_items = ai_f.read().replace("'", "").split("\n")
    ai_f.close()
    split_f = open('misc/split_string.txt', 'r')
    eor_string = split_f.read()
    split_f.close()
    df_sb = pd.DataFrame()
    steam_conn = True
    steam_cnt = 0
    run_cnt = 0
    while True:
        print('Finding offers....')
        if not steam_conn:
            steam_cnt += 1
        if steam_cnt % 20 == 0:
            steam_conn = True
        if run_cnt % 20 == 0:
            await channel.send('SCRIPT STILL RUNNING')
        sent_messages, df_sb, steam_conn = await get_current_skin_data(SB_API_KEY, channel, sent_messages, 
                                                            df_sb, accepted_items, eor_string, args.acceptable_discount, steam_conn)
        run_cnt += 1
        print('offers found: ', len(sent_messages))
        
        

client.run(TOKEN)
