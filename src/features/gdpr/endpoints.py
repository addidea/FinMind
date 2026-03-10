# GDPR Compliance Endpoints
import json
import csv
import io
from datetime import datetime
from flask import Blueprint, request, jsonify, Response
from src.features.gdpr.service import GDPRService
from src.features.gdpr.audit import log_gdpr_action

gdpr_bp = Blueprint('gdpr', __name__)

gdpr_service = GDPRService()


def validate_user_id(user_id):
    """Validate user ID format"""
    if not user_id or not isinstance(user_id, str) or len(user_id.strip()) == 0:
        return False
    return True


def validate_auth_token(token):
    """Validate authentication token"""
    # In a real implementation, this would verify JWT or session token
    # For now, we'll implement basic validation
    if not token or not isinstance(token, str) or len(token.strip()) < 10:
        return False
    return True


@gdpr_bp.route('/export/<user_id>', methods=['GET'])
def export_user_data(user_id):
    """Export user data in JSON or CSV format"""
    auth_header = request.headers.get('Authorization')
    
    if not validate_user_id(user_id):
        log_gdpr_action(user_id, 'export_attempt_failed', 'Invalid user ID')
        return jsonify({'error': 'Invalid user ID'}), 400
    
    if not auth_header or not validate_auth_token(auth_header.replace('Bearer ', '')):
        log_gdpr_action(user_id, 'export_attempt_failed', 'Unauthorized access attempt')
        return jsonify({'error': 'Unauthorized'}), 401
    
    format_type = request.args.get('format', 'json').lower()
    
    try:
        user_data = gdpr_service.get_user_data(user_id)
        
        if not user_data:
            log_gdpr_action(user_id, 'export_attempt_failed', 'User not found')
            return jsonify({'error': 'User not found'}), 404
        
        if format_type == 'csv':
            csv_content = gdpr_service.convert_to_csv(user_data)
            log_gdpr_action(user_id, 'data_exported', f'Exported as CSV, {len(csv_content)} bytes')
            return Response(
                csv_content,
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename=user_{user_id}_data.csv'}
            )
        else:
            log_gdpr_action(user_id, 'data_exported', f'Exported as JSON, {len(json.dumps(user_data))} bytes')
            return Response(
                json.dumps(user_data, indent=2, default=str),
                mimetype='application/json',
                headers={'Content-Disposition': f'attachment; filename=user_{user_id}_data.json'}
            )
    except Exception as e:
        log_gdpr_action(user_id, 'export_error', str(e))
        return jsonify({'error': 'Internal server error during export'}), 500


@gdpr_bp.route('/delete/<user_id>', methods=['DELETE'])
def delete_user_data(user_id):
    """Delete all user data"""
    auth_header = request.headers.get('Authorization')
    
    if not validate_user_id(user_id):
        log_gdpr_action(user_id, 'delete_attempt_failed', 'Invalid user ID')
        return jsonify({'error': 'Invalid user ID'}), 400
    
    if not auth_header or not validate_auth_token(auth_header.replace('Bearer ', '')):
        log_gdpr_action(user_id, 'delete_attempt_failed', 'Unauthorized access attempt')
        return jsonify({'error': 'Unauthorized'}), 401
    
    confirmation = request.json.get('confirm', False) if request.json else False
    
    if not confirmation:
        log_gdpr_action(user_id, 'delete_attempt_failed', 'Deletion not confirmed')
        return jsonify({'error': 'Deletion must be confirmed by setting confirm=true'}), 400
    
    try:
        result = gdpr_service.delete_user_data(user_id)
        
        if result:
            log_gdpr_action(user_id, 'data_deleted', 'All user data successfully deleted')
            return jsonify({'message': 'User data successfully deleted'}), 200
        else:
            log_gdpr_action(user_id, 'delete_failed', 'User not found')
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        log_gdpr_action(user_id, 'delete_error', str(e))
        return jsonify({'error': 'Internal server error during deletion'}), 500


@gdpr_bp.route('/audit/<user_id>', methods=['GET'])
def get_audit_log(user_id):
    """Get audit log for a specific user"""
    auth_header = request.headers.get('Authorization')
    
    if not validate_user_id(user_id):
        return jsonify({'error': 'Invalid user ID'}), 400
    
    if not auth_header or not validate_auth_token(auth_header.replace('Bearer ', '')):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        audit_logs = gdpr_service.get_audit_logs(user_id)
        return jsonify(audit_logs), 200
    except Exception as e:
        return jsonify({'error': 'Error retrieving audit logs'}), 500