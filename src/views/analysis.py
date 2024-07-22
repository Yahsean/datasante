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

    # Convertir la colonne 'annee' en entier pour le curseur
    df['annee'] = df['annee'].astype(int)

    # Sélection de la visualisation via un sous-menu dans la page principale
    visualization_option = st.selectbox(
        "Choisissez la visualisation",
        ["Graphique en barres", "Camembert", "Évolution Annuelle", "Carte Géographique"]
    )

    # Filtrage par colonne 'Année' (sélection unique via curseur)
    years = sorted(df['annee'].unique())
    selected_year = st.slider(
        "Sélectionnez l'année", 
        min_value=min(years), 
        max_value=max(years), 
        value=max(years)  # Valeur par défaut
    )

    # Initialiser les filtres avec des listes vides
    professions = sorted(df['profession_sante'].unique())
    selected_professions = st.multiselect("Sélectionnez les professions", options=professions, default=[])

    regions = sorted(df['libelle_region'].unique())
    selected_regions = st.multiselect("Sélectionnez les régions", options=regions, default=[])

    # Filtrer les départements en fonction des régions sélectionnées
    if selected_regions:
        departements = sorted(df[df['libelle_region'].isin(selected_regions)]['libelle_departement'].unique())
    else:
        departements = []
    selected_departements = st.multiselect("Sélectionnez les départements", options=departements, default=[])

    # Application des filtres
    filtered_df = df[
        (df['annee'] == selected_year) &
        (df['profession_sante'].isin(selected_professions) if selected_professions else True) &
        (df['libelle_region'].isin(selected_regions) if selected_regions else True) &
        (df['libelle_departement'].isin(selected_departements) if selected_departements else True)
    ]

    # Utilisation des colonnes pour organiser le contenu
    col1, col2 = st.columns([2, 1])  # Crée deux colonnes avec une largeur relative de 2:1

    with col1:
        # Affichage en fonction de la sélection du sous-menu
        if visualization_option == "Graphique en barres":
            # Groupement par spécialité et région ou département
            group_by = st.radio("Choisissez la dimension pour le groupement du graphique en barres", ["Région", "Département"], key="bar")

            if group_by == "Région":
                grouped_df = filtered_df.groupby(['profession_sante', 'libelle_region']).agg({'effectif': 'sum'}).reset_index()
                fig = px.bar(grouped_df, x='profession_sante', y='effectif', color='libelle_region',
                             title=f'Effectifs par Spécialité et Région en {selected_year}', labels={'profession_sante': 'Spécialité', 'effectif': 'Effectif'},
                             barmode='group')
            else:
                grouped_df = filtered_df.groupby(['profession_sante', 'libelle_departement']).agg({'effectif': 'sum'}).reset_index()
                fig = px.bar(grouped_df, x='profession_sante', y='effectif', color='libelle_departement',
                             title=f'Effectifs par Spécialité et Département en {selected_year}', labels={'profession_sante': 'Spécialité', 'effectif': 'Effectif'},
                             barmode='group')
            
            st.plotly_chart(fig)

        elif visualization_option == "Camembert":
            # Groupement pour le camembert
            group_by = st.radio("Choisissez la dimension pour le groupement du camembert", ["Région", "Département"], key="pie")

            if group_by == "Région":
                camembert_df = filtered_df.groupby('profession_sante').agg({'effectif': 'sum'}).reset_index()
                fig = px.pie(camembert_df, names='profession_sante', values='effectif',
                             title=f'Répartition des Effectifs par Spécialité en {selected_year}')
            else:
                camembert_df = filtered_df.groupby('libelle_departement').agg({'effectif': 'sum'}).reset_index()
                fig = px.pie(camembert_df, names='libelle_departement', values='effectif',
                             title=f'Répartition des Effectifs par Département en {selected_year}')
            
            st.plotly_chart(fig)

        elif visualization_option == "Évolution Annuelle":
            # Filtrage pour l'évolution annuelle
            evolution_professions = sorted(df['profession_sante'].unique())
            selected_evolution_profession = st.selectbox("Sélectionnez la spécialité", options=evolution_professions, index=0)

            # Groupement et affichage de l'évolution annuelle
            evolution_by_region_dept = st.radio("Choisissez la dimension pour l'évolution annuelle", ["Région", "Département"], key="evolution")

            if evolution_by_region_dept == "Région":
                evolution_df = df[df['profession_sante'] == selected_evolution_profession]
                evolution_df = evolution_df.groupby(['annee', 'libelle_region']).agg({'effectif': 'sum'}).reset_index()
                fig = px.line(evolution_df, x='annee', y='effectif', color='libelle_region',
                              title=f'Évolution Annuelle des Effectifs pour {selected_evolution_profession} par Région', labels={'annee': 'Année', 'effectif': 'Effectif'})
            else:
                evolution_df = df[df['profession_sante'] == selected_evolution_profession]
                evolution_df = evolution_df.groupby(['annee', 'libelle_departement']).agg({'effectif': 'sum'}).reset_index()
                fig = px.line(evolution_df, x='annee', y='effectif', color='libelle_departement',
                              title=f'Évolution Annuelle des Effectifs pour {selected_evolution_profession} par Département', labels={'annee': 'Année', 'effectif': 'Effectif'})
            
            st.plotly_chart(fig)

        elif visualization_option == "Carte Géographique":
            # Sous-menu pour choisir le type de carte
            map_view = st.selectbox("Choisissez le type de carte", ["Carte des Régions", "Carte des Départements"])

            if map_view == "Carte des Régions":
                # Groupement par région pour obtenir les valeurs
                grouped_df = filtered_df.groupby(['libelle_region']).agg({'effectif': 'sum'}).reset_index()

                # Définir une plage de couleurs réduite pour les régions
                max_effectif = grouped_df['effectif'].max()
                min_effectif = grouped_df['effectif'].quantile(0.05)  # 5e percentile pour éviter les valeurs extrêmes
                range_effectif = (min_effectif, max_effectif)
                
                # Créer une carte choroplèthe pour les régions
                fig = px.choropleth_mapbox(
                    grouped_df,
                    geojson=regions_geojson,
                    locations='libelle_region',
                    featureidkey="properties.nom",  # Clé pour les régions dans GeoJSON
                    color='effectif',
                    color_continuous_scale="Viridis",  # Échelle de couleur plus nuancée
                    range_color=range_effectif,
                    title=f'Effectifs de {", ".join(selected_professions) if selected_professions else "toutes les spécialités"} par Région en {selected_year}',
                    center={"lat": 46.603354, "lon": 1.888334},  # Centre approximatif de la France
                    mapbox_style="carto-positron",
                    labels={'effectif': 'Effectif'},
                    zoom=5
                )

                # Afficher la carte des régions
                st.plotly_chart(fig, use_container_width=True)

                # Sélectionner une région pour voir les départements
                selected_region = st.selectbox("Sélectionnez une région pour voir les départements", options=grouped_df['libelle_region'].tolist())

                if selected_region:
                    # Filtrer les départements pour la région sélectionnée
                    departements_filtered_df = filtered_df[filtered_df['libelle_region'] == selected_region]
                    departements_grouped_df = departements_filtered_df.groupby(['libelle_departement']).agg({'effectif': 'sum'}).reset_index()
                    
                    # Créer une carte choroplèthe pour les départements
                    fig_departements = px.choropleth_mapbox(
                        departements_grouped_df,
                        geojson=departements_geojson,
                        locations='libelle_departement',
                        featureidkey="properties.nom",  # Clé pour les départements dans GeoJSON
                        color='effectif',
                        color_continuous_scale="Viridis",  # Échelle de couleur plus nuancée
                        range_color=range_effectif,
                        title=f'Effectifs de {", ".join(selected_professions) if selected_professions else "toutes les spécialités"} par Département en {selected_year} (Région: {selected_region})',
                        center={"lat": 46.603354, "lon": 1.888334},  # Centre approximatif de la France
                        mapbox_style="carto-positron",
                        labels={'effectif': 'Effectif'},
                        zoom=6
                    )
                    
                    st.plotly_chart(fig_departements, use_container_width=True)
            
            elif map_view == "Carte des Départements":
                # Ajouter l'option "Tout Département" dans la liste déroulante
                departements_options = ["Tout Département"] + sorted(df['libelle_departement'].unique())
                selected_departements = st.multiselect(
                    "Sélectionnez les départements", 
                    options=departements_options, 
                    default=["Tout Département"]
                )

                # Appliquer le filtre pour les départements
                if "Tout Département" in selected_departements:
                    filtered_departements_df = filtered_df
                else:
                    filtered_departements_df = filtered_df[
                        (filtered_df['libelle_departement'].isin(selected_departements))
                    ]

                # Groupement par département pour obtenir les valeurs
                grouped_df = filtered_departements_df.groupby(['libelle_departement']).agg({'effectif': 'sum'}).reset_index()

                # Définir une plage de couleurs réduite pour les départements
                max_effectif = grouped_df['effectif'].max()
                min_effectif = grouped_df['effectif'].quantile(0.05)  # 5e percentile pour éviter les valeurs extrêmes
                range_effectif = (min_effectif, max_effectif)
                
                # Créer une carte choroplèthe pour les départements
                fig = px.choropleth_mapbox(
                    grouped_df,
                    geojson=departements_geojson,
                    locations='libelle_departement',
                    featureidkey="properties.nom",  # Clé pour les départements dans GeoJSON
                    color='effectif',
                    color_continuous_scale="Viridis",  # Échelle de couleur plus nuancée
                    range_color=range_effectif,
                    title=f'Effectifs de {", ".join(selected_professions) if selected_professions else "toutes les spécialités"} par Département en {selected_year}',
                    center={"lat": 46.603354, "lon": 1.888334},  # Centre approximatif de la France
                    mapbox_style="carto-positron",
                    labels={'effectif': 'Effectif'},
                    zoom=6
                )

                st.plotly_chart(fig, use_container_width=True)

# Appel de la fonction load_view si ce script est exécuté directement
if __name__ == "__main__":
    load_view()
