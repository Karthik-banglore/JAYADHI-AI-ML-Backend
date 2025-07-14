# data-curation/data_issues_config.py

DATA_ISSUES = {
    'easy_student_data': {
        'issues': [
            {
                'type': 'outlier',
                'column': 'age',
                'problematic_value': 25,
                'explanation': 'Age 25 is too old for elementary school students',
                'suggested_action': 'Remove or flag as data entry error'
            },
            {
                'type': 'formatting',
                'column': 'grade',
                'problematic_value': '8',
                'correct_value': '8th',
                'explanation': 'Grade format should be consistent (e.g., 8th, not 8)',
                'suggested_action': 'Standardize to include ordinal suffix'
            },
            {
                'type': 'missing_value',
                'column': 'test_score',
                'explanation': 'Missing test scores need to be handled',
                'suggested_action': 'Fill with average, median, or mark as incomplete'
            },
            {
                'type': 'impossible_value',
                'column': 'test_score',
                'problematic_value': 150,
                'explanation': 'Test scores should be between 0-100',
                'suggested_action': 'Remove or verify the data entry'
            },
            {
                'type': 'impossible_value',
                'column': 'attendance',
                'problematic_value': 1.5,
                'explanation': 'Attendance rate cannot exceed 100% (1.0)',
                'suggested_action': 'Check if this should be 0.15 or remove'
            }
        ],
        'total_issues': 5
    },
    'medium_employee_data': {
        'issues': [
            {
                'type': 'case_inconsistency',
                'column': 'employee_id',
                'problematic_value': 'emp004',
                'correct_value': 'EMP004',
                'explanation': 'Employee IDs should follow consistent capitalization',
                'suggested_action': 'Convert all to uppercase'
            },
            {
                'type': 'case_inconsistency',
                'column': 'department',
                'problematic_values': ['sales', 'hr'],
                'explanation': 'Department names should be consistently capitalized',
                'suggested_action': 'Use title case for all department names'
            },
            {
                'type': 'outlier',
                'column': 'salary',
                'problematic_value': 250000,
                'explanation': 'Salary significantly higher than others, may be data error',
                'suggested_action': 'Verify if this is correct or a decimal place error'
            },
            {
                'type': 'format_inconsistency',
                'column': 'start_date',
                'problematic_value': '2021/05/10',
                'explanation': 'Date format should be consistent (YYYY-MM-DD)',
                'suggested_action': 'Standardize all dates to YYYY-MM-DD format'
            },
            {
                'type': 'invalid_data',
                'column': 'email',
                'problematic_value': 'carol@gmail.com',
                'explanation': 'Personal email should be company email',
                'suggested_action': 'Contact employee for correct company email'
            },
            {
                'type': 'missing_value',
                'column': 'email',
                'explanation': 'Missing email address',
                'suggested_action': 'Contact employee for email address'
            }
        ],
        'total_issues': 6
    },
    'hard_product_data': {
    'issues': [
        {
            'type': 'format_inconsistency',
            'column': 'product_id',
            'problematic_value': 'PRD-003',
            'explanation': 'Product ID format inconsistent',
            'suggested_action': 'Standardize to PRDXXX'
        },
        {
            'type': 'case_inconsistency',
            'column': 'product_name',
            'problematic_values': ['wireless mouse', 'KEYBOARD MECHANICAL'],
            'explanation': 'Product names should follow title case',
            'suggested_action': 'Convert to title case'
        },
        {
            'type': 'impossible_value',
            'column': 'price',
            'problematic_value': -50.00,
            'explanation': 'Price cannot be negative',
            'suggested_action': 'Verify or remove entry'
        },
        {
            'type': 'case_inconsistency',
            'column': 'category',
            'problematic_values': ['electronics', 'storage'],
            'explanation': 'Category names should be capitalized',
            'suggested_action': 'Use title case'
        },
        {
            'type': 'missing_value',
            'column': 'stock_quantity',
            'explanation': 'Missing stock quantity',
            'suggested_action': 'Add correct quantity'
        },
        {
            'type': 'impossible_value',
            'column': 'rating',
            'problematic_value': 6.0,
            'explanation': 'Rating cannot exceed 5.0',
            'suggested_action': 'Verify or remove entry'
        }
    ],
    'total_issues': 6
}
}