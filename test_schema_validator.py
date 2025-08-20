import unittest
from schema_validator import SchemaValidator, validate_user_record
from test_data import (
    VALID_RECORDS, 
    INVALID_RECORDS, 
    RECORDS_WITH_EXTRA_FIELDS
)


class TestSchemaValidator(unittest.TestCase):
    """Unit tests for SchemaValidator class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.validator = SchemaValidator()
    
    def test_valid_records(self):
        """Test that all valid records pass validation."""
        for i, record in enumerate(VALID_RECORDS):
            with self.subTest(record_index=i, record=record):
                result = self.validator.validate_record(record)
                self.assertTrue(result['valid'], 
                              f"Valid record {i} failed validation: {result['errors']}")
                self.assertEqual(len(result['errors']), 0,
                               f"Valid record {i} should have no errors")
    
    def test_invalid_records(self):
        """Test that all invalid records fail validation."""
        for i, record in enumerate(INVALID_RECORDS):
            with self.subTest(record_index=i, record=record):
                result = self.validator.validate_record(record)
                self.assertFalse(result['valid'],
                               f"Invalid record {i} should fail validation")
                self.assertGreater(len(result['errors']), 0,
                                 f"Invalid record {i} should have errors")
    
    def test_missing_required_fields(self):
        """Test validation of missing required fields."""
        record = {'name': 'Test', 'email': 'test@example.com'}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertIn('Missing required field: id', result['errors'])
        
        record = {'id': 1, 'email': 'test@example.com'}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertIn('Missing required field: name', result['errors'])
        
        record = {'id': 1, 'name': 'Test'}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertIn('Missing required field: email', result['errors'])
    
    def test_wrong_data_types(self):
        """Test validation of incorrect data types."""
        record = {'id': 'string', 'name': 'Test', 'email': 'test@example.com'}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertTrue(any('must be of type int' in error for error in result['errors']))
        
        record = {'id': 1, 'name': 123, 'email': 'test@example.com'}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertTrue(any('must be of type str' in error for error in result['errors']))
        
        record = {'id': 1, 'name': 'Test', 'email': 123}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertTrue(any('must be of type str' in error for error in result['errors']))
    
    def test_email_format_validation(self):
        """Test email format validation."""
        invalid_emails = [
            'not-an-email',
            'missing@domain',
            '@missing-local.com',
            'spaces in@email.com',
            'double@@domain.com',
            'trailing.dot.@domain.com',
            '.leading.dot@domain.com'
        ]
        
        for email in invalid_emails:
            with self.subTest(email=email):
                record = {'id': 1, 'name': 'Test', 'email': email}
                result = self.validator.validate_record(record)
                self.assertFalse(result['valid'])
                self.assertTrue(any('valid email address' in error for error in result['errors']))
        
        valid_emails = [
            'test@example.com',
            'user.name@domain.org',
            'user+tag@example.co.uk',
            'user123@test-domain.com'
        ]
        
        for email in valid_emails:
            with self.subTest(email=email):
                record = {'id': 1, 'name': 'Test', 'email': email}
                result = self.validator.validate_record(record)
                self.assertTrue(result['valid'], 
                              f"Valid email {email} failed validation: {result['errors']}")
    
    def test_none_values(self):
        """Test validation of None values for required fields."""
        record = {'id': None, 'name': 'Test', 'email': 'test@example.com'}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertTrue(any('cannot be None' in error for error in result['errors']))
        
        record = {'id': 1, 'name': None, 'email': 'test@example.com'}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertTrue(any('cannot be None' in error for error in result['errors']))
        
        record = {'id': 1, 'name': 'Test', 'email': None}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertTrue(any('cannot be None' in error for error in result['errors']))
    
    def test_extra_fields_allowed(self):
        """Test that records with extra fields are allowed."""
        for record in RECORDS_WITH_EXTRA_FIELDS:
            with self.subTest(record=record):
                result = self.validator.validate_record(record)
                self.assertTrue(result['valid'],
                              f"Record with extra fields should be valid: {result['errors']}")
    
    def test_edge_cases(self):
        """Test edge cases like empty strings and special characters."""
        record = {'id': 1, 'name': '', 'email': 'test@example.com'}
        result = self.validator.validate_record(record)
        self.assertTrue(result['valid'])
        
        record = {'id': 1, 'name': 'Test', 'email': ''}
        result = self.validator.validate_record(record)
        self.assertFalse(result['valid'])
        self.assertTrue(any('valid email address' in error for error in result['errors']))
    
    def test_convenience_function(self):
        """Test the convenience function validate_user_record."""
        valid_record = {'id': 1, 'name': 'Test', 'email': 'test@example.com'}
        result = validate_user_record(valid_record)
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['errors']), 0)
        
        invalid_record = {'id': 'string', 'name': 'Test', 'email': 'test@example.com'}
        result = validate_user_record(invalid_record)
        self.assertFalse(result['valid'])
        self.assertGreater(len(result['errors']), 0)


class TestSchemaValidatorIntegration(unittest.TestCase):
    """Integration tests using test data."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.validator = SchemaValidator()
    
    def test_all_valid_records_pass(self):
        """Test that all records in VALID_RECORDS pass validation."""
        for record in VALID_RECORDS:
            result = self.validator.validate_record(record)
            self.assertTrue(result['valid'], 
                          f"Record {record} should be valid but got errors: {result['errors']}")
    
    def test_all_invalid_records_fail(self):
        """Test that all records in INVALID_RECORDS fail validation."""
        for record in INVALID_RECORDS:
            result = self.validator.validate_record(record)
            self.assertFalse(result['valid'],
                           f"Record {record} should be invalid but passed validation")


if __name__ == '__main__':
    unittest.main()
