import os, shutil, pathlib, tqdm

BASE_TRAIN_PATH = 'MSN_yolo2'

data = {'0_RED':'0 0.706250 0.530208 0.031250 0.031250',
        '0_YELLOW': '1 0.707031 0.554167 0.029687 0.029167',
        '0_NONE': '2 0.707031 0.538542 0.035937 0.064583',
        '1_RED': '0 0.475781 0.498958 0.048438 0.043750',
        '1_YELLOW': '1 0.477344 0.530208 0.048438 0.047917',
        '1_NONE': '2 0.475781 0.514583 0.054688 0.087500'}

DATASET_IMAGES_PATH = os.path.join(BASE_TRAIN_PATH, 'images')
DATASET_LABELS_PATH = os.path.join(BASE_TRAIN_PATH, 'labels')
os.makedirs(DATASET_IMAGES_PATH, exist_ok=True)
os.makedirs(DATASET_LABELS_PATH, exist_ok=True)

for label in data:
    dir_path = os.path.join(BASE_TRAIN_PATH, label)

    files = os.listdir(dir_path)
    
    for file in tqdm.tqdm(files):
        
        txt_name = os.path.splitext(file)[0] + '.txt'
        txt_path = os.path.join(DATASET_LABELS_PATH, txt_name)
        img_path = os.path.join(DATASET_IMAGES_PATH, file)
        original_path = os.path.join(dir_path, file)
        hour = os.path.splitext(file)[0].split('_')[3]
        
        if label[2:] == 'NONE':
            if int(hour) < 8 or 17 < int(hour):
                continue

        with open(txt_path, 'w') as f:
            f.write(data[label])
        shutil.copyfile(original_path, img_path)


        

            
