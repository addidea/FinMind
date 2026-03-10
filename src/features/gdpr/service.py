# GDPR Compliance Service
import json
import csv
import io
from typing import Dict, List, Optional
from datetime import datetime


class GDPRService:
    def __init__(self):
        # In a real implementation, this would connect to your database
        # For now, we'll simulate with in-memory storage
        self.user_data_store = {}
        self.audit_log_store = []
    
    def get_user_data(self, user_id: str) -> Optional[Dict]:
        """Retrieve all personal data for a user"""
        # Simulate database lookup
        # In a real implementation, this would query your actual database
        # and collect all personal data associated with the user
        
        # This is a mock implementation - in reality you'd fetch from your DB
        # and collect data from all tables/models that store user information
        mock_user_data = {
            'user_id': user_id,
            'personal_info': {
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '+1234567890',
                'address': '123 Main St, City, State'
            },
            'financial_data': [
                {'id': 'trans_1', 'amount': 100.00, 'date': '2023-01-01', 'description': 'Grocery'},
                {'id': 'trans_2', 'amount': 50.00, 'date': '2023-01-02', 'description': 'Gas'}
            ],
            'preferences': {
                'notifications_enabled': True,
                'currency': 'USD',
                'budget_alerts': True
            },
            'account_info': {
                'created_at': '2023-01-01T00:00:00Z',
                'last_login': '2023-12-01T10:00:00Z',
                'status': 'active'
            }
        }
        
        # Return mock data if user exists, otherwise None
        if user_id.startswith('test_') or user_id.isdigit():
            return mock_user_data
        return None
    
    def convert_to_csv(self, user_data: Dict) -> str:
        """Convert user data to CSV format"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Category', 'Field', 'Value'])
        
        # Flatten the user data into rows
        def flatten_dict(d, parent_key=''):
            items = []
            for k, v in d.items():
                new_key = f'{parent_key}.{k}' if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key).items())
                elif isinstance(v, list):
                    for i, item in enumerate(v):
                        if isinstance(item, dict):
                            items.extend(flatten_dict(item, f'{new_key}[{i}]').items())
                        else:
                            items.append((f'{new_key}[{i}]', str(item)))
                else:
                    items.append((new_key, str(v)))
            return dict(items)
        
        flattened = flatten_dict(user_data)
        for key, value in flattened.items():
            writer.writerow(['Personal Data', key, value])
        
        return output.getvalue()
    
    def delete_user_data(self, user_id: str) -> bool:
        """Delete all personal data for a user"""
        # In a real implementation, this would:
        # 1. Delete user records from all relevant tables
        # 2. Remove any related data (transactions, preferences, etc.)
        # 3. Ensure foreign key constraints are handled properly
        # 4. Log the deletion action
        
        # Mock implementation - mark user as deleted
        # In real implementation, actually remove from database
        user_exists = self.get_user_data(user_id) is not None
        
        if user_exists:
            # Here you would perform actual deletion from database
            # For example:
            # db.session.execute(delete(User).where(User.id == user_id))
            # db.session.execute(delete(Transaction).where(Transaction.user_id == user_id))
            # db.session.commit()
            
            # For this mock, just return success
            return True
        
        return False
    
    def get_audit_logs(self, user_id: str) -> List[Dict]:
        """Get audit logs for a specific user"""
        # In a real implementation, this would query the audit log table
        # and return logs related to the specified user
        
        # Mock implementation
        mock_logs = [
            {
                'timestamp': '2023-12-01T10:00:00Z',
                'action': 'data_accessed',
                'details': 'User profile accessed'
            },
            {
                'timestamp': '2023-12-01T10:05:00Z',
                'action': 'data_exported',
                'details': 'Data exported as JSON'
            }
        ]
        
        return mock_logs
    
    def get_all_users_for_deletion(self, days_inactive: int = 365) -> List[str]:
        """Get list of users eligible for data deletion based on inactivity"""
        # In a real implementation, this would query the database
        # for users who have been inactive for the specified number of days
        
        # Mock implementation
        return ['inactive_user_1', 'inactive_user_2']