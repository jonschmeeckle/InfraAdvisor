def analyze_cisco_config():
    filename = input("Enter the Cisco configuration filename: ")

    with open(filename, "r") as config_file:
        lines = config_file.readlines()

    hostname = "Not found"

    for line in lines:
        if line.startswith("hostname "):
            hostname = line.strip().split(" ", 1)[1]
            break

    interface_count = 0

    for line in lines:
        if line.startswith("interface "):
            interface_count += 1

    print()
    print("Configuration loaded successfully.")
    print(f"Total lines: {len(lines)}")
    print(f"Hostname: {hostname}")
    print(f"Interfaces: {interface_count}")