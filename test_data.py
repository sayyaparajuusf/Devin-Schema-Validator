"""
Test data examples for schema validation.
Contains both valid and invalid data records for testing.
"""

VALID_RECORDS = [
    {
        'id': 1,
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    },
    {
        'id': 2,
        'name': 'Jane Smith',
        'email': 'jane.smith@company.org'
    },
    {
        'id': 100,
        'name': 'Alice Johnson',
        'email': 'alice.johnson@university.edu'
    },
    {
        'id': 999,
        'name': 'Bob Wilson',
        'email': 'bob.wilson@domain.co.uk'
    }
]

INVALID_RECORDS = [
    {
        'name': 'Missing ID',
        'email': 'missing.id@example.com'
    },
    {
        'id': 1,
        'email': 'missing.name@example.com'
    },
    {
        'id': 2,
        'name': 'Missing Email'
    },
    
    {
        'id': 'not_an_integer',
        'name': 'Wrong ID Type',
        'email': 'wrong.id@example.com'
    },
    {
        'id': 3,
        'name': 123,  # Should be string
        'email': 'wrong.name@example.com'
    },
    {
        'id': 4,
        'name': 'Wrong Email Type',
        'email': 12345  # Should be string
    },
    
    {
        'id': 5,
        'name': 'Invalid Email 1',
        'email': 'not-an-email'
    },
    {
        'id': 6,
        'name': 'Invalid Email 2',
        'email': 'missing@domain'
    },
    {
        'id': 7,
        'name': 'Invalid Email 3',
        'email': '@missing-local.com'
    },
    {
        'id': 8,
        'name': 'Invalid Email 4',
        'email': 'spaces in@email.com'
    },
    
    {
        'id': None,
        'name': 'None ID',
        'email': 'none.id@example.com'
    },
    {
        'id': 9,
        'name': None,
        'email': 'none.name@example.com'
    },
    {
        'id': 10,
        'name': 'None Email',
        'email': None
    }
]

EDGE_CASE_RECORDS = [
    {
        'id': 11,
        'name': '',
        'email': 'empty.name@example.com'
    },
    {
        'id': 12,
        'name': 'Empty Email',
        'email': ''
    },
    
    {
        'id': 13,
        'name': 'A' * 1000,  # Very long name
        'email': 'long.name@example.com'
    },
    
    {
        'id': 14,
        'name': 'José María O\'Connor-Smith',
        'email': 'special.chars@example.com'
    },
    
    {
        'id': 15,
        'name': 'International User',
        'email': 'user@münchen.de'
    }
]

RECORDS_WITH_EXTRA_FIELDS = [
    {
        'id': 16,
        'name': 'Extra Fields User',
        'email': 'extra@example.com',
        'age': 30,
        'department': 'Engineering'
    }
]
