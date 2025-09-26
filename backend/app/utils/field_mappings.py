"""
Field mappings for different log sources and security events
"""

# Common security log fields mapping
SECURITY_FIELD_MAPPINGS = {
    "timestamp": ["@timestamp", "timestamp", "time", "event_time"],
    "source_ip": ["src_ip", "source_ip", "client_ip", "remote_addr"],
    "destination_ip": ["dst_ip", "dest_ip", "destination_ip", "server_ip"],
    "user": ["user", "username", "user_name", "account"],
    "event_type": ["event_type", "event", "action", "activity"],
    "severity": ["severity", "level", "priority", "alert_level"],
    "message": ["message", "description", "summary", "event_description"]
}

def get_field_mapping(field_name: str, log_source: str = "generic"):
    """Get possible field names for a given field"""
    return SECURITY_FIELD_MAPPINGS.get(field_name, [field_name])