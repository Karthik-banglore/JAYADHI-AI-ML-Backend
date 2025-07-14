# data-curation/create_messy_datasets.py

import pandas as pd
import json
import os

def create_easy_dataset():
    """Create an easy-level messy dataset with obvious problems"""
    data = {
        'student_id': ['STU001', 'STU002', 'STU003', 'STU004', 'STU005', 
                       'STU006', 'STU007', 'STU008', 'STU009', 'STU010'],
        'name': ['Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Emma Brown',
                 'Frank Miller', 'Grace Lee', 'Henry Chen', 'Ivy Taylor', 'Jack Moore'],
        'age': [12, 13, 14, 25, 12, 13, 14, 13, 12, 11],  # 25 is an outlier
        'grade': ['7th', '8th', '9th', '8', '7th', '8th', '9th', '8th', '7th', '6th'],  # '8' missing 'th'
        'test_score': [85, 92, None, 88, 95, 150, 78, 82, 90, 87],  # None and 150 are issues
        'attendance': [0.95, 0.88, 0.92, 0.85, 1.5, 0.89, 0.94, 0.91, 0.87, 0.93]  # 1.5 is impossible
    }
    
    return pd.DataFrame(data)

def create_medium_dataset():
    """Create a medium-level dataset with subtler issues"""
    data = {
        'employee_id': ['EMP001', 'EMP002', 'EMP003', 'emp004', 'EMP005',  # Inconsistent case
                        'EMP006', 'EMP007', 'EMP008', 'EMP009', 'EMP010'],
        'department': ['Sales', 'Marketing', 'sales', 'IT', 'HR',  # Inconsistent capitalization
                       'Marketing', 'IT', 'hr', 'Sales', 'Finance'],
        'salary': [50000, 55000, 48000, 62000, 45000,
                   58000, 61000, 43000, 52000, 250000],  # 250000 is an outlier
        'start_date': ['2020-01-15', '2019-03-22', '2021/05/10', '2020-11-30', '2018-07-08',  # Inconsistent date format
                       '2019-12-01', '2021-02-14', '2020-06-25', '2019-09-18', '2018-11-12'],
        'email': ['alice@company.com', 'bob@company.com', 'carol@gmail.com', 'david@company.com', None,  # Personal email and missing
                  'frank@company.com', 'grace@company.com', 'henry@company.com', 'ivy@company.com', 'jack@company.com']
    }
    
    return pd.DataFrame(data)

def create_hard_dataset():
    """Create a hard-level dataset with complex issues"""
    data = {
        'product_id': ['PRD001', 'PRD002', 'PRD-003', 'PRD004', 'PRD005',  # Inconsistent format
                       'PRD006', 'PRD007', 'PRD008', 'PRD009', 'PRD010'],
        'product_name': ['Laptop Computer', 'wireless mouse', 'KEYBOARD MECHANICAL', 'Monitor 24"', 'USB Cable',
                         'Hard Drive', 'Graphics Card', 'Power Supply', 'RAM Memory', 'SSD Drive'],
        'price': [999.99, 25.50, 149.99, 299.99, 12.99,
                  199.99, 599.99, 89.99, 79.99, -50.00],  # Negative price
        'category': ['Electronics', 'electronics', 'Electronics', 'Monitors', 'Accessories',
                     'Storage', 'Components', 'Components', 'Memory', 'storage'],  # Case issues
        'stock_quantity': [50, 100, 75, 30, 200, 0, 25, 60, 150, None],  # Missing value
        'rating': [4.5, 4.2, 4.8, 4.0, 3.9, 4.3, 4.7, 4.1, 4.6, 6.0]  # Rating > 5.0 impossible
    }
    
    return pd.DataFrame(data)

# Create and save datasets (FIXED PATHS)
os.makedirs('messy-datasets', exist_ok=True)

easy_df = create_easy_dataset()
medium_df = create_medium_dataset()
hard_df = create_hard_dataset()

easy_df.to_json('messy-datasets/easy_student_data.json', orient='records', indent=2)
medium_df.to_json('messy-datasets/medium_employee_data.json', orient='records', indent=2)
hard_df.to_json('messy-datasets/hard_product_data.json', orient='records', indent=2)

print("✅ Easy dataset created: messy-datasets/easy_student_data.json")
print("✅ Medium dataset created: messy-datasets/medium_employee_data.json") 
print("✅ Hard dataset created: messy-datasets/hard_product_data.json")
print("✅ All messy datasets created successfully!")
