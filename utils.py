import streamlit as st
import base64
from streamlit.components.v1 import html

from PATHS import NAVBAR_PATHS, SETTINGS


def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Personnalisation de la sélection de la page */
        .css-1n7v3ny.e8zbici1 {
            background-color: #f0f0f0;  /* Couleur de fond pour la sélection */
            color: #333;  /* Couleur du texte pour la sélection */
            border-radius: 5px;  /* Bordure arrondie */
            border: 1px solid #ddd;  /* Bordure fine */
            padding: 5px;  /* Espacement interne */
        }
        
        .css-1n7v3ny.e8zbici1:hover {
            background-color: #e0e0e0;  /* Couleur de fond au survol */
        }
        
        .css-1n7v3ny.e8zbici1:focus {
            outline: 2px solid #007bff;  /* Bordure au focus */
        }
        
        /* Ajustement du style du selectbox dans le menu latéral */
        .css-12ttj6m {
            font-size: 18px;  /* Taille de la police */
        }
        
        .css-12ttj6m select {
            padding: 10px;  /* Espacement interne */
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def navbar_component():
    with open("src/assets/images/settings.png", "rb") as image_file:
        image_as_base64 = base64.b64encode(image_file.read())

    navbar_items = ''
    for key, value in NAVBAR_PATHS.items():
        navbar_items += (f'<a class="navitem" href="/?nav=%2F{value}">{key}</a>')

    settings_items = ''
    for key, value in SETTINGS.items():
        settings_items += (
            f'<a href="/?nav={value}" class="settingsNav">{key}</a>')

    component = rf'''
            <nav class="container navbar" id="navbar">
                <ul class="navlist">
                {navbar_items}
                </ul>
                <div class="dropdown" id="settingsDropDown">
                    <img class="dropbtn" src="data:image/png;base64, {image_as_base64.decode("utf-8")}"/>
                    <div id="myDropdown" class="dropdown-content">
                        {settings_items}
                    </div>
                </div>
            </nav>
            '''
    st.markdown(component, unsafe_allow_html=True)
    js = '''
    <script>
        // navbar elements
        var navigationTabs = window.parent.document.getElementsByClassName("navitem");
        var cleanNavbar = function(navigation_element) {
            navigation_element.removeAttribute('target')
        }
        
        for (var i = 0; i < navigationTabs.length; i++) {
            cleanNavbar(navigationTabs[i]);
        }
        
        // Dropdown hide / show
        var dropdown = window.parent.document.getElementById("settingsDropDown");
        dropdown.onclick = function() {
            var dropWindow = window.parent.document.getElementById("myDropdown");
            if (dropWindow.style.visibility == "hidden"){
                dropWindow.style.visibility = "visible";
            }else{
                dropWindow.style.visibility = "hidden";
            }
        };
        
        var settingsNavs = window.parent.document.getElementsByClassName("settingsNav");
        var cleanSettings = function(navigation_element) {
            navigation_element.removeAttribute('target')
        }
        
        for (var i = 0; i < settingsNavs.length; i++) {
            cleanSettings(settingsNavs[i]);
        }
    </script>
    '''
    html(js)
