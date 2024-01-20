from streamlit_option_menu import option_menu

def main():
        selected2 = option_menu(None, ["Home", "Upload", "Tasks", 'Settings'],
                                icons=['house', 'cloud-upload', "list-task", 'gear'],
                                menu_icon="cast", default_index=0, orientation="horizontal")
        selected2

if __name__ == "__main__":
    main()
