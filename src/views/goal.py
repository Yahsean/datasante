import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt





def load_view():    
    st.title("Objectif du projet Fil Rouge")
    st.header("Introduction - Description du projet : \n Les données présentées ici sont produites à partir des fichiers statistiques construits chaque année par la DREES à partir du Répertoire partagé des professionnels de santé (RPPS) et du répertoire Adeli. Elles décrivent les professionnels qui sont actifs occupés au 1er janvier. ")
    with st.expander("Professions concernées par le RPPS"):
        st.markdown("""
### Professions concernées par le RPPS :

- les médecins
- les chirurgiens-dentistes
- les pharmaciens
- les sages-femmes
- les masseurs-kinésithérapeutes (à partir de 2017)
- les pédicures-podologues (à partir de 2018)
""")                    
    with st.expander("Professions concernées par le répertoire Adeli"):
        st.markdown("""

### Professions concernées par le répertoire Adeli :

- les audioprothésistes
- les diététiciens
- les ergothérapeutes
- les infirmiers (jusqu’en 2021)
- les manipulateurs ERM
- les masseur-kinésithérapeutes (jusqu’en 2016)
- les opticiens-lunetiers
- les orthophonistes
- les orthoptistes
- les pédicure-podologues (jusqu’en 2017)
- les professionnels de l’appareillage
- les psychologues
- les psychomotriciens
- les techniciens de laboratoire
""")
    st.title("Description des 10 premières lignes de notre dataframe")
    dataset = "data/demographie-exercices-liberaux.csv"
    df = pd.read_csv(dataset, sep=';')
    df['annee'] = df['annee'].astype(str)
    
    st.write(df.head())
    #st.write(df.isnull().sum())


    # Extraire et trier les valeurs uniques de la colonne 'profession_sante'
    unique_professions = sorted(df['profession_sante'].unique())

    # Créer un DataFrame avec les valeurs uniques organisées en deux colonnes
    num_cols = 2
    num_professions = len(unique_professions)
    num_rows = (num_professions + num_cols - 1) // num_cols  # Calculer le nombre de lignes nécessaires

    # Créer les colonnes pour le DataFrame
    columns = [f'Colonne {i+1}' for i in range(num_cols)]
    data = {col: [] for col in columns}

    # Remplir les colonnes avec les valeurs uniques
    for i in range(num_rows):
        for j in range(num_cols):
            index = i + j * num_rows
            if index < num_professions:
                data[columns[j]].append(unique_professions[index])
            else:
                data[columns[j]].append('')

    # Convertir le dictionnaire en DataFrame
    df_unique_professions = pd.DataFrame(data)
    st.title("Les differentes professions ou groupements de professions du DataSet (triées par ordre alphabétique) :")
    st.table(df_unique_professions)


