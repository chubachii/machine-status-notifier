import requests, json

# settings ファイル読み込み
with open("settings.json") as f: 
    config: dict = json.load(f)
    
TOKEN = config['token']
API = 'https://notify-api.line.me/api/notify'


def send(message, img_path=''):
    
    headers = {'Authorization': 'Bearer ' + TOKEN}
    data = {'message': message}
    
    # 画像を添付する場合
    if img_path == '':
        response = requests.post(API, headers=headers, data=data)     # POST
       
    # 画像を添付しない場合 
    else:
        files = {'imageFile': open(img_path, "rb")} 
        response = requests.post(API, headers=headers, data=data, files=files)     # POST
        
    try:
        response.raise_for_status()
        
    except requests.exceptions.HTTPError:
        print('HTTP Error: ' + str(response.status_code))


if __name__ == "__main__":
    send(message='message', img_path='../img/cat.jpg')
    send(message='message')