import streamlit as st
import plotly.express as px
import pandas as pd
import json

def load_view():
    st.title("Visualisation des Effectifs par Spécialité")

    # Ajouter du CSS personnalisé pour élargir le corps de la page
    st.markdown("""
        <style>
        .reportview-container {
            max-width: 1200px;
            margin: 0 auto;
        }
        .main {
            padding: 2rem;
        }
        .stButton > button {
            width: 100%;
            height: 100%;
        }
        .icon-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
        }
        .icon-container div {
            margin: 20px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Charger les données géographiques (GeoJSON)
    with open("data/departements.geojson") as f:
        departements_geojson = json.load(f)
    
    with open("data/regions.geojson") as f:
        regions_geojson = json.load(f)
    
    # Charger les données principales
    dataset = "data/demographie-exercices-liberaux.csv"
    df = pd.read_csv(dataset, sep=';')

    # Convertir la colonne 'annee' en entier pour la sélection
    df['annee'] = df['annee'].astype(int)

    # Initialiser les valeurs dans session state si elles n'existent pas
    if 'selected_years' not in st.session_state:
        st.session_state.selected_years = [max(df['annee'].unique())]
    if 'visualization_option' not in st.session_state:
        st.session_state.visualization_option = None
    if 'selected_professions' not in st.session_state:
        st.session_state.selected_professions = []
    if 'selected_regions' not in st.session_state:
        st.session_state.selected_regions = []
    if 'selected_departements' not in st.session_state:
        st.session_state.selected_departements = []
    if 'selected_evolution_profession' not in st.session_state:
        st.session_state.selected_evolution_profession = []

    # Filtrage par colonne 'Année' (sélection multiple via liste déroulante)
    years = sorted(df['annee'].unique())
    st.session_state.selected_years = st.multiselect(
        "Sélectionnez les années", 
        options=years, 
        default=st.session_state.selected_years
    )

    # Icônes pour choisir la visualisation
    st.markdown("<div class='icon-container'>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Graphique en barres"):
            st.session_state.visualization_option = "Graphique en barres"
    
    with col2:
        if st.button("🍰 Camembert"):
            st.session_state.visualization_option = "Camembert"
    
    with col3:
        if st.button("📈 Évolution Annuelle"):
            st.session_state.visualization_option = "Évolution Annuelle"
    
    with col4:
        if st.button("🗺️ Carte Géographique"):
            st.session_state.visualization_option = "Carte Géographique"

    st.markdown("</div>", unsafe_allow_html=True)

    # Utilisation des colonnes pour organiser le contenu
    main_col, side_col = st.columns([3, 1])

    with main_col:
        if st.session_state.visualization_option is None:
            st.warning("Veuillez sélectionner un type de visualisation.")
            return

        # Assurez-vous que les valeurs sont des listes, même si elles sont uniques
        selected_professions = st.session_state.selected_professions
        selected_regions = st.session_state.selected_regions
        selected_departements = st.session_state.selected_departements
        selected_evolution_profession = st.session_state.selected_evolution_profession
        
        # Afficher les filtres en fonction du type de visualisation sélectionné
        with side_col:
            st.subheader("Filtres")
            professions = sorted(df['profession_sante'].unique())
            regions = sorted(df['libelle_region'].unique())
            
            if st.session_state.visualization_option == "Graphique en barres":
             
                selected_professions = st.selectbox("Sélectionnez les professions", options=professions, index=0)
                selected_regions = st.multiselect("Sélectionnez les régions", options=regions, default=selected_regions)
                
                if selected_regions:
                    departements = sorted(df[df['libelle_region'].isin(selected_regions)]['libelle_departement'].unique())
                else:
                    departements = []
                selected_departements = st.multiselect("Sélectionnez les départements", options=departements, default=selected_departements)

                # Mettre à jour les valeurs dans session state
                st.session_state.selected_professions = [selected_professions] if isinstance(selected_professions, str) else selected_professions
                st.session_state.selected_departements = [dept for dept in selected_departements if dept != "Tout département"]
                st.session_state.selected_regions = [region for region in selected_regions if region]


                # Filtrer les données en fonction des sélections
                filtered_df = df[
                    (df['profession_sante'].isin(st.session_state.selected_professions)) &
                    (df['libelle_region'].isin(st.session_state.selected_regions)) &
                    (df['libelle_departement'].isin(st.session_state.selected_departements))
                ]

                # Générer le graphique en barres
                if not filtered_df.empty:
                    fig = px.bar(filtered_df, x='libelle_region', y='effectif', color='annee', barmode='group',
                                title=f'Évolution des Effectifs pour {selected_professions} par Région et Département',
                                labels={'libelle_region': 'Région', 'effectif': 'Effectif', 'annee': 'Année'},
                                text='effectif')

                    fig.update_layout(
                        xaxis=dict(title='Région'),
                        yaxis=dict(title='Effectif'),
                        legend=dict(title='Année')
                    )
            elif st.session_state.visualization_option == "Camembert":
                selected_professions = st.selectbox("Sélectionnez les professions", options=professions, index=0)
                selected_regions = st.multiselect("Sélectionnez les régions", options=regions, default=selected_regions)
                
                if selected_regions:
                    departements = sorted(df[df['libelle_region'].isin(selected_regions)]['libelle_departement'].unique())
                else:
                    departements = []
                selected_departements = st.multiselect("Sélectionnez les départements", options=departements, default=selected_departements)

                # Mettre à jour les valeurs dans session state
                st.session_state.selected_professions = [selected_professions] if isinstance(selected_professions, str) else selected_professions
                st.session_state.selected_departements = [dept for dept in selected_departements if dept != "Tout Département"]
                st.session_state.selected_regions = [region for region in selected_regions if region]

            elif st.session_state.visualization_option == "Évolution Annuelle":
                selected_evolution_profession = st.selectbox("Sélectionnez la spécialité", options=professions, index=0)
                selected_regions = st.multiselect("Sélectionnez les régions", options=regions, default=selected_regions)
                
                if selected_regions:
                    departements = sorted(df[df['libelle_region'].isin(selected_regions)]['libelle_departement'].unique())
                else:
                    departements = []
                selected_departements = st.multiselect("Sélectionnez les départements", options=departements, default=selected_departements)
                
                st.session_state.selected_evolution_profession = [selected_evolution_profession] if isinstance(selected_evolution_profession, str) else selected_evolution_profession
                st.session_state.selected_departements = [dept for dept in selected_departements if dept != "Tout Département"]
                st.session_state.selected_regions = [region for region in selected_regions if region]

            elif st.session_state.visualization_option == "Carte Géographique":
                selected_professions = st.multiselect("Sélectionnez les professions", options=professions, default=selected_professions)
                selected_regions = st.multiselect("Sélectionnez les régions", options=regions, default=selected_regions)
                
                if selected_regions:
                    departements = sorted(df[df['libelle_region'].isin(selected_regions)]['libelle_departement'].unique())
                else:
                    departements = []
                selected_departements = st.multiselect("Sélectionnez les départements", options=departements, default=selected_departements)
                
                st.session_state.selected_professions = [prof for prof in selected_professions if prof]
                st.session_state.selected_departements = [dept for dept in selected_departements if dept != "Tout département"]
                st.session_state.selected_regions = [region for region in selected_regions if region]

        # Filtrage des données
        if not st.session_state.selected_years:
            st.warning("Veuillez sélectionner au moins une année.")
            return

        filtered_df = df[
            (df['annee'].isin(st.session_state.selected_years)) &
            (df['profession_sante'].isin(st.session_state.selected_professions) if st.session_state.selected_professions else True) &
            (df['libelle_region'].isin(st.session_state.selected_regions) if st.session_state.selected_regions else True) &
            (df['libelle_departement'].isin(st.session_state.selected_departements) if st.session_state.selected_departements else True)
        ]

        # Exclure "Tout Département" des résultats
        filtered_df = filtered_df[filtered_df['libelle_departement'] != "Tout département"]
        filtered_df = filtered_df[filtered_df['departement'] != "999"]

        # Générer les visualisations
        if st.session_state.visualization_option == "Graphique en barres":
            if st.session_state.selected_regions:
                if len(st.session_state.selected_regions) == 1:
                    # Afficher les départements dans la région sélectionnée
                    selected_region = st.session_state.selected_regions[0]
                    filtered_df_region = filtered_df[filtered_df['libelle_region'] == selected_region]

                    if len(st.session_state.selected_departements) > 0:
                        grouped_df = filtered_df_region.groupby(['libelle_departement', 'profession_sante']).agg({'effectif': 'sum'}).reset_index()
                    else:
                        grouped_df = filtered_df_region.groupby(['libelle_departement', 'profession_sante']).agg({'effectif': 'sum'}).reset_index()

                    fig = px.bar(grouped_df, x='libelle_departement', y='effectif', color='profession_sante',
                                title=f'Effectifs par Département dans la Région {selected_region} pour les années {", ".join(map(str, st.session_state.selected_years))}',
                                labels={'libelle_departement': 'Département', 'effectif': 'Effectif', 'profession_sante': 'Spécialité'},
                                barmode='group')  # Changer barmode en 'group'
                else:
                    # Afficher les données globales ou par région
                    if len(st.session_state.selected_regions) > 1:
                        grouped_df = filtered_df.groupby(['libelle_region', 'libelle_departement', 'profession_sante']).agg({'effectif': 'sum'}).reset_index()
                    else:
                        grouped_df = filtered_df.groupby(['libelle_departement', 'profession_sante']).agg({'effectif': 'sum'}).reset_index()

                    fig = px.bar(grouped_df, x='libelle_departement', y='effectif',
                                title=f'Effectifs par Département pour les années {", ".join(map(str, st.session_state.selected_years))}',
                                labels={'libelle_departement': 'Département', 'effectif': 'Effectif', 'libelle_region': 'Région'},
                                barmode='group')  # Changer barmode en 'group'
            else:
                # Si aucune région n'est sélectionnée, afficher les effectifs par région
                grouped_df = filtered_df.groupby(['libelle_region', 'profession_sante']).agg({'effectif': 'sum'}).reset_index()

                fig = px.bar(grouped_df, x='libelle_region', y='effectif', color='profession_sante',
                            title=f'Effectifs par Région pour les années {", ".join(map(str, st.session_state.selected_years))}',
                            labels={'libelle_region': 'Région', 'effectif': 'Effectif', 'profession_sante': 'Spécialité'},
                            barmode='group')  # Changer barmode en 'group'

            st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.visualization_option == "Camembert":

            if st.session_state.selected_professions and st.session_state.selected_regions:
                filtered_df = filtered_df[
                    (filtered_df['profession_sante'].isin(st.session_state.selected_professions)) &
                    (filtered_df['libelle_region'].isin(st.session_state.selected_regions))
                ]
                
                if st.session_state.selected_departements:
                    filtered_df = filtered_df[filtered_df['libelle_departement'].isin(st.session_state.selected_departements)]
                
                exercise_type_df = filtered_df.groupby('type_exercice_liberal').agg({'effectif': 'sum'}).reset_index()
                exercise_type_df['type_exercice_liberal'] = exercise_type_df['type_exercice_liberal'].map({2: 'Libéral Mixte', 1: 'Libéral Exclusif'})
                
                fig = px.pie(
                    exercise_type_df,
                    names='type_exercice_liberal',
                    values='effectif',
                    title=f'Repartition des Types d\'Exercice pour {", ".join(st.session_state.selected_professions)} en {", ".join(st.session_state.selected_regions)}'
                )
                
                st.plotly_chart(fig, use_container_width=True)

        elif st.session_state.visualization_option == "Évolution Annuelle":
            # Générer le graphique d'évolution annuelle
            if st.session_state.selected_evolution_profession:
                evolution_by = st.radio("Choisissez la dimension pour l'évolution annuelle", ["Région", "Département"])

                if evolution_by == "Région":
                    grouped_df = filtered_df.groupby(['annee', 'libelle_region']).agg({'effectif': 'sum'}).reset_index()
                    fig = px.line(grouped_df, x='annee', y='effectif', color='libelle_region',
                                title=f'Évolution Annuelle des Effectifs par Région pour les spécialités {", ".join(st.session_state.selected_evolution_profession)}',
                                labels={'annee': 'Année', 'effectif': 'Effectif', 'libelle_region': 'Région'},
                                markers=True)  # Ajouter des marqueurs pour les points
                else:
                    grouped_df = filtered_df.groupby(['annee', 'libelle_departement']).agg({'effectif': 'sum'}).reset_index()
                    fig = px.line(grouped_df, x='annee', y='effectif', color='libelle_departement',
                                title=f'Évolution Annuelle des Effectifs par Département pour les spécialités {", ".join(st.session_state.selected_evolution_profession)}',
                                labels={'annee': 'Année', 'effectif': 'Effectif', 'libelle_departement': 'Département'},
                                markers=True)  # Ajouter des marqueurs pour les points

                
                st.plotly_chart(fig, use_container_width=True)


        elif st.session_state.visualization_option == "Carte Géographique":
            # Générer la carte géographique
            grouped_df = filtered_df.groupby(['libelle_departement']).agg({'effectif': 'sum'}).reset_index()
            
            # Filtrage des données
            if not st.session_state.selected_years or not st.session_state.selected_professions:
                st.warning("Veuillez sélectionner au moins une année et une spécialité.")
                return

            filtered_df = df[
                (df['annee'].isin(st.session_state.selected_years)) &
                (df['profession_sante'].isin(st.session_state.selected_professions))
            ]

            # Exclure "Tout Département" des résultats
            filtered_df = filtered_df[filtered_df['libelle_departement'] != "Tout département"]
            filtered_df = filtered_df[filtered_df['departement'] != "999"]
            filtered_df = filtered_df[filtered_df['region'] != "99"]



            fig = px.choropleth_mapbox(
                grouped_df,
                geojson=departements_geojson,
                locations='libelle_departement',
                featureidkey="properties.nom",
                color='effectif',
                color_continuous_scale="Viridis",
                range_color=(0, grouped_df['effectif'].max()),
                mapbox_style="carto-positron",
                zoom=5,
                center={"lat": 46.603354, "lon": 1.888334},
                opacity=0.5,
                labels={'effectif': 'Effectif'},
                title=f'Effectifs par Département pour les années {", ".join(map(str, st.session_state.selected_years))}'
            )
            st.plotly_chart(fig, use_container_width=True)
# Ajouter une section de texte explicatif avant chaque graphique
    if st.session_state.visualization_option == "Graphique en barres":
        st.markdown("""
            ### Objectif du Graphique en Barres
            Le graphique en barres permet de comparer les effectifs des professionnels de santé entre les différentes régions ou départements d'une même région sélectionnés. 
            Il met en évidence les variations d'effectifs par année, ce qui permet de visualiser les tendances et les différences géographiques.
        """)


    elif st.session_state.visualization_option == "Camembert":
        st.markdown("""
            ### Objectif du Camembert
            Le camembert montre la répartition des effectifs des professionnels de santé par spécialité ou par département. 
            Il met en évidence la proportion des effectifs par catégorie sélectionnée, permettant une vue d'ensemble de la distribution.
        """)


    elif st.session_state.visualization_option == "Évolution Annuelle":
        st.markdown("""
            ### Objectif de l'Évolution Annuelle
            Le graphique d'évolution annuelle montre les tendances des effectifs des professionnels de santé au fil des années. 
            Il permet d'identifier les variations annuelles et de comprendre les dynamiques temporelles par région ou par département.
        """)


    elif st.session_state.visualization_option == "Carte Géographique":
        st.markdown("""
            ### Objectif de la Carte Géographique
            La carte géographique permet de visualiser la distribution des effectifs des professionnels de santé par région ou par département. 
            Elle met en évidence les zones avec des effectifs élevés et permet une analyse spatiale des données.
        """)

if __name__ == "__main__":
    load_view()
