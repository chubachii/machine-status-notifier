from camera_class import Camera
from line_class import Line
from model_class import Model

import json, os

camID = 1
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
image_tmp_path = os.path.join(os.path.dirname(__file__), 'status.jpg')

if __name__ == '__main__':
    
    # settings ファイル読み込み
    with open(config_path) as f: 
        config: dict = json.load(f)
    
    ### インスタンス生成
    camera = Camera(camID)
    line = Line(token=config['token'])
    model = Model(model_path=config['model_path'])
    
    ### カメラオープン
    if not camera.open(): line.send('エラー: カメラが見つかりません')
    
    ### メインループ
    while(True):
        
        if camera.wait_key(wait_time=200) == ord("q"): break  # qキーで抜ける

        frame = camera.read()               # カメラから1フレーム読み出し
        #camera.show_frame(frame)            # 読み込んだフレームを表示
        
        #　積層灯の状態予測と表示
        machine_status, score, update_flag = model.predict(image=frame)  
        camera.show_status(image=frame, status=machine_status, score=score) 
        
        # 積層灯の状態が更新された
        if update_flag: 
            
            # Noneへの変化の場合は無視する
            if not machine_status == 'none':
            
                # 積層灯の画像を保存
                camera.save(path=image_tmp_path, image=frame)
                line.send(message='変化を検知: ' + machine_status, image_path=image_tmp_path)
            