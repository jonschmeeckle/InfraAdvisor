from banner import display_banner
from menu import display_menu
from menu import get_menu_choice
def main():
    version = "0.1"

    display_banner(version)

    while True:
        display_menu()

        choice = get_menu_choice()

        print()

        if choice == "4":
            print("Exiting InfraAdvisor.")
            break
        else:
            print(f"You selected option {choice}.")
            print()

if __name__ == "__main__":
    main()