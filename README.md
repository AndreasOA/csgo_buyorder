# Outdated, because of bot protection :(

## CSGO Marketplace Buyorder

This python script helps finding and tracking the best offers for the items of your choice.

### Currently Working:
- Selenium Skinport
- API Skinbaron

### In Progress:
- API Skinport (Endpoint Update Slow, not useful for finding cheap items)
- API Skinbaron (Full Marketplace. Trick to detect items earlier)
- Rework for Skinport with selenium, sometimes Bot protection causes issues. Make sure to use your google profile with the chrome instance of the webdriver

### Note:
- Discord currently unused. Credentials can be omitted.
- Same goes for cc.

### Known issues:
- Doppler and marble fade tracking does not work, since the sites treat them differently. Suggested Price at Skinport always suggests Sapphire or Ruby prices. Skinbaron treats phases seperatly. Lowest price does not differ between phase, therefore it is mostly only phase 1.
- Script crashes if one marketplace is down.

## Installation

Required packages:
- pandas
- bs4
- discord
- (selenium)

Checkout this repo and create a file in the misc folder called **credentials.json**.

```json
{
    "discord_credentials": {
        "token": "XXXXX",
        "guild": "XXXXX",
        "channel_id": "XXXXX"
    },
    "skinport_api_credentials": {
        "client_id": "XXXXX",
        "client_secret": "XXXXX",
        "username": "XXXXX",
        "password": "XXXXX"
    },
    "skinbaron_api_credentials": {
        "api_key": "XXXXX"
    },
    "telegram": {
        "api_token": "XXXXX",
        "chat_id": "XXXXX",
        "phone": "XXXXX"
    },
    "cc": {
        "secret": "XXXXX"
    }
}
```

Replace all the `XXXXX` with your own data.

## Usage

```bash
python monitor_skinport.py
```
or
```bash
python monitor_skinbaron.py
```

Set the discounts you want to track in the python file you want to execute.

In **accepted_items.txt** one can add or remove skins, which should be monitored by the script. 
