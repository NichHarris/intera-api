import os
import json
from bot_studio import *

YOUTUBE_URL = 'https://www.youtube.com/watch?v='

DL_DIR = '../top_words_videos'
TOP_WORDS = 'top_words.json'
DESCRIPTION = 'Video Source: https://github.com/dxli94/WLASL and '
UPLOAD_JSON = 'uploaded_vids.json'
MISSING = 'missing_vids.txt'

if __name__ == '__main__':

    if os.path.exists(DL_DIR):
        video_list = os.listdir(DL_DIR)

        video_list = sorted(video_list)
        print(video_list)
        
        word_list = json.load(open(TOP_WORDS, 'r'))

        uploaded_vids = {}

        for video_num, video in enumerate(video_list):
            try:
                base_video_path = f'{DL_DIR}/{video}'

                video_name = os.path.split(video)[-1]
                word = video_name.split('_')[0]

                if word in word_list:
                    url = word_list[word]
                    print(f'Uploading {word}...')

                    youtube=bot_studio.youtube()
                    false=False;true=True
                    cookie_list=[
{
    "domain": ".youtube.com",
    "expirationDate": 1708724987.896741,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__Secure-1PAPISID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "CIqS1FSYXpUunrrc/AfhXrSBBh03-_ZCaV",
    "id": 1
},
{
    "domain": ".youtube.com",
    "expirationDate": 1708724987.89655,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__Secure-1PSID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "TAhe_Yq2tqtdxF909Ec_GnZEOXiAu2QF1xd2KMz-SamJQjAhEYt655v3FatcvBodkpnajg.",
    "id": 2
},
{
    "domain": ".youtube.com",
    "expirationDate": 1706851723.143715,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__Secure-1PSIDCC",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "AFvIBn_LT3Vwh7kskl0I7ZIwoihoMXtxvMuEdcETcd9SZjcLZfh0Fgj7oStPEaZOVEP_DWyk8Cc",
    "id": 3
},
{
    "domain": ".youtube.com",
    "expirationDate": 1708724987.896772,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__Secure-3PAPISID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "CIqS1FSYXpUunrrc/AfhXrSBBh03-_ZCaV",
    "id": 4
},
{
    "domain": ".youtube.com",
    "expirationDate": 1708724987.896592,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__Secure-3PSID",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "TAhe_Yq2tqtdxF909Ec_GnZEOXiAu2QF1xd2KMz-SamJQjAh8J6CTaKfJhR7Rdyty7dCrA.",
    "id": 5
},
{
    "domain": ".youtube.com",
    "expirationDate": 1706851723.143743,
    "hostOnly": false,
    "httpOnly": true,
    "name": "__Secure-3PSIDCC",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "AFvIBn8Gs3HgFykQYbiGMAHDqj7LfrjMzAcCzvNiXxk-wqBGFdXzalDsYJNsqMV-NNxLz00gMhQ",
    "id": 6
},
{
    "domain": ".youtube.com",
    "expirationDate": 1708724987.89668,
    "hostOnly": false,
    "httpOnly": false,
    "name": "APISID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "GTqGJN4QmqGMC5hF/AwFl7JlH55IuNoyEr",
    "id": 7
},
{
    "domain": ".youtube.com",
    "expirationDate": 1689022196.619595,
    "hostOnly": false,
    "httpOnly": true,
    "name": "DEVICE_INFO",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "ChxOekU0TnpRNU9UYzJORGM1TlRZM01ERXpOZz09EPTB/J0GGPTB/J0G",
    "id": 8
},
{
    "domain": ".youtube.com",
    "expirationDate": 1708724987.896626,
    "hostOnly": false,
    "httpOnly": true,
    "name": "HSID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "A7emNXl7rcnwY7dxm",
    "id": 9
},
{
    "domain": ".youtube.com",
    "expirationDate": 1709875701.741296,
    "hostOnly": false,
    "httpOnly": true,
    "name": "LOGIN_INFO",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "AFmmF2swRQIhAOANckqHsBoRlzSSub8vw_zYVstMdeMdYZ9F7SLHrzfUAiBoBX01MIh8YbSiHMN6tjkDCZzl_j-xHLA8G_wTVVPkIg:QUQ3MjNmeHpqVm56dHBLS0NNLXdaSVMzS1BKbTFnclRaS1FlRWdESEY3R3FUSW5kazB6ZlRmTVFpdG5YMjBwblZhekhEN25vOFl4TmxoTm1UbElFanBFRkUtVkh4bkhXLURjbkhUakRieUxoQ0xuNDRiV2p1OVNySW9tYXdyUHFEYW5ZUTQ1SWNyQkRJZW4yanc4VHlwRWFIaHBlV2hUa19R",
    "id": 10
},
{
    "domain": ".youtube.com",
    "expirationDate": 1709875702.227943,
    "hostOnly": false,
    "httpOnly": false,
    "name": "PREF",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "tz=America.Toronto&f6=40000000&f7=100&f5=20000&f4=4000000",
    "id": 11
},
{
    "domain": ".youtube.com",
    "expirationDate": 1708724987.89671,
    "hostOnly": false,
    "httpOnly": false,
    "name": "SAPISID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "CIqS1FSYXpUunrrc/AfhXrSBBh03-_ZCaV",
    "id": 12
},
{
    "domain": ".youtube.com",
    "expirationDate": 1708724987.896466,
    "hostOnly": false,
    "httpOnly": false,
    "name": "SID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "TAhe_Yq2tqtdxF909Ec_GnZEOXiAu2QF1xd2KMz-SamJQjAh9N1f3yVyYCbv3Jk_AYZiDQ.",
    "id": 13
},
{
    "domain": ".youtube.com",
    "expirationDate": 1706851723.143652,
    "hostOnly": false,
    "httpOnly": false,
    "name": "SIDCC",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "AFvIBn_NL317Fimy-mnRCFcuQildFCZ2XIzrZpoOOi06_8zUwpxDqsuuVsOSAlD9RH3VfO6vDTQ",
    "id": 14
},
{
    "domain": ".youtube.com",
    "expirationDate": 1708724987.896652,
    "hostOnly": false,
    "httpOnly": true,
    "name": "SSID",
    "path": "/",
    "sameSite": "unspecified",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "AZmwdR1mVqDkHbgZg",
    "id": 15
},
{
    "domain": ".youtube.com",
    "expirationDate": 1690820997.044819,
    "hostOnly": false,
    "httpOnly": true,
    "name": "VISITOR_INFO1_LIVE",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": false,
    "storeId": "0",
    "value": "miAusHoAtrg",
    "id": 16
},
{
    "domain": ".youtube.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "wide",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "1",
    "id": 17
},
{
    "domain": ".youtube.com",
    "hostOnly": false,
    "httpOnly": true,
    "name": "YSC",
    "path": "/",
    "sameSite": "no_restriction",
    "secure": true,
    "session": true,
    "storeId": "0",
    "value": "kVNtHy83OHU",
    "id": 18
}
]
                    youtube.login_cookie(cookies=cookie_list)
                    response=youtube.upload_to_playlist(title=word, video_path=base_video_path, description=f'{DESCRIPTION} {url}', type='unlisted', playlist='intera')
                    body=response['body']
                    video_link=body['VideoLink']

                    with open(UPLOAD_JSON, 'r') as f:
                        json_file = json.load(f)

                    json_file[word] = video_link

                    with open(UPLOAD_JSON, 'w') as top_words_file:
                        json.dump(json_file, top_words_file)

                    # os.system(f'python upload_vid.py --file="{base_video_path}" --title="{word}" --description="{DESCRIPTION} {url}" --category="22" --privacyStatus="unlisted"')

            except Exception as e:
                print(e)
                continue

        # check for missing words

        uploaded_vids = {}
        with open(UPLOAD_JSON, 'r') as f:
            try:
                uploaded_vids = json.load(f)
            except:
                pass

        for word in word_list:
            if word not in uploaded_vids:
                print(f'{word} not uploaded')
                
                with open(MISSING, 'a+') as f:
                    f.write(f'{word}\n')

# os.system(f'python upload_vid.py --file="{DL_DIR}/{video}" --title="{word}" --description="{DESCRIPTION} {url}" --category="22" --privacyStatus="unlisted"')
