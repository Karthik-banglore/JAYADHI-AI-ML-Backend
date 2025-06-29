
import os
import csv

def generate_metadata():
    """
    Scans the training data directory and creates a metadata.csv file
    listing each image filename and its corresponding class label.
    """
    # Define the directory to scan and the output CSV file path
    train_dir = os.path.join(os.path.dirname(__file__), 'fruits-360-subset', 'train')
    metadata_file = os.path.join(os.path.dirname(__file__), 'metadata.csv')
    
    # Check if the training directory exists
    if not os.path.exists(train_dir):
        print(f"Error: Training directory not found at '{train_dir}'")
        return
        
    print(f"Scanning directory: {train_dir}")
    
    # Open the CSV file for writing
    with open(metadata_file, 'w', newline='') as csvfile:
        # Create a CSV writer object
        csv_writer = csv.writer(csvfile)
        
        # Write the header row
        csv_writer.writerow(['filename', 'label'])
        
        # Walk through the training directory
        for class_label in sorted(os.listdir(train_dir)):
            class_dir = os.path.join(train_dir, class_label)
            
            # Check if it's a directory
            if os.path.isdir(class_dir):
                for filename in sorted(os.listdir(class_dir)):
                    # Write the filename and label to the CSV
                    csv_writer.writerow([filename, class_label])

    print(f"Successfully created metadata.csv at: {metadata_file}")

if __name__ == '__main__':
    generate_metadata()
