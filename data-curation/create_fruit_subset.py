

import os
import shutil

def create_fruit_subset():
    # The original dataset is expected to be in the parent directory of this script
    original_dataset_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fruits-360_original-size', 'fruits-360-original-size'))
    
    # Define the classes to be included in the subset
    classes_to_include = [
        'Apple_Red_Delicious', 'Apple_Golden_1', 'Banana', 'Orange', 'Strawberry', 
        'Peach', 'Pineapple', 'Grape_Black', 'Cherry_Rainier', 'Lemon', 'Pear', 
        'Plum', 'Kiwi', 'Cantaloupe_1', 'Pomegranate', 'Pepper_Green', 
        'Potato_White', 'Tomato_1', 'Cucumber_Ripe', 'Onion_White'
    ]
    
    # Define source and destination directories
    source_train_dir = os.path.join(original_dataset_dir, 'Training')
    source_test_dir = os.path.join(original_dataset_dir, 'Test')
    
    subset_base_dir = os.path.join(os.path.dirname(__file__), 'fruits-360-subset')
    dest_train_dir = os.path.join(subset_base_dir, 'train')
    dest_test_dir = os.path.join(subset_base_dir, 'test')
    
    # Create destination directories if they don't exist
    os.makedirs(dest_train_dir, exist_ok=True)
    os.makedirs(dest_test_dir, exist_ok=True)
    
    # Function to copy files for a given class
    def copy_class_files(source_dir, dest_dir, class_name):
        source_class_dir = os.path.join(source_dir, class_name)
        dest_class_dir = os.path.join(dest_dir, class_name)
        
        if os.path.exists(source_class_dir):
            os.makedirs(dest_class_dir, exist_ok=True)
            for filename in os.listdir(source_class_dir):
                shutil.copy(os.path.join(source_class_dir, filename), dest_class_dir)
    
    # Copy the specified classes for both training and test sets
    for class_name in classes_to_include:
        print(f'Copying {class_name}...')
        copy_class_files(source_train_dir, dest_train_dir, class_name)
        copy_class_files(source_test_dir, dest_test_dir, class_name)
        
    # Create labels.txt
    labels_file = os.path.join(subset_base_dir, 'labels.txt')
    with open(labels_file, 'w') as f:
        for class_name in sorted(classes_to_include):
            f.write(f"{class_name}\n")
            
    print("\nSubset creation complete.")
    print(f"Copied {len(classes_to_include)} classes to: {subset_base_dir}")
    print(f"Created labels.txt at: {labels_file}")

if __name__ == '__main__':
    create_fruit_subset()

