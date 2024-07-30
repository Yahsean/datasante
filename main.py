import streamlit as st
import json
import utils as utl

from src.views import home, goal, dataset, analysis, conclusion, options, login, logout
from src.router import get_route, redirect



# Configuration de l'application Streamlit
st.set_page_config(layout="wide", page_title='Projet Fil Rouge')
#st.set_option('deprecation.showPyplotGlobalUse', False)

# Afficher le logo dans le menu latéral
st.sidebar.image("data/logo.jpg", use_column_width=True)

# Injecter le CSS personnalisé
utl.inject_custom_css()

# Fonction pour créer un bouton stylisé
def custom_sidebar_button(button_text, redirect_target):
    button_html = f"""
    <a href="javascript:void(0);" class="custom-button" onclick="window.location.href='{redirect_target}'">
        {button_text}
    </a>
    """
    st.sidebar.markdown(button_html, unsafe_allow_html=True)

# Fonction pour afficher le menu personnalisé
def custom_sidebar():
    # Menu de navigation
    st.sidebar.title("Projet Fil Rouge")
    st.sidebar.header("Réalisé par Yassine RAZINE")
    
    # Utilisation de selectbox pour la sélection de la page
    selected_page = st.sidebar.selectbox(
        "Navigation",
        ["Accueil", "Objectifs", "Données", "Analyse", "Conclusion"]
    )
    
    # Séparateur
    #st.sidebar.markdown("---")

    
    # Paramètres supplémentaires
    #st.sidebar.write("### Auteur du projet")
    #param1 = st.sidebar.slider("Sélectionnez un paramètre", 0, 100, 50)
    #param2 = st.sidebar.selectbox("Choisissez une option", ["Option 1", "Option 2", "Option 3"])
    
    # Séparateur pour les boutons spéciaux
    st.sidebar.markdown("---")
    st.sidebar.subheader("Gestion du compte")
    
    # Boutons spéciaux
    if st.sidebar.button("Se Déconnecter"):
        redirect("logout")
    elif st.sidebar.button("Se Connecter"):
        redirect("login")
    
    # Ajout d'un bouton d'options
    if st.sidebar.button("Options"):
        redirect("options")


    # Gestion du compte
    st.sidebar.subheader("Gestion du compte")
    
    # Boutons spéciaux
    custom_sidebar_button("Se Déconnecter", "logout")
    custom_sidebar_button("Se Connecter", "login")
    custom_sidebar_button("Options", "options")

    return selected_page

# Fonction principale de navigation
def navigation():
    # Charger les cookies
    with open('session.json') as json_file:
        SESSION = json.load(json_file)
    
    # Vérifier l'utilisateur dans les cookies
    if SESSION.get("email", "") == "":
        redirect("login")
    
    selected_page = custom_sidebar()
    
    route = {
        "Accueil": "/home",
        "Objectifs": "/goal",
        "Données": "/dataset",
        "Analyse": "/analysis",
        "Conclusion": "/conclusion"
    }.get(selected_page, "/home")
    
    # Contenu principal
    col1, col2 = st.columns([1, 4])
    
    with col2:
        if route == "/home":
            home.load_view()
        elif route == "/goal":
            goal.load_view()
        elif route == "/dataset":
            dataset.load_view()
        elif route == "/analysis":
            analysis.load_view()
        elif route == "/conclusion":
            conclusion.load_view()
        elif route == "/options":
            options.load_view()
        elif route == "/logout":
            logout.load_view()
        elif route == "/login":
            login.load_view()
        else:
            redirect("/home")
            home.load_view()

# Exécuter la fonction de navigation
if __name__ == "__main__":
    navigation()
