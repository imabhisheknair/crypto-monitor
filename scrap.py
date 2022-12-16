import requests

url='https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition'
headers= {
    "content-type": "application/json",
    "x-trace-id": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0",
    "x-ui-request-trace": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0"
}

payload = {"encryptedUid":"2154D02AD930F6C6E65C507DD73CB3E7","tradeType":"PERPETUAL"}

req=requests.post(url,headers=headers,json=payload).json()
positions = req['data']['otherPositionRetList']
for pos in positions:
    print(pos)
# for item in req['data']:
#     roi = item['value']
#     print(roi)