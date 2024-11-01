'''
This script is a work in progress. However, the general idea is this script will 
take in logs in JSON format from Wazuh, parse them, and assign values according
to the IRIS API. Dummy values were assigned to prevent client leakage.

This was script was created by Mark L. for use within a Shuffle environment.
'''

import json

# Dummy plug applied. You'll need to change the value to reflect your variables, i.e. $shuffle.something.etc
alert_level = int($dummy.value.added) # Make sure this is the rule level and the Wazuh severity level.

if alert_level < 5:
    severity = 2
elif alert_level >= 5 and alert_level < 7:
    severity = 3
elif alert_level >= 7 and alert_level < 10:
    severity = 4
elif alert_level >= 10 and alert_level < 13:
    severity = 5
elif alert_level >= 13:
    severity = 6
else:
    severity = 1

def get_customer_id(agent_name_var, group_label_var, customer_mappings):
    if group_label_var and not group_label_var.startswith('$'): # this is a catch for when they value isn't there.
        try:
            return customer_mappings[group_label_var.lower()]
        except KeyError:
            pass
    
    if agent_name_var and not agent_name_var.startswith('$'): 
        name_parts = agent_name_var.lower().replace("-", " ").replace("_", " ").split()
        for customer_name, customer_id in customer_mappings.items():
            if customer_name.lower() in name_parts:
                return customer_id

    return 1
# I've removed the clients names, but the key is a string that reflects the customer and the key is the integer that reflects that customer.
CUSTOMER_MAPPINGS = {
    "test1": 1,
    "test2": 2,
    "test3": 3,
}

# Dummy plug applied. You'll need to change the value to reflect your variables, i.e. $shuffle.something.etc
agent_name = "$dummy.value.added"
group_label = "$dummy.value.added"

customer_id = get_customer_id(agent_name, group_label, CUSTOMER_MAPPINGS)

# It is possible to add more to the JSON output, but this worked as is for our application. Ref the IRIS API for adding alerts.
payload = json.dumps({
    "alert_title": "$dummy.value.added",
    "alert_description": "$dummy.value.added",
    "alert_source": "String value for reference name",
    "alert_source_ref": "String value for reference source",
    "alert_source_link": "URL of Source",
    "alert_severity_id": severity,
    "alert_status_id": 2, # This can be change, but is an integer value. 
    "alert_context": "",
    "alert_source_event_time": "$dummy.value.added",
    "alert_note": "Rule ID: $dummy.value.added Alert ID: $dummy.value.added **include some message or additional info/details**",
    "alert_tags": "String value for tags. The string values are separated by a comma",
    "alert_iocs": "",
    "alert_assets": [
        {
            "asset_name": "$dummy.value.added",
            "asset_description": "String value for the assest description",
            "asset_type_id": 1, # This value is an integer that changes the assest type. This can be done dynamically as well with more code.
            "asset_ip": "$dummy.value.added",
            "asset_domain": "String value for the domain",
            "asset_tags": "String value for tags. The string values are separated by a comma",
        }
    ],
    "alert_customer_id": customer_id,
    "alert_classification_id": 1,
    "alert_source_content": ""
})

print(payload)