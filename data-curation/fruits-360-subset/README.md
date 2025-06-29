# Fruits 360 Subset

This dataset is a curated subset of the original [Fruits 360 dataset](https://www.kaggle.com/datasets/moltean/fruits). It has been created to provide a smaller, more manageable collection of images for specific applications.

## Contents

This subset contains images for 20 distinct classes, comprising:
- **15 Fruits:** Apple (Red Delicious, Golden 1), Banana, Orange, Strawberry, Peach, Pineapple, Grape (Black), Cherry (Rainier), Lemon, Pear, Plum, Kiwi, Cantaloupe, Pomegranate.
- **5 Vegetables:** Pepper (Green), Potato (White), Tomato, Cucumber (Ripe), Onion (White).

## Directory Structure

The dataset is organized into the following structure:

```
fruits-360-subset/
├── train/
│   ├── Apple_Golden_1/
│   │   ├── r0_0.jpg
│   │   └── ...
│   ├── Banana/
│   └── ...
├── test/
│   ├── Apple_Golden_1/
│   │   ├── r0_1.jpg
│   │   └── ...
│   ├── Banana/
│   └── ...
├── labels.txt
├── metadata.csv
└── README.md
```

- **`train/`**: Contains the training images, organized into subdirectories for each class.
- **`test/`**: Contains the testing images, also organized by class.
- **`labels.txt`**: A text file listing all class names in this subset, one per line.
- **`metadata.csv`**: A CSV file mapping each image filename in the `train` set to its corresponding class label.

## Usage

This subset is designed for a variety of tasks, including:

### Game Logic
The images can be used as assets in games that require fruit and vegetable identification. The clear, consistent backgrounds make them easy to process for tasks like:
- Matching games
- Quizzes and educational apps
- Object recognition challenges

### Model Training
The dataset is well-suited for training machine learning models, particularly for image classification. The `train` and `test` splits are already prepared, and the `metadata.csv` can be used to easily load the data with libraries like Pandas and TensorFlow/PyTorch.

## Contact

If you have any questions about this dataset, please contact **Me**.
