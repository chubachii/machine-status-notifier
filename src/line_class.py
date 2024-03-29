import requests

class Line():

    def __init__(self, token):
        self.__TOKEN = token
        self.__API = 'https://notify-api.line.me/api/notify'

    def send(self, message, image_path=''):
        headers = {'Authorization': 'Bearer ' + self.__TOKEN}
        data = {'message': message}
        
        # 画像を添付しない場合
        if image_path == '':
            response = requests.post(self.__API, headers=headers, data=data)     # POST
        
        # 画像を添付する場合 
        else:
            files = {'imageFile': open(image_path, "rb")} 
            response = requests.post(self.__API, headers=headers, data=data, files=files)     # POST
            
        try:
            response.raise_for_status()
            
        except requests.exceptions.HTTPError:
            print('HTTP Error: ' + str(response.status_code))
