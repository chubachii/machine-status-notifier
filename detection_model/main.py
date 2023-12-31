from camera_class import Camera
from line_class import Line
from model_class_yolo import Model_yolo

import json, os, datetime

camID = 0
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
image_tmp_path = os.path.join(os.path.dirname(__file__), 'status.jpg')

if __name__ == '__main__':
    
    # settings ファイル読み込み
    with open(config_path) as f: 
        config: dict = json.load(f)

    # 今日の日付を取得し3つのラベルそれぞれの保存用フォルダを作成
    today = datetime.datetime.now().strftime('%Y_%m_%d')
    save_dir = config['save_dir']
    os.makedirs(os.path.join(save_dir, 'none'), exist_ok = True)
    os.makedirs(os.path.join(save_dir, 'yellow'), exist_ok = True)
    os.makedirs(os.path.join(save_dir, 'red'), exist_ok = True)
    
    ### インスタンス生成
    camera = Camera(camID)
    line = Line(token=config['token'])
    model_yolo = Model_yolo(model_path=config['model_path'], class_path=config['class_path'])
    
    ### カメラオープン
    if not camera.open(): line.send('エラー: カメラが見つかりません')
    
    ### メインループ
    count = 20
    while(True):
        
        if camera.wait_key(wait_time=2000) == ord("q"): break  # qキーで抜ける

        frame = camera.read()               # カメラから1フレーム読み出し
        #camera.show_frame(frame)            # 読み込んだフレームを表示
        
        #　積層灯の状態予測と描画
        detections, machine_status, predicted_status, update_flag = model_yolo.predict(image=frame)  
        model_yolo.draw_predict(draw=frame.copy(), detections=detections)

        # 積層灯の状態が更新された
        if update_flag: 
            
            # Noneへの変化の場合は無視する
            if not machine_status == 'none':

                # 平日18:00～25:00 or 休日 の場合は通知する
                dt_now = datetime.datetime.now()
                HH = dt_now.strftime('%H')
                day = dt_now.strftime('%A')

                if (18 <= int(HH) <= 23) or (0 == int(HH)) or (day == 'Saturday') or (day == 'Sunday'):
                
                    # 積層灯の画像を保存
                    camera.save(path=image_tmp_path, image=frame)
                    #line.send(message='変化を検知: ' + machine_status, image_path=image_tmp_path)
        
        # 学習用データの収集
        if count > 19:
            #image_heatmap = model.draw_heatmap(frame.copy())
            dt_now = datetime.datetime.now()
            now = dt_now.strftime('%Y_%m_%d_%H_%M_%S')
        
            camera.save(path=os.path.join(save_dir, model_yolo.predicted_color, now + '.jpg'), image=frame)
           
            count = 0
        count += 1    

        # ステータスとヒートマップを並べて表示
        #camera.show_merged_image(image_status, image_heatmap)
    