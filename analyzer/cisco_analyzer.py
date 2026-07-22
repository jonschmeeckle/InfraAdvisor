def analyze_cisco_config():
    filename = input("Enter the Cisco configuration filename: ")

    with open(filename, "r") as config_file:
        lines = config_file.readlines()

    print()
    print(f"Configuration loaded successfully.")
    print(f"Total lines: {len(lines)}")