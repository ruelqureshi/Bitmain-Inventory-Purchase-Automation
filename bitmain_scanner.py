import requests
import json
import configparser, time, subprocess

config = configparser.ConfigParser()
config.read('settings.ini')

productid = str(config['Credentials']['productid'])

headers = {
    'Host': 'shop-product-service.bitmain.com',
    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Accept': 'application/json, text/plain, */*',
    'Sec-Ch-Ua-Mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Origin': 'https://shop.bitmain.com',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://shop.bitmain.com/product/detail?pid=00020230515112234510hwBt32se06B7',
    # 'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cookie': '_gid=GA1.2.1584388827.1688344801; country=en; language=en; _fbp=fb.1.1688344824935.1326487461; locale=en; JSESSIONID=b4c57021-db0d-4736-b555-f071e66aa91e; id=1783218; _ga_WLQLVERFEL=GS1.1.1688428816.3.1.1688428883.60.0.0; ticket=ST-de16c626a52405448d7517ef888f58a12b15c910ecebdb06884b129fcebafa72; _ga=GA1.2.299513903.1688344801; SERVERID=ce790d8e04a1135ede51e5b0f4a74ecf|1688429126|1688428883',
}

params = {'productId': productid}

print("[+] Scanning for product.")
while True:
    response = requests.get(
        'https://shop-product-service.bitmain.com/api/product/getDetail',
        params=params,
        #cookies=cookies,
        headers=headers,
        verify=False,
        )
    f = json.loads(response.text)['data']['productStatus']
    g = json.loads(response.text)['data']['buyPerMaxCount']
    time.sleep(1.8)
    if f == 4:
        pass
    elif f == 2:
        print('[+] Purchasing product')
        subprocess.run(["python", "purchaser.py", str(g)])
        break
