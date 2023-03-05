# CSGO Marketplace Buyorder

## Currently only the Skinport Selenium implementation is working.

This python script helps finding and tracking the best offers for the items of your choice.

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
        "client_secret": "XXXX"
    },
    "skinbaron_api_credentials": {
        "api_key": "XXXXX"
    }
}
```

Replace all the XXXXX with your own data.

## Usage

```bash
python run.py 0.70
```

The value after run.py defines how much cheaper an item should be, so that it gets posted in the discord channel. 0.7 means 70% marketprice.

In **accepted_items.txt** one can add or remove skins, which should be monitored by the script. 

## Known issues

- Doppler and marble fade tracking does not work, since the sites treat them differently. Suggested Price at Skinport always suggests Sapphire or Ruby prices. Skinbaron treats phases seperatly. Lowest price does not differ between phase, therefore it is mostly only phase 1.
- (Script crashes if one marketplace is down.)
- Rework for Skinport with selenium, sometimes Bot protection causes issues. Make sure to use your google profile with the chrome instance of the webdriver