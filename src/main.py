from camera_class import Camera
from line_class import Line
from model_class import Model

import json, os, datetime, jpholiday, cv2

image_tmp_path = os.path.join(os.path.dirname(__file__), 'status.jpg')

###################  準備  ###################
# 重みファイルがない場合はダウンロードする
weight_path = os.path.join(os.path.dirname(__file__), '../weights', 'best.pt')
if not os.path.isfile(weight_path):
    os.makedirs(os.path.dirname(weight_path), exist_ok=True)
    os.system(f'curl -Lo {weight_path} https://github.com/chubachii/machine-status-notifier/releases/download/v1.1/best.pt')
    
# config ファイル読み込み
with open(os.path.join(os.path.dirname(__file__), '../', 'config.json')) as f: 
    config: dict = json.load(f)

# インスタンス生成
line = Line(token=config['token'])

# カメラごとにモデルのインスタンスを生成する
cameras = {}
models = {}
for camID in range(10):
    cameras[camID] = Camera(camID)
    if cameras[camID].open():
        models[camID] = (Model(weight_path=weight_path))
    else:
        del cameras[camID]

if len(cameras) < 1:
    print('カメラが接続されていません')
    exit()

###################  メインループ  ###################
while(True):
    
    # カメラごとにループ
    for camID in cameras:

        if cameras[camID].wait_key(wait_time=20) == ord("q"): break  # qキーで抜ける

        frame = cameras[camID].read()  # カメラから1フレーム読み出し
        
        frame_draw, machine_status, update_flag = models[camID].predict(image=frame)

        cv2.imshow(f'{camID}', frame_draw)

        # 積層灯の状態が更新された
        if update_flag: 
            print(f'{camID}: color changed to {machine_status}')
            
            # Noneへの変化の場合は無視する
            if not machine_status == 'none':

                # 平日18:00～25:00 or 休日 の場合は通知する
                dt_now = datetime.datetime.now()
                HH = dt_now.strftime('%H')
                day = dt_now.strftime('%A')

                if (jpholiday.is_holiday(datetime.datetime.now()) 
                    or (18 <= int(HH) <= 23) 
                    or (0 == int(HH)) 
                    or (day == 'Saturday') 
                    or (day == 'Sunday')):
                
                    # 積層灯の画像を保存してLINEに送信
                    cameras[camID].save(path=image_tmp_path, image=frame)
                    line.send(message='変化を検知: ' + machine_status, image_path=image_tmp_path)