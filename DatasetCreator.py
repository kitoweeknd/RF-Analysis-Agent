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
DIALOG = '/root/autodl-tmp/RF-Analysis-Agent/dialog.json'
DATASET = '/root/autodl-tmp/RF-Analysis-Agent/dataset.json'
SOURCE = 'signal agent dataset'


def build_vqa_data(image_dir, user, assistant):
    return {
        "messages": [
            {"role": "user", "content": user},
            {"role": "assistant", "content": assistant},
            {"image": image_dir},
        ]
    }

def save_dataset(data, output_json_file):
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def main():
    # 先读取现有数据
    if os.path.exists(DATASET):
        with open(DATASET, 'r', encoding='utf-8') as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = []
    else:
        all_data = []
    
    if not isinstance(all_data, list):
        all_data = [all_data]
    
    with open(DIALOG, 'r', encoding='utf-8') as f:
        data = json.load(f)


    path = '/root/autodl-tmp/dataset/Dataset_allDrone+5SNRsDrone/allDrones/'
    for drone in DRONES:
        packs = os.path.join(path, drone)
        for pack in os.listdir(packs):
            imges = os.listdir(os.path.join(packs, pack))
            imgs = [os.path.join(packs, pack, i) for i in imges if i.endswith('.jpg')]
        random.shuffle(imgs)
        
        # 收集数据而不是立即写入
        for img in imgs[:NUM_DRONES]:
            all_data.append(build_vqa_data(img, data[drone]['analysis_Q'], data[drone]['analysis_A']))
            all_data.append(build_vqa_data(img, data[drone]['Type_Q'], data[drone]['Type_A']))
            all_data.append(build_vqa_data(img, data['SNR']['High_Q'], data['SNR']['High_A']))
            
            print(f"{img} Done")
    
    # 最后一次性写入所有数据
    save_dataset(all_data, DATASET)


    path = '/root/autodl-tmp/dataset/Dataset_allDrone+5SNRsDrone/5SNRs/'
    for drone in ['DJI MINI 3', 'DJI AVATA2', 'DJI FPV COMBO', 'DJI MAVIC3 PRO', 'DJI MINI4 PRO']:

        snrs = os.listdir(os.path.join(path, drone))

        for snr in snrs:
            if int(snr[:-2]) >= 10:
                snr_level = 'High_A'
            elif int(snr[:-2]) < 10 and int(snr[:-2]) > -10:
                snr_level = 'Middle_A'
            elif int(snr[:-2]) <= -10:
                snr_level = 'Low_A'
            imges = os.listdir(os.path.join(path, drone, snr))
            imgs = [os.path.join(path, drone, snr, 'parula', '1024', i) for i in imges if i.endswith('.jpg')]
            random.shuffle(imgs)
            for img in imgs[:NUM_SNRS]:
                
                all_data.append(build_vqa_data(img, data[drone]['analysis_Q'], data[drone]['analysis_A']))
                all_data.append(build_vqa_data(img, data[drone]['Type_Q'], data[drone]['Type_A']))
                all_data.append(build_vqa_data(img, data['SNR']['High_Q'], data['SNR'][snr_level]))
                
                print(f"{img} Done")
    save_dataset(all_data, DATASET)


if __name__ == '__main__':
    main()