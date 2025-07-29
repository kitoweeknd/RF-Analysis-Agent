import csv
import json
import os

def build_vqa_json(image_dir, qa_csv_file, output_json_file):
    data = []

    with open(qa_csv_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            image_name = row['image_name']
            question = row['question']
            answer = row['answer']
            source = row.get('source', 'MyVQA')

            # 构建样本
            sample = {
                "image": os.path.join(image_dir, image_name),
                "texts": [
                    {
                        "user": question,
                        "assistant": answer,
                        "source": source
                    }
                ]
            }
            data.append(sample)

    # 写入 JSON 文件
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ 写入完成，共写入 {len(data)} 条样本 → {output_json_file}")
