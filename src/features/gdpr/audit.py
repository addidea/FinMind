# GDPR Audit Logging
import json
from datetime import datetime
from typing import Dict, Any

# In a real implementation, this would connect to a database or logging service
audit_log_storage = []


def log_gdpr_action(user_id: str, action: str, details: str = ""):
    """Log GDPR-related actions for compliance auditing"""
    log_entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'user_id': user_id,
        'action': action,
        'details': details,
        'ip_address': '',  # Would capture from request in actual implementation
        'user_agent': ''   # Would capture from request in actual implementation
    }
    
    # In a real implementation, this would save to a database or logging system
    # For now, we'll just append to our in-memory list
    audit_log_storage.append(log_entry)
    
    # Also print to standard output for visibility during development
    print(f"GDPR Audit Log: {json.dumps(log_entry)}")


def get_audit_logs(user_id: str = None) -> list:
    """Retrieve audit logs, optionally filtered by user_id"""
    if user_id:
        return [log for log in audit_log_storage if log['user_id'] == user_id]
    return audit_log_storage


def get_compliance_report() -> Dict[str, Any]:
    """Generate a GDPR compliance report"""
    total_actions = len(audit_log_storage)
    
    action_counts = {}
    for log in audit_log_storage:
        action = log['action']
        action_counts[action] = action_counts.get(action, 0) + 1
    
    return {
        'report_generated_at': datetime.utcnow().isoformat(),
        'total_audit_entries': total_actions,
        'action_breakdown': action_counts,
        'recent_activities': audit_log_storage[-10:]  # Last 10 entries
    }