import streamlit as st
import pandas as pd
import geopandas as gpd

@st.cache_data
def data_load() : 
    prod = pd.read_csv("data/volume_vin 2009-2010.csv", encoding='iso-8859-1', sep = ";")
    prod['TOTAL'] = prod['TOTAL'].str.replace(' ', '').astype(float)
    prod = prod.fillna(-1)

    colonnes_a_exclure = ['code_dep', 'nom_dep']
    for col in prod.columns:
        if col not in colonnes_a_exclure and prod[col].dtype == 'object':
            prod[col] = prod[col].str.replace(' ', '')

    prod['Total AOP'] = prod['AOP Blanc'] + prod['AOP Rouge/Rose']
    prod['Total IGP'] = prod['IGP Blanc'] + prod['IGP Rouge/Rose']
    prod['Total VSIG'] = prod['VSIG Blanc'] + prod['VSIG Rouge/Rose']
    st.write(prod.head(30))
    
    return prod

@st.cache_data
def géo_load():
    departements = gpd.read_file("data/departements.geojson")
    return departements

@st.cache_data
def data_true ():
    df = pd.read_excel(
        "https://www.data.gouv.fr/fr/datasets/r/c0f9337b-3bda-45fa-ad31-c3dfa8a1cce8", 
        skiprows=21, 
        header=None, 
        names=["num&nom_dep",
               "nombre de déclarations", 
               "superficie totale",
               "superficie AOP",
               "superficie VDQS",
               "superficie Cognac",
               "superficie autre",
               "qte AOC blanc",
               "qte AOC rouge/rose",
               "qte VDQS blanc",
               "qte VDQS rouge/rose",
               "qte Cognac",
               "qte VDP blanc",
               "qte VDP rouge/rose",
               "qte autre blanc",
               "qte autre rouge/rose",
               "qte totale blanc",
               "qte totale rouge/rose",
               "TOTAL",
               ])
    
    df.at[len(df) - 1, 'num&nom_dep'] = "00 Total"
    df['num&nom_dep'] = df['num&nom_dep'].astype(str)
    df['code_dep'] = df['num&nom_dep'].apply(lambda x: x[:2])
    # df['code_dep'] = df['code_dep'].str.replace('O', '0')
    df = df.drop([96,97])
    df = df.reset_index(drop=True)
    
    df['TOTAL'] = df['TOTAL'].replace(' ', '').astype(float)
    colonnes_a_exclure = ['num&nom_dep']
    for col in df.columns:
        if col not in colonnes_a_exclure and df[col].dtype == 'object':
            df[col] = df[col].replace(' ', '')
    
    df['Total AOC'] = df['qte AOC blanc'] + df['qte AOC rouge/rose']
    df['Total VDQS'] = df['qte VDQS blanc'] + df['qte VDQS rouge/rose']
    df['Total autre'] = df['qte autre blanc'] + df['qte autre rouge/rose']
    df['Total VDP'] = df ['qte VDP blanc'] + df['qte VDP rouge/rose']
    df = df.fillna(0)

    return df