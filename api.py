#!/bin/env python3

import requests
import json

#based on https://gist.github.com/anonymous/9c790980b4955a35187a

NINTENDO_LOGIN_PAGE = "https://id.nintendo.net/oauth/authorize"

SPLATNET_CALLBACK_URL = "https://splatoon.nintendo.net/users/auth/nintendo/callback"
SPLATNET_CLIENT_ID = "12af3d0a3a1f441eb900411bb50a835a"

SPLATNET_SCHEDULE_URL = "https://splatoon.nintendo.net/schedule/index.json?utf8=✓"

username_eu = 'YOUR EU NNID HERE'
password_eu = 'YOUR EU NNID PWD HERE'
username_na = 'YOUR US NNID HERE'
password_na = 'YOUR US NNID PWD HERE'
username_jp = 'YOUR JP NNID HERE'
password_jp = 'YOUR JP NNID PWD HERE'

#based on https://github.com/Wiwiweb/SakuraiBot/blob/master/src/sakuraibot.py
def get_new_splatnet_cookie(u, pwd):
    parameters = {'client_id': SPLATNET_CLIENT_ID,
                  'response_type': 'code',
                  'redirect_uri': SPLATNET_CALLBACK_URL,
                  'username': u,
                  'password': pwd}

    response = requests.post(NINTENDO_LOGIN_PAGE, data=parameters)

    cookie = response.history[-1].cookies.get('_wag_session')
    if cookie is None:
        raise Exception("Couldn't retrieve cookie")
    return cookie


def get_splatnet_schedule(splatnet_cookie):
    cookies = {'_wag_session': splatnet_cookie}

    response = requests.get(SPLATNET_SCHEDULE_URL, cookies=cookies, data={'locale':"ja"})
    data = response.json()
    
    schedule = data["schedule"]
    festival = data["festival"]
    
    for rotation in schedule:
        
        #Clean names
        rotation["begin"] = rotation["datetime_begin"]
        del rotation["datetime_begin"]
        rotation["end"] = rotation["datetime_end"]
        del rotation["datetime_end"]
        
        if festival == False:
            rotation["ranked_mode"] = rotation["gachi_rule"]
            del rotation["gachi_rule"]
            rotation["stages"]["ranked"] = rotation["stages"]["gachi"]
            del rotation["stages"]["gachi"]
            
            regular = rotation["stages"]["regular"]
            ranked = rotation["stages"]["ranked"]
            
            for map in regular:
                del map["asset_path"]
            for map in ranked:
                del map["asset_path"]
        else:
            for map in rotation["stages"]:
                del map["asset_path"]

    return data

def write_schedule(u, pwd, region):
    splatnet_cookie = get_new_splatnet_cookie(u, pwd)
    dataI = get_splatnet_schedule(splatnet_cookie)
    with open('YOUR/PATH/TO/FILE/schedule_'+region+'.json', 'w', encoding='utf-8') as outfile:
        json.dump(dataI, outfile, ensure_ascii=False)
    

if __name__ == "__main__":
    
    write_schedule(username_eu, password_eu, "eu")
    write_schedule(username_na, password_na, "na")
    write_schedule(username_jp, password_jp, "jp")


