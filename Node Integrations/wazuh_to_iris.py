'''
Wazuh to IRIS Alert Integration Script
------------------------------------

Purpose:
    This script processes Wazuh security logs in JSON format and transforms them into
    IRIS-compatible alert formats for security incident tracking and response.

Features:
    - Converts Wazuh alert levels to IRIS severity levels
    - Maps agent names and group labels to customer IDs
    - Generates standardized IRIS alert payload
    - Handles missing or invalid input gracefully

Usage:
    Deploy this script in a Shuffle workflow environment where it can access
    Wazuh alert data and forward to IRIS API.

Author: Mark L.
Environment: Shuffle Automation Platform
Version: 1.0
'''

import json

# Severity Mapping
# Converts Wazuh alert levels (0-15) to IRIS severity levels (1-6)
alert_level = int($dummy.value.added)  # Expected Wazuh rule level

def map_severity(alert_level):
    """
    Maps Wazuh alert levels to IRIS severity levels.
    
    Args:
        alert_level (int): Wazuh alert level (0-15)
    
    Returns:
        int: IRIS severity level (1-6)
    """
    if alert_level < 5:
        return 2  
    elif alert_level >= 5 and alert_level < 7:
        return 3  
    elif alert_level >= 7 and alert_level < 10:
        return 4  
    elif alert_level >= 10 and alert_level < 13:
        return 5
    elif alert_level >= 13:
        return 6  
    else:
        return 1  

severity = map_severity(alert_level)

def get_customer_id(agent_name_var, group_label_var, customer_mappings):
    """
    Determines customer ID based on agent name or group label.
    
    Args:
        agent_name_var (str): Name of the Wazuh agent
        group_label_var (str): Wazuh group label
        customer_mappings (dict): Mapping of customer names to their IDs
    
    Returns:
        int: Customer ID (defaults to 1 if no match found)
    """
    # First try matching by group label
    if group_label_var and not group_label_var.startswith('$'):
        try:
            return customer_mappings[group_label_var.lower()]
        except KeyError:
            pass
    
    # If no group label match, try matching by agent name
    if agent_name_var and not agent_name_var.startswith('$'):
        name_parts = agent_name_var.lower().replace("-", " ").replace("_", " ").split()
        for customer_name, customer_id in customer_mappings.items():
            if customer_name.lower() in name_parts:
                return customer_id

    return 1  # Default customer ID if no matches found

# Customer ID mapping dictionary
# Format: "customer_name": customer_id
CUSTOMER_MAPPINGS = {
    "test1": 1,  # Replace with actual customer names and IDs
    "test2": 2,
    "test3": 3,
}

# Input variables (replace $dummy.value.added with actual Shuffle variables)
agent_name = "$dummy.value.added"  # Wazuh agent name
group_label = "$dummy.value.added"  # Wazuh group label

customer_id = get_customer_id(agent_name, group_label, CUSTOMER_MAPPINGS)

# IRIS Alert Payload Construction
# Reference: IRIS API documentation for alert creation
payload = json.dumps({
    # Alert Metadata
    "alert_title": "$dummy.value.added",
    "alert_description": "$dummy.value.added",
    "alert_source": "String value for reference name",
    "alert_source_ref": "String value for reference source",
    "alert_source_link": "URL of Source",
    
    # Alert Classification
    "alert_severity_id": severity,
    "alert_status_id": 2,  # Default status (e.g., 2 = New)
    "alert_classification_id": 1,  # Alert type classification
    
    # Alert Details
    "alert_context": "",
    "alert_source_event_time": "$dummy.value.added",
    "alert_note": "Rule ID: $dummy.value.added Alert ID: $dummy.value.added **include some message or additional info/details**",
    "alert_tags": "String value for tags. The string values are separated by a comma",
    "alert_iocs": "",
    
    # Asset Information
    "alert_assets": [
        {
            "asset_name": "$dummy.value.added",
            "asset_description": "String value for the assest description",
            "asset_type_id": 1,  # Asset type identifier
            "asset_ip": "$dummy.value.added",
            "asset_domain": "String value for the domain",
            "asset_tags": "String value for tags. The string values are separated by a comma",
        }
    ],
    
    # Customer Information
    "alert_customer_id": customer_id,
    "alert_source_content": ""
})

print(payload)
