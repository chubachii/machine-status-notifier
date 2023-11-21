import os, shutil, pathlib, tqdm, random

BASE_TRAIN_PATH = 'MSN_combined'
DATASET_IMAGES_PATH = 'images'
DATASET_LABELS_PATH = 'labels'

###################################################################################
#### 学習用 (train) データに関する処理 ####
###################################################################################

# train 画像数取得
files = os.listdir(os.path.join(BASE_TRAIN_PATH, 'images'))
random.shuffle(files)
IMAGES_NUM = len(files)
TRAIN_NUM = int(IMAGES_NUM * 0.8)  # 学習データ:8割, 検証データ:2割 で分割

# アノテーション形式 変換 (PascalVOC→YOLO)
"""
print("\n*** アノテーション形式 変換中 (PascalVOC .xml  ->  YOLO .txt) ***")
# 変換後の .txt が存在する場合は追記を防ぐため一度消去する
TXT_PATH = os.path.join(BASE_PATH, 'train', 'labels_txt')
if os.path.isdir(TXT_PATH):
    shutil.rmtree(TXT_PATH) 
os.makedirs(TXT_PATH) 
convert_pascalvoc2yolo()
"""

# train ファイル移動
print("\n*** ファイルをコピー中 (original/Japan/train  ->  images, labels) ***")
os.makedirs(os.path.join(DATASET_IMAGES_PATH, 'train'), exist_ok=True)
os.makedirs(os.path.join(DATASET_LABELS_PATH, 'train'), exist_ok=True)
os.makedirs(os.path.join(DATASET_IMAGES_PATH, 'valid'), exist_ok=True)
os.makedirs(os.path.join(DATASET_LABELS_PATH, 'valid'), exist_ok=True)
count = 0
for file in tqdm.tqdm(files):
    
    # train へのコピー
    if count < TRAIN_NUM:
        file_path = os.path.join(BASE_TRAIN_PATH, 'images', file)
        shutil.copy(src=file_path, dst=os.path.join(DATASET_IMAGES_PATH, 'train'))
        
        # 対応するラベルが存在する場合には, ラベルもコピーする
        label_path = os.path.join(BASE_TRAIN_PATH, 'labels', pathlib.PurePath(pathlib.Path(file_path).name).stem + '.txt')
        if os.path.isfile(label_path):
            shutil.copy(src=label_path, dst=os.path.join(DATASET_LABELS_PATH, 'train'))

    # valid へのコピー
    else:
        file_path = os.path.join(BASE_TRAIN_PATH, 'images', file)
        shutil.copy(src=file_path, dst=os.path.join(DATASET_IMAGES_PATH, 'valid'))
        
        # 対応するラベルが存在する場合には, ラベルもコピーする
        label_path = os.path.join(BASE_TRAIN_PATH, 'labels', pathlib.PurePath(pathlib.Path(file_path).name).stem + '.txt')
        if os.path.isfile(label_path):
            shutil.copy(src=label_path, dst=os.path.join(DATASET_LABELS_PATH, 'valid'))
            
    count+=1
    
    
###################################################################################
#### テスト用 (test) データに関する処理 ####
###################################################################################
    
"""
# test 画像数取得
files = os.listdir(os.path.join(BASE_TEST_PATH, 'images'))

# test ファイル移動
print("\n*** ファイルをコピー中 (original/Japan/test  ->  images, labels) ***")
os.makedirs(os.path.join(DATASET_IMAGES_PATH, 'test'), exist_ok=True)
os.makedirs(os.path.join(DATASET_LABELS_PATH, 'test'), exist_ok=True)

for file in tqdm.tqdm(files):
    
    file_path = os.path.join(BASE_TEST_PATH, 'images', file)
    shutil.copy(src=file_path, dst=os.path.join(DATASET_IMAGES_PATH, 'test'))

"""