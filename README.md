# CSGO Marketplace Buyorder

This python script helps finding and tracking the best offers for the items of your choice.

## Installation

Checkout this repo and create a file in the misc folder called credentials.json

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