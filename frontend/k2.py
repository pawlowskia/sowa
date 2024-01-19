import streamlit as st
from streamlit_option_menu import option_menu

user_navbar = option_menu(None, ["", "", "", "", "", ""],
                          icons=['house', 'person-circle', "search", "wallet", "book", "bell"],
                          menu_icon="cast", default_index=0, orientation="horizontal")

worker_navbar = option_menu(None, ["", "", "", "", "", ""],
                            icons=['house', 'person-circle', "search", "file-earmark-bar-graph", "book", "bell"],
                            menu_icon="cast", default_index=0, orientation="horizontal")
