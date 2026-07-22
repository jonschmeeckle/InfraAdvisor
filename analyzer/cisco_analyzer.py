def analyze_cisco_config():
    filename = input("Enter the Cisco configuration filename: ")

    with open(filename, "r") as config_file:
        lines = config_file.readlines()

    hostname = "Not found"

    for line in lines:
        if line.startswith("hostname "):
            hostname = line.strip().split(" ", 1)[1]
            break

    print()
    print("Configuration loaded successfully.")
    print(f"Total lines: {len(lines)}")
    print(f"Hostname: {hostname}")