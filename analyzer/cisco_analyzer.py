def analyze_cisco_config():
    filename = input("Enter the Cisco configuration filename: ")

    with open(filename, "r") as config_file:
        lines = config_file.readlines()

    hostname = "Not found"
    interface_count = 0
    ospf_enabled = False
    bgp_enabled = False
    static_route_count = 0

    for line in lines:
        if line.startswith("hostname "):
            hostname = line.strip().split(" ", 1)[1]

        if line.startswith("interface "):
            interface_count += 1

        if line.startswith("router ospf "):
            ospf_enabled = True

        if line.startswith("router bgp "):
            bgp_enabled = True  

        if line.startswith("ip route "):
            static_route_count += 1

    print()
    print("=" * 40)
    print("Cisco Configuration Summary")
    print("=" * 40)
    print()
    print(f"Hostname:           {hostname:<20}")
    print(f"Interfaces:         {interface_count}")
    print()
    print("Routing")
    print("-" * 40 )
    print(f"OSPF Enabled:      {ospf_enabled}")
    print(f"BGP Enabled:       {bgp_enabled}")
    print(f"Static Routes:     {static_route_count}")