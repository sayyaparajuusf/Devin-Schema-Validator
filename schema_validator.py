import re
from typing import Dict, Any


class SchemaValidator:
    """A simple schema validator for data validation."""
    
    def __init__(self):
        self.user_schema = {
            'id': {
                'type': int,
                'required': True
            },
            'name': {
                'type': str,
                'required': True
            },
            'email': {
                'type': str,
                'required': True,
                'format': 'email'
            }
        }
        
        self.email_pattern = re.compile(
            r'^[a-zA-Z0-9][a-zA-Z0-9._%+-]*[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$|^[a-zA-Z0-9]@[a-zA-Z0-9][a-zA-Z0-9.-]*[a-zA-Z0-9]\.[a-zA-Z]{2,}$'
        )
    
    def validate_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a data record against the user schema.
        
        Args:
            record: Dictionary containing the data to validate
            
        Returns:
            Dictionary with validation results:
            {
                'valid': bool,
                'errors': List[str]
            }
        """
        errors = []
        
        for field_name, field_config in self.user_schema.items():
            if field_config.get('required', False):
                if field_name not in record:
                    errors.append(f"Missing required field: {field_name}")
                elif record[field_name] is None:
                    errors.append(f"Required field '{field_name}' cannot be None")
        
        for field_name, value in record.items():
            if field_name in self.user_schema:
                field_config = self.user_schema[field_name]
                expected_type = field_config['type']
                
                if value is None and not field_config.get('required', False):
                    continue
                
                if not isinstance(value, expected_type):
                    errors.append(
                        f"Field '{field_name}' must be of type {expected_type.__name__}, "
                        f"got {type(value).__name__}"
                    )
                
                if (field_name == 'email' and 
                    field_config.get('format') == 'email' and 
                    isinstance(value, str)):
                    if not self.email_pattern.match(value):
                        errors.append(f"Field '{field_name}' must be a valid email address")
            else:
                pass
        
        return {
            'valid': len(errors) == 0,
            'errors': errors
        }


def validate_user_record(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function to validate a user record.
    
    Args:
        record: Dictionary containing user data to validate
        
    Returns:
        Dictionary with validation results
    """
    validator = SchemaValidator()
    return validator.validate_record(record)


if __name__ == "__main__":
    validator = SchemaValidator()
    
    valid_record = {
        'id': 1,
        'name': 'John Doe',
        'email': 'john.doe@example.com'
    }
    
    invalid_record = {
        'id': 'not_an_int',
        'name': 'Jane Doe',
        'email': 'invalid-email'
    }
    
    print("Valid record validation:")
    result = validator.validate_record(valid_record)
    print(f"Valid: {result['valid']}")
    print(f"Errors: {result['errors']}")
    
    print("\nInvalid record validation:")
    result = validator.validate_record(invalid_record)
    print(f"Valid: {result['valid']}")
    print(f"Errors: {result['errors']}")
