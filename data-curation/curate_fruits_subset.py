import os, shutil, random

original_path = '/Users/karthikbt/Desktop/JAYADHI-AI-ML-Backend/fruits-360_original-size/fruits-360-original-size/Training'
subset_path = '/Users/karthikbt/Desktop/JAYADHI-AI-ML-Backend/data-curation/fruits-360-subset'
selected_classes = ['Apple', 'Banana', 'Orange', 'Grape', 'Pear', 'Tomato', 'Kiwi', 'Plum', 'Pineapple', 'Cucumber']

# Remove old subset if exists
if os.path.exists(subset_path):
    shutil.rmtree(subset_path)

for split in ['train', 'test']:
    os.makedirs(os.path.join(subset_path, split), exist_ok=True)

for cls in selected_classes:
    src = os.path.join(original_path, cls)
    images = sorted(os.listdir(src))
    random.shuffle(images)
    train_imgs = images[:70]
    test_imgs = images[70:100]
    os.makedirs(os.path.join(subset_path, 'train', cls), exist_ok=True)
    os.makedirs(os.path.join(subset_path, 'test', cls), exist_ok=True)
    for img in train_imgs:
        shutil.copy(os.path.join(src, img), os.path.join(subset_path, 'train', cls, img))
    for img in test_imgs:
        shutil.copy(os.path.join(src, img), os.path.join(subset_path, 'test', cls, img))

with open(os.path.join(subset_path, 'labels.txt'), 'w') as f:
    for cls in selected_classes:
        f.write(cls + '\n')

with open(os.path.join(subset_path, 'metadata.csv'), 'w') as f:
    f.write('filename,label,split\n')
    for split in ['train', 'test']:
        for cls in selected_classes:
            folder = os.path.join(subset_path, split, cls)
            for img in os.listdir(folder):
                f.write(f'{img},{cls},{split}\n')

print("Curation complete.")
