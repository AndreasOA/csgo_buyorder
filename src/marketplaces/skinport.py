import base64
import requests


def authentication(clientId, clientSecret):
    clientData = f"{clientId}:{clientSecret}"
    encodedData = str(base64.b64encode(clientData.encode("utf-8")), "utf-8")
    authorizationHeaderString = f"Basic {encodedData}"

    return clientData, encodedData, authorizationHeaderString


def sp_get_marketplace_items():
    return requests.get("https://api.skinport.com/v1/items", params={
        "app_id": 730,
        "currency": "EUR",
        "tradable": 0
    }).json()


def save_data_to_txt(data):
    f = open('gen_files/skinport.txt', 'w')
    f.write(data)
    f.close()


if __name__ == '__main__':
    save_data_to_txt(str(sp_get_marketplace_items()).replace('},', '},\n'))