import json
from analyzer.ai_analyzer import analyze_with_ai
def analyze_cisco_config(filename=None):
    if filename is None:
        filename = input("Enter the Cisco configuration filename: ")

    with open(filename, "r") as config_file:
        lines = config_file.readlines()

    hostname = "Not found"
    ospf_enabled = False
    bgp_enabled = False
    static_route_count = 0
    static_routes = []
    interfaces = []
    ntp_configured = False
    snmp_v2c_configured = False
    snmp_v3_configured = False
    snmp_version = "Not Configured"
    # Interface analysis state
    interface_count = 0
    interfaces_with_description = 0
    interfaces_shutdown = 0
    

# Track whether we've already started parsing an interface.
# This prevents us from evaluating a "previous" interface
# before we've encountered the first one.
    inside_interface = False
# Tracks whether the current interface contains a description.
# This is evaluated when we reach the next interface (or EOF).
    current_interface_has_description = False
# Tracks whether the current interface has been administratively disabled
# using the "shutdown" command. Evaluated when the interface ends.
    current_interface_is_shutdown = False
    current_interface_name = None
    current_interface_description = None
    current_interface_ip_address = None

    for line in lines:
        if line.startswith("hostname "):
            hostname = line.strip().split(" ", 1)[1]
# Beginning of a new interface.
# Before starting it, evaluate whether the previous interface
# contained a description.
        if line.startswith("interface "):
            if inside_interface:
                # Evaluate previous interface description
                if current_interface_has_description:
                    interfaces_with_description += 1
                if current_interface_is_shutdown:
                    interfaces_shutdown += 1
                 # Evaluate previous interface shutdown status
                interfaces.append({
                    "name": current_interface_name,
                    "description": current_interface_description,
                    "ip_address": current_interface_ip_address,
                    "admin_status": "down" if current_interface_is_shutdown else "up",
                    "oper_status": "not_available",
                    "oper_status_reason": "Static configuration does not contain live operational status"
                })

            interface_count += 1
            current_interface_name = line.strip().split(" ", 1)[1]
            current_interface_description = None
            current_interface_ip_address = None

            inside_interface = True
            current_interface_has_description = False
            current_interface_is_shutdown = False
        if line.strip().startswith("description "):
            current_interface_has_description = True
            current_interface_description = line.strip().split(" ", 1)[1]

        if line.strip().startswith("ip address "):
            current_interface_ip_address = line.strip().split(" ", 2)[2]

        if line.strip().startswith("shutdown"):
            current_interface_is_shutdown = True

        if line.startswith("router ospf "):
            ospf_enabled = True

        if line.startswith("router bgp "):
            bgp_enabled = True  

        if line.startswith("ip route "):
            static_route_count += 1
            static_routes.append(line.strip())

        if line.startswith("ntp server "):
            ntp_configured = True
        
        if line.startswith("snmp-server community "):
            snmp_v2c_configured = True
        if line.startswith("snmp-server group ") or line.startswith("snmp-server user "):
            snmp_v3_configured = True
        if snmp_v2c_configured and snmp_v3_configured:
            snmp_version = "v2c, v3"
        elif snmp_v2c_configured:
            snmp_version = "v2c"
        elif snmp_v3_configured:
            snmp_version = "v3"
# The last interface won't be evaluated by another interface
# statement, so process it after the loop ends.
    if inside_interface:
        if current_interface_has_description:
            interfaces_with_description += 1

        if current_interface_is_shutdown:
            interfaces_shutdown += 1

        interfaces.append({
            "name": current_interface_name,
            "description": current_interface_description,
            "ip_address": current_interface_ip_address,
            "admin_status": "down" if current_interface_is_shutdown else "up",
            "oper_status": "not_available",
            "oper_status_reason": "Static configuration does not contain live operational status"
        })

    interfaces_without_description = interface_count - interfaces_with_description
    interfaces_active = interface_count - interfaces_shutdown

    knowledge_packet = {
    "device": {
        "hostname": hostname
    },
    "interfaces": {
        "total": interface_count,
        "described": interfaces_with_description,
        "undescribed": interfaces_without_description,
        "shutdown": interfaces_shutdown,
        "active": interfaces_active,
        "details": interfaces
    },
    "routing": {
        "ospf_enabled": ospf_enabled,
        "bgp_enabled": bgp_enabled,
        "static_route_count": static_route_count,
        "static_routes": static_routes
    },
    "services": {
        "ntp_configured": ntp_configured,
        "snmp_version": snmp_version
    }
    }
    ai_analysis = analyze_with_ai(knowledge_packet)

    print()
    print("=" * 40)
    print("Cisco Configuration Summary")
    print("=" * 40)
    print()
    print(f"Hostname:               {hostname:<20}")
    # Interface summary
    print(f"Interfaces:             {interface_count}")
    print(f"Interfaces Described:   {interfaces_with_description}")
    print(f"Interfaces Undescribed: {interfaces_without_description}")
    print(f"Interfaces Shutdown:    {interfaces_shutdown}")
    print(f"Interfaces Active:      {interfaces_active}")
    print()
    print("Routing")
    print("-" * 40 )
    print(f"OSPF Enabled:      {ospf_enabled}")
    print(f"BGP Enabled:       {bgp_enabled}")
    print(f"Static Routes:     {static_route_count}")
    print()
    print("Services")
    print("-" * 40)
    print(f"NTP Configured:    {ntp_configured}")
    print(f"SNMP Version:      {snmp_version}")
    print()
    print("AI Knowledge Packet")
    print("-" * 40)
    print(json.dumps(knowledge_packet, indent=4))
    print()

    print()
    print("AI Analysis")
    print("-" * 40)

    for finding in ai_analysis["findings"]:
        print(f"Interface: {finding['interface']}")
        print(f"Severity: {finding['severity']}")
        print(f"Severity Reason: {finding['severity_reason']}")
        print(f"Confidence: {finding['confidence']}")
        print(f"Confidence Reason: {finding['confidence_reason']}")
        print()
        print("Observed Facts:")
        for fact in finding["observed_facts"]:
            print(f"- {fact}")
        print()
        print("Inferences:")
        for inference in finding["inferences"]:
            print(f"- {inference}")
        print()

        print("Possible Impact:")
        for impact in finding["possible_impact"]:
            print(f"- {impact}")
        print()

        print("Recommended Actions:")
        for action in finding["recommended_actions"]:
            print(f"- {action}")
        print()

        print("Additional Data Needed:")
        for data in finding["additional_data_needed"]:
            print(f"- {data}")
        print()

    print("Overall Priority Summary")
    print("-" * 40)

    for priority in ai_analysis["overall_priority_summary"]:
        print(priority)
        
    return ai_analysis