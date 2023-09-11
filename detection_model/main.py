from camera_class import Camera
from line_class import Line
from model_class import Model

import json, os, datetime

camID = 0
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
image_tmp_path = os.path.join(os.path.dirname(__file__), 'status.jpg')

if __name__ == '__main__':
    
    # settings ファイル読み込み
    with open(config_path) as f: 
        config: dict = json.load(f)

    # 今日の日付を取得し保存用フォルダを作成
    today = datetime.datetime.now().strftime('%Y_%m_%d')
    save_dir = config['save_dir'] + today
    os.makedirs(save_dir, exist_ok = True)
    
    ### インスタンス生成
    camera = Camera(camID)
    line = Line(token=config['token'])
    model = Model(model_path=config['model_path'])
    
    ### カメラオープン
    if not camera.open(): line.send('エラー: カメラが見つかりません')
    
    ### メインループ
    count = 0
    while(True):
        
        if camera.wait_key(wait_time=2000) == ord("q"): break  # qキーで抜ける

        frame = camera.read()               # カメラから1フレーム読み出し
        #camera.show_frame(frame)            # 読み込んだフレームを表示
        
        #　積層灯の状態予測と表示
        machine_status, score, update_flag = model.predict(image=frame)  
        camera.show_status(image=frame.copy(), status=machine_status, score=score) 
        
        # 積層灯の状態が更新された
        if update_flag: 
            
            # Noneへの変化の場合は無視する
            if not machine_status == 'none':
            
                # 積層灯の画像を保存
                camera.save(path=image_tmp_path, image=frame)
                line.send(message='変化を検知: ' + machine_status, image_path=image_tmp_path)
        
        # 学習用データの収集
        if count > 19:
            dt_now = datetime.datetime.now()
            now = dt_now.strftime('%Y_%m_%d_%H_%M_%S')
            camera.save(path=os.path.join(save_dir, now + '.jpg'), image=frame)
            count = 0
        count += 1    