from banner import display_banner
from menu import display_menu
from menu import get_menu_choice
from analyzer.cisco_analyzer import analyze_cisco_config
def main():
    version = "0.1"

    display_banner(version)

    while True:
        display_menu()

        choice = get_menu_choice()

        print()

        if choice == "1":
            analyze_cisco_config()
            print()

        elif choice == "2":
            print("Palo Alto configuration analysis is coming soon.")
            print()

        elif choice == "3":
            print("Executive summary generation is coming soon.")
            print()

        elif choice == "4":
            print("Exiting InfraAdvisor.")
            break

        else:
            print("Invalid selection. Please choose a number from 1 to 4.")
            print()


if __name__ == "__main__":
    main()