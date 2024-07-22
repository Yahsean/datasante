import pandas as pd
import streamlit as st

def load_view():
    st.title("Présentation des données et tableaux de visualisation")
    
    # Chargement des données 
    dataset = "data/demographie-exercices-liberaux.csv"
    df = pd.read_csv(dataset, sep=';')
    df['annee'] = df['annee'].astype(str)
    
    # Afficher les informations sur les colonnes
    st.write("Listing des données du DataSet et le type de colonnes :")
    columns_info = pd.DataFrame({
        'Nom de Colonne': df.columns,
        'Type de Donnée': df.dtypes
    })
    st.write(columns_info)

    # Afficher le DataFrame après conversion
    st.write("DataFrame après conversion de la colonne 'annee' :")
    st.write(df.head())

    # Définir les nouveaux noms de colonnes
    column_rename_map = {
        'annee': 'Année',
        'profession_sante': 'Profession de Santé',
        'libelle_region': 'Région',
        'departement': 'Département',
        'libelle_departement': 'Libellé du Département',
        'libelle_type_exercice_liberal': 'Type d\'Exercice Libéral',
        'effectif': 'Effectif'
    }

    # Vérifier si toutes les colonnes à renommer existent dans le DataFrame
    missing_columns = [col for col in column_rename_map.keys() if col not in df.columns]
    if missing_columns:
        st.error(f"Les colonnes suivantes sont manquantes dans les données : {', '.join(missing_columns)}")
    else:
        # Sélectionner les colonnes spécifiques
        columns_to_display = list(column_rename_map.keys())

        # Filtrage par colonne 'Année'
        years = df['annee'].unique()
        selected_years = st.multiselect("Sélectionnez l'année", options=years, default=years)

        # Filtrage par colonne 'Profession'
        professions = df['profession_sante'].unique()
        selected_professions = st.multiselect("Sélectionnez les professions", options=professions, default=professions)

        # Filtrage par colonne 'Région'
        regions = df['libelle_region'].unique()
        selected_regions = st.multiselect("Sélectionnez les régions", options=regions, default=regions)

        # Filtrage par colonne 'Département'
        departements = df['libelle_departement'].unique()
        selected_departements = st.multiselect("Sélectionnez les départements", options=departements, default=departements)

        # Filtrage par colonne 'Type d'Exercice'
        types_exercice = df['libelle_type_exercice_liberal'].unique()
        selected_types_exercice = st.multiselect("Sélectionnez les types d'exercice", options=types_exercice, default=types_exercice)

        # Application des filtres
        filtered_df = df[
            (df['annee'].isin(selected_years)) &
            (df['profession_sante'].isin(selected_professions)) &
            (df['libelle_region'].isin(selected_regions)) &
            (df['libelle_departement'].isin(selected_departements)) &
            (df['libelle_type_exercice_liberal'].isin(selected_types_exercice))
        ]

        # Affichage du tableau filtré
        st.write("### Tableau Filtré")
        st.dataframe(filtered_df)

        # Extraire les colonnes spécifiques
        df_filtered = df[columns_to_display]

        # Renommer les colonnes pour l'affichage
        df_filtered_renamed = df_filtered.rename(columns=column_rename_map)

        # Afficher le DataFrame avec les colonnes renommées
        st.write("Données avec les colonnes renommées :")
        st.dataframe(df_filtered_renamed)

