import os
import csv

def generate_metadata():
    """
    Scans the training data directory and creates a metadata.csv file
    listing each image filename and its corresponding class label.
    """
    # Define the directory to scan and the output CSV file path
    base_dir = os.path.dirname(__file__)
    train_dir = os.path.join(base_dir, 'fruits-360-subset', 'train')
    metadata_file = os.path.join(base_dir, 'metadata.csv')
    
    # Check if the training directory exists
    if not os.path.exists(train_dir):
        print(f"Error: Training directory not found at '{train_dir}'")
        return
        
    print(f"Scanning directory: {train_dir}")
    
    # Open the CSV file for writing
    with open(metadata_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write the header row
        csv_writer.writerow(['filename', 'label'])
        
        # Walk through the training directory
        for class_label in sorted(os.listdir(train_dir)):
            class_dir = os.path.join(train_dir, class_label)
            if os.path.isdir(class_dir):
                for filename in sorted(os.listdir(class_dir)):
                    csv_writer.writerow([filename, class_label])

    print(f"Successfully created metadata.csv at: {metadata_file}")

if __name__ == '__main__':
    generate_metadata()
