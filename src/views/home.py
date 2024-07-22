import streamlit as st
from src.router import redirect
def load_view():

    # Titre de la page
    st.title(f"Projet Fil Rouge ")
    st.header("Répartition et Évolution des effectifs des professionnels de santé par spécialité en France")
    # Introduction
    with st.expander("Introduction"):
        st.markdown("""
    ## Introduction
    Le projet fil rouge porte sur l'analyse de la répartition et de l'évolution des professionnels de santé en France. La répartition des professionnels de santé est inégale à travers le territoire français, avec des disparités marquées entre les régions urbaines et rurales. Cette situation peut affecter l'accès aux soins et la qualité des services médicaux.

    Le but de ce projet est d'analyser la répartition actuelle des professionnels de santé, d'étudier son évolution régionale et de fournir des recommandations pour améliorer l'équilibre des ressources.
    """)

    # Objectifs du Projet
    with st.expander("Objectif du projet"):
         st.markdown("""
    ## Objectifs du Projet
    **Objectif Principal :**  
    Fournir une vue détaillée de la répartition géographique des professionnels de santé en France et analyser son évolution au fil du temps.

    **Objectifs Secondaires :**
    - Identifier les disparités régionales dans la distribution des professionnels de santé.
    - Analyser les tendances d'évolution selon les régions.
    - Proposer des recommandations pour une meilleure répartition des ressources.
    """)

    # Méthodologie
    with st.expander("Méthodologie"):
        st.markdown("""
    ## Méthodologie
    **Approche Globale :**  
    - **Collecte de Données :** Récupération des données sur les professionnels de santé à partir de bases de données publiques et d'organismes de santé.
    - **Prétraitement des Données :** Nettoyage et structuration des données pour l'analyse.
    - **Analyse :** Utilisation de méthodes statistiques pour évaluer la répartition et les tendances.
    - **Visualisation :** Création de cartes et de graphiques pour illustrer les résultats.
    - **Recommandations :** Élaboration de suggestions pour optimiser la répartition des professionnels de santé.

    **Outils et Technologies :**
    - Python (Pandas, NumPy, Matplotlib, Seaborn)
    - Logiciels SIG (QGIS, ArcGIS)
    - Outils de visualisation interactive (Tableau, Power BI)
    """)

    # Plan de Travail et Chronogramme
    with st.expander("Plan de Travail et Chronogramme"):
        st.markdown("""
    ## Plan de Travail et Chronogramme
    **Planification :**
    1. **Phase 1 :** Collecte de données (Mois 1)
    2. **Phase 2 :** Prétraitement et structuration des données (Mois 2)
    3. **Phase 3 :** Analyse des données (Mois 3)
    4. **Phase 4 :** Création de visualisations et de rapports (Mois 4)
    5. **Phase 5 :** Présentation des résultats et recommandations (Mois 5)

    **Chronogramme :**
    - Un calendrier avec les jalons clés pour chaque phase du projet.
    """)

    # Ressources et Budget
    with st.expander("Ressources et Budget"):
        st.markdown("""
    ## Ressources et Budget
    **Ressources Humaines :**
    - Data scientists
    - Analystes de données
    - Experts en SIG
    - Développeurs de visualisation

    **Ressources Matérielles :**
    - Accès aux bases de données
    - Logiciels d'analyse et de visualisation
    - Matériel informatique

    **Budget :**
    - Estimation des coûts pour l'acquisition des données, les outils logiciels, et les ressources humaines nécessaires.
    """)

    # Résultats Attendus
    with st.expander("Résultats Attendus", expanded=True):
        st.markdown("""
    ## Résultats Attendus
    **Produits Livrables :**
    - Cartes interactives montrant la répartition des professionnels de santé par région.
    - Rapports détaillés sur les tendances et les disparités régionales.
    - Recommandations pour optimiser la répartition des professionnels de santé.

    **Bénéfices Anticipés :**
    - Amélioration de la compréhension de la répartition des ressources médicales.
    - Aide à la prise de décision pour les politiques de santé publique.
    - Identification des régions nécessitant une attention particulière pour améliorer l'accès aux soins.
    """)

    # Risques et Gestion des Risques
    with st.expander("Risques et Gestion des Risques", expanded=True):
         st.markdown("""
    ## Risques et Gestion des Risques
    **Identification des Risques :**
    - Difficulté à obtenir des données complètes et précises.
    - Erreurs dans le prétraitement des données.
    - Limites des outils de visualisation et d'analyse.

    **Stratégies de Mitigation :**
    - Utilisation de sources de données multiples pour assurer la précision.
    - Vérification et validation rigoureuse des données traitées.
    - Utilisation d'outils éprouvés et recours à des experts en SIG et en analyse de données.
    """)

    # Conclusion
    with st.expander("Conclusion"):
        st.markdown("""
    ## Conclusion
    **Résumé :**  
    Le projet vise à offrir une vue d'ensemble sur la répartition des professionnels de santé en France, à analyser son évolution, et à fournir des recommandations pour une meilleure répartition régionale.

    **Appel à l'Action :**  
    Encourager les parties prenantes à utiliser les résultats pour améliorer les politiques de santé et optimiser la répartition des ressources médicales.
    """)

    # Questions et Réponses
    with st.expander("Questions et Réponses"):
        st.markdown("""
    ## Questions et Réponses
    Ouvrir la session aux questions et aux discussions pour clarifier les points soulevés durant la présentation. Répondre aux préoccupations et suggestions des parties prenantes.
    """)
