from django.http import JsonResponse
from django.shortcuts import render
import requests
from datetime import datetime
from django.contrib.auth.decorators import login_required

from accounts.models import Account


# Create your views here.
def home_page(request):
    url = 'https://www.binance.com/bapi/futures/v3/public/future/leaderboard/getLeaderboardRank'
    headers= {
        "content-type": "application/json",
        "x-trace-id": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0",
        "x-ui-request-trace": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0"
    }    
    payload = {"tradeType":"PERPETUAL","statisticsType":"ROI","periodType":"WEEKLY","isShared":"true","isTrader":"false"}
    req=requests.post(url,headers=headers,json=payload).json()
    data = req['data']
    uidList = []
    for item in data:
        uidList.append(item['encryptedUid'])
    url = "https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getPositionStatus"
    payload = {"tradeType":"PERPETUAL","encryptedUidList":uidList[:20]}
    result = requests.post(url,headers=headers,json=payload).json()
    posStatus = result['data'] 
    i = 0
    # print(posStatus)
    data = data[:20]
    for item in data:
        item["hasPosition"] = posStatus[i]['hasPosition']
        i += 1
    context = {
        "data": data,
    }
    return render(request, "index.html", context)


@login_required(login_url='/account/login')
def monitor(request):
    if request.POST or request.GET.get('encryptedUid'):
        tradeType = request.POST.get('tradeType', 'PERPETUAL')
        uid = request.POST.get('uid', request.GET.get('encryptedUid'))
        url='https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getOtherPosition'
        headers= {
            "content-type": "application/json",
            "x-trace-id": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0",
            "x-ui-request-trace": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0"
        }

        payload = {"encryptedUid":uid,"tradeType":tradeType}

        req=requests.post(url,headers=headers,json=payload).json()
        positions = req['data']['otherPositionRetList']
        url = 'https://www.binance.com/bapi/futures/v2/public/future/leaderboard/getOtherLeaderboardBaseInfo'
        headers= {
            "content-type": "application/json",
            "x-trace-id": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0",
            "x-ui-request-trace": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0"
        }

        payload = {"encryptedUid":uid}

        req=requests.post(url,headers=headers,json=payload).json()
        userInfo = req['data']

        for pos in positions:
            time = pos['updateTimeStamp']
            pos['updateTimeStamp'] = datetime.fromtimestamp(time / 1000)
            pos['roe'] = round(pos['roe'] * 100, 4)
            pos['pnl'] = round(pos['pnl'], 2)
            pos['size'] = abs(pos['amount'])
            pos['entryPrice'] = round(pos['entryPrice'], 4)
            pos['markPrice'] = round(pos['markPrice'], 4)
            

        context = {
            'positions': positions,
            'userInfo': userInfo,
        }
        return render(request, "monitor.html", context)    


@login_required(login_url='/account/login')
def sendTel(request):
    # importing all required libraries
    url = 'https://api.telegram.org/bot5980251499:AAG2pFjNpT7v-62Uk7w9Jnt92QGppxXX8p0/getUpdates'
    resp = requests.get(url).json()
    result = resp['result']
    users = []
    for i in result:
        if i.get('message'):
            chat_id = i['message']['from']['id']
            first_name = i['message']['from']['first_name']
            if chat_id not in users:
                users.append(chat_id)

                TOKEN = '5980251499:AAG2pFjNpT7v-62Uk7w9Jnt92QGppxXX8p0'
                # chat_id = '379595374'
                message = "Test. Hello "+first_name+", Welcome to CryptoMonitor!"
                url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
                resp = requests.get(url).json()
    # print(requests.get(url).json()) # this sends the message
    return JsonResponse({"status": "success"})


def viewUser(request):
    url = 'https://api.telegram.org/bot5980251499:AAG2pFjNpT7v-62Uk7w9Jnt92QGppxXX8p0/getUpdates'
    resp = requests.get(url).json()
    result = resp['result']
    users = []
    for i in result:
        if i.get('message'):
            chat_id = i['message']['from']['id']
            if chat_id not in users:
                users.append(chat_id)
    return JsonResponse(resp)


def GetPosList(request):
    url = 'https://www.binance.com/bapi/futures/v1/public/future/leaderboard/getFeaturedUserRank'
    headers= {
        "content-type": "application/json",
        "x-trace-id": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0",
        "x-ui-request-trace": "4c3d6fce-a2d8-421e-9d5b-e0c12bd2c7c0"
    }    
    payload = {"tradeType":"PERPETUAL"}
    req=requests.post(url,headers=headers,json=payload).json()
    
    return JsonResponse(req)


def subscribe(request):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "auth_error"})   

    TOKEN = '5980251499:AAG2pFjNpT7v-62Uk7w9Jnt92QGppxXX8p0'
                # chat_id = '379595374'
    trader = request.GET.get('user', '')
    message = "Hello, You'll be getting alerts of "+trader
    if request.user.chatid == '':
        url = 'https://api.telegram.org/bot5980251499:AAG2pFjNpT7v-62Uk7w9Jnt92QGppxXX8p0/getUpdates'
        resp = requests.get(url).json()
        result = resp['result']
        for i in result:
            if i.get('message'):
                if i['message']['from']['username'] == request.user.username:
                    chat_id = i['message']['from']['id']
                    Account.objects.filter(id=request.user.id).update(chatid=chat_id)
                else:
                    chat_id = ''  
    else:
        chat_id = request.user.chatid

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    resp = requests.get(url).json()
    if not resp['ok']:
        return JsonResponse({"status": "failed", "username": request.user.username})
    return JsonResponse({"status": "success"})