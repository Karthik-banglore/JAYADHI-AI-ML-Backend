import os, shutil, random

original_path = '/Users/karthikbt/Desktop/JAYADHI-AI-ML-Backend/fruits-360_original-size/fruits-360-original-size/Training'
subset_path   = '/Users/karthikbt/Desktop/JAYADHI-AI-ML-Backend/data-curation/fruits-360-subset'

selected_classes = [
  'Apple 10','Banana 3','Blackberrie 1','Beans 1','Cabbage red 1','carrot_1',
  'Cherry 3','Cucumber 10','pear_1','Tomato 5'
]

# Remove old subset if exists
if os.path.exists(subset_path):
    shutil.rmtree(subset_path)

# Create train/test folders
for split in ['train','test']:
    os.makedirs(os.path.join(subset_path, split), exist_ok=True)

# Copy images
for cls in selected_classes:
    src = os.path.join(original_path, cls)
    imgs = sorted(os.listdir(src))
    random.shuffle(imgs)
    train_imgs = imgs[:70]
    test_imgs  = imgs[70:100]
    for split, images in (('train', train_imgs), ('test', test_imgs)):
        dst_dir = os.path.join(subset_path, split, cls)
        os.makedirs(dst_dir, exist_ok=True)
        for img in images:
            shutil.copy(os.path.join(src, img), os.path.join(dst_dir, img))

# Write labels.txt
with open(os.path.join(subset_path, 'labels.txt'), 'w') as f:
    f.write('\n'.join(selected_classes))

# Write metadata.csv
with open(os.path.join(subset_path, 'metadata.csv'), 'w') as f:
    f.write('filename,label,split\n')
    for split in ['train','test']:
        for cls in selected_classes:
            folder = os.path.join(subset_path, split, cls)
            for img in os.listdir(folder):
                f.write(f'{img},{cls},{split}\n')

print("Curation complete.")
