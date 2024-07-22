import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    dataset = "data/demographie-exercices-liberaux.csv"
    df = pd.read_csv(dataset, sep=';')
    return df

def load_view():
    st.title("Conclusion des Analyses")

    df = load_data()

    # Convertir la colonne 'annee' en entier pour le curseur
    df['annee'] = df['annee'].astype(int)

    # Exclure "France" et "Tout Département" des données
    df = df[df['libelle_region'] != "FRANCE"]
    df = df[df['libelle_departement'] != "Tout département"]

    # Exclure les spécialités contenant "Ensemble"
    df = df[~df['profession_sante'].str.contains("Ensemble", case=False, na=False)]

    # Calculer la densité des effectifs
    # Par région
    regional_summary_df = df.groupby(['libelle_region']).agg({'effectif': 'sum'}).reset_index()
    total_effectif = regional_summary_df['effectif'].sum()
    regional_summary_df['densite'] = (regional_summary_df['effectif'] / total_effectif) * 100

    # Par département
    departmental_summary_df = df.groupby(['libelle_departement']).agg({'effectif': 'sum'}).reset_index()
    departmental_summary_df['densite'] = (departmental_summary_df['effectif'] / total_effectif) * 100

    # Par spécialité
    specialite_summary_df = df.groupby(['profession_sante']).agg({'effectif': 'sum'}).reset_index()
    specialite_summary_df['densite'] = (specialite_summary_df['effectif'] / total_effectif) * 100

    # Synthèse des données
    st.subheader("Synthèse des Données")
    total_effectif = df['effectif'].sum()
    unique_professions = df['profession_sante'].nunique()
    unique_departements = df['libelle_departement'].nunique()
    unique_regions = df['libelle_region'].nunique()

    st.write(f"**Total Effectif :** {total_effectif}")
    st.write(f"**Nombre de spécialités :** {unique_professions}")
    st.write(f"**Nombre de départements :** {unique_departements}")
    st.write(f"**Nombre de régions :** {unique_regions}")

    # Répartition par région
    st.subheader("Répartition des Effectifs par Région")
    fig_region = px.bar(regional_summary_df, x='libelle_region', y='effectif',
                        title='Répartition des Effectifs par Région',
                        labels={'libelle_region': 'Région', 'effectif': 'Effectif'})
    st.plotly_chart(fig_region)

    # Répartition par département
    st.subheader("Répartition des Effectifs par Département")
    fig_dept = px.bar(departmental_summary_df, x='libelle_departement', y='effectif',
                      title='Répartition des Effectifs par Département',
                      labels={'libelle_departement': 'Département', 'effectif': 'Effectif'})
    st.plotly_chart(fig_dept)

    # Répartition par spécialité
    st.subheader("Analyse par Spécialité")
    fig_specialite = px.pie(specialite_summary_df, names='profession_sante', values='effectif',
                            title='Répartition des Effectifs par Spécialité')
    st.plotly_chart(fig_specialite)

    # Analyse des disparités
    st.subheader("Analyse des Disparités")

    # Disparités Régionales
    st.subheader("Disparités Régionales")
    max_region_effectif = regional_summary_df.loc[regional_summary_df['effectif'].idxmax()]
    min_region_effectif = regional_summary_df.loc[regional_summary_df['effectif'].idxmin()]
    max_region_densite = regional_summary_df.loc[regional_summary_df['densite'].idxmax()]
    min_region_densite = regional_summary_df.loc[regional_summary_df['densite'].idxmin()]

    st.write(f"**Région avec le plus grand effectif :** Région {max_region_effectif['libelle_region']} avec {max_region_effectif['effectif']} effectifs.")
    st.write(f"**Région avec le plus petit effectif :** Région {min_region_effectif['libelle_region']} avec {min_region_effectif['effectif']} effectifs.")
    st.write(f"**Région avec la plus haute densité :** Région {max_region_densite['libelle_region']} avec une densité de {max_region_densite['densite']:.2f}%.")
    st.write(f"**Région avec la plus basse densité :** Région {min_region_densite['libelle_region']} avec une densité de {min_region_densite['densite']:.2f}%.")

    # Disparités Départementales
    st.subheader("Disparités Départementales")
    max_dept_effectif = departmental_summary_df.loc[departmental_summary_df['effectif'].idxmax()]
    min_dept_effectif = departmental_summary_df.loc[departmental_summary_df['effectif'].idxmin()]
    max_dept_densite = departmental_summary_df.loc[departmental_summary_df['densite'].idxmax()]
    min_dept_densite = departmental_summary_df.loc[departmental_summary_df['densite'].idxmin()]

    st.write(f"**Département avec le plus grand effectif :** Département {max_dept_effectif['libelle_departement']} avec {max_dept_effectif['effectif']} effectifs.")
    st.write(f"**Département avec le plus petit effectif :** Département {min_dept_effectif['libelle_departement']} avec {min_dept_effectif['effectif']} effectifs.")
    st.write(f"**Département avec la plus haute densité :** Département {max_dept_densite['libelle_departement']} avec une densité de {max_dept_densite['densite']:.2f}%.")
    st.write(f"**Département avec la plus basse densité :** Département {min_dept_densite['libelle_departement']} avec une densité de {min_dept_densite['densite']:.2f}%.")

    # Disparités par Spécialité
    st.subheader("Disparités par Spécialité")
    max_specialite_effectif = specialite_summary_df.loc[specialite_summary_df['effectif'].idxmax()]
    min_specialite_effectif = specialite_summary_df.loc[specialite_summary_df['effectif'].idxmin()]
    max_specialite_densite = specialite_summary_df.loc[specialite_summary_df['densite'].idxmax()]
    min_specialite_densite = specialite_summary_df.loc[specialite_summary_df['densite'].idxmin()]

    st.write(f"**Spécialité avec le plus grand effectif :** Spécialité {max_specialite_effectif['profession_sante']} avec {max_specialite_effectif['effectif']} effectifs.")
    st.write(f"**Spécialité avec le plus petit effectif :** Spécialité {min_specialite_effectif['profession_sante']} avec {min_specialite_effectif['effectif']} effectifs.")
    st.write(f"**Spécialité avec la plus haute densité :** Spécialité {max_specialite_densite['profession_sante']} avec une densité de {max_specialite_densite['densite']:.2f}%.")
    st.write(f"**Spécialité avec la plus basse densité :** Spécialité {min_specialite_densite['profession_sante']} avec une densité de {min_specialite_densite['densite']:.2f}%.")

    st.write("Les disparités observées montrent des variations importantes dans la densité des effectifs entre les régions, départements et spécialités. Une haute densité peut indiquer des zones avec une couverture médicale plus concentrée, tandis qu'une faible densité peut révéler des besoins accrus en matière de services de santé dans certaines zones.")

# Appel de la fonction load_view si ce script est exécuté directement
if __name__ == "__main__":
    load_view()
