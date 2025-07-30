import json
import os
import random


DRONES = [
    'DJI MAVIC3 PRO',
    'DAUTEL EVO NANO',
    'DEVENTION DEVO',
    'DJI FPV COMBO',
    'DJI AVATA2',
    'DJI MINI 3',
    'DJI MINI4 PRO',
    'FLY SKY EL 18',
    'FLY SKY FS I6X',
    'FRSKY-X9DP2019',
    'FRSKY X14',
    'FRSKY X20R',
    'FUTABA T10J',
    'HERELINK HX4',
    'JR PROPO XG7',
    'JR PROPO XG14',
    'JUMPER T14',
    'JUMPER TPro V2',
    'Radiolink AT9S Pro',
    'Radiolink AT10 II',
    'RadioMaster BOXER',
    'RadioMaster TX16S',
    'SIYI FT24',
    'SIYI MK15',
    'SIYI MK32',
    'SKYDROID-H12',
    'SKYDROID-T10',
    'WFLY ET10',
    'WFLY ET16S',
    'WFLY WFT09SII',
    'YUNZHUO-H12',
    'YUNZHUO-H16',
    'YUNZHUO-H30'
]
NUM_DRONES = 60
NUM_SNRS = 20
DIALOG = 'C:/ML/signal_agent/dialog.json'
DATASET = 'C:/ML/signal_agent/dataset.json'
SOURCE = 'signal agent dataset'


def build_vqa_json(image_dir, output_json_file, user, assistant):
    if os.path.exists(output_json_file):
        with open(output_json_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    if not isinstance(data, list):
        data = [data]
    
    # 构建新样本
    sample = {
        "image": image_dir,
        "texts": [
            {
                "user": user,
                "assistant": assistant,
                "source": SOURCE
            }
        ]
    }
    
    # 添加新样本到数据中
    data.append(sample)

    # 写入 JSON 文件
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    
    with open(DIALOG, 'r', encoding='utf-8') as f:
        data = json.load(f)
    """
    path = 'E:/Drone_dataset/RFUAV/augmentation_exp2_allDrone/or_image/matlab/'
    for drone in DRONES:

        packs = os.path.join(path, drone)

        for pack in os.listdir(packs):
            imges = os.listdir(os.path.join(packs, pack))
            imgs = [os.path.join(packs, pack, i) for i in imges if i.endswith('.jpg')]
        random.shuffle(imgs)
        for img in imgs[:NUM_DRONES]:
            build_vqa_json(img, DATASET, data[drone]['analysis_Q'], data[drone]['analysis_A'])
            build_vqa_json(img, DATASET, data[drone]['Type_Q'], data[drone]['Type_A'])
            build_vqa_json(img, DATASET, data['SNR']['High_Q'], data['SNR']['High_A'])
    """


    path = 'E:/Drone_dataset/RFUAV/augmentation_exp1_MethodSelect/benchmark_or/'
    for drone in ['DJI MINI 3', 'DJI AVATA2', 'DJI FPV COMBO', 'DJI MAVIC3 PRO', 'DJI MINI4 PRO']:

        snrs = os.listdir(os.path.join(path, drone))

        for snr in snrs:
            if int(snr[:-2]) >= 10:
                snr_level = 'High_A'
            elif int(snr[:-2]) < 10 and int(snr[:-2]) > -10:
                snr_level = 'Middle_A'
            elif int(snr[:-2]) <= -10:
                snr_level = 'Low_A'
            imges = os.listdir(os.path.join(path, drone, snr, 'parula', '1024'))
            imgs = [os.path.join(path, drone, snr, 'parula', '1024', i) for i in imges if i.endswith('.jpg')]
            random.shuffle(imgs)
            for img in imgs[:NUM_SNRS]:
                build_vqa_json(img, DATASET, data[drone]['analysis_Q'], data[drone]['analysis_A'])
                build_vqa_json(img, DATASET, data[drone]['Type_Q'], data[drone]['Type_A'])
                build_vqa_json(img, DATASET, data['SNR']['High_Q'], data['SNR'][snr_level])


if __name__ == '__main__':
    main()