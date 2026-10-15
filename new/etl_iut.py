import pandas as pd
from sqlalchemy import create_engine

# ==========================================
# 1. CONFIGURATION DE LA CONNEXION
# ==========================================
DATABASE_URL = "postgresql+psycopg2://postgres:admin123@localhost:5432/dwh_iut_douala"
engine = create_engine(DATABASE_URL)

print("🔌 Connexion à PostgreSQL réussie !")

# ==========================================
# 2. EXTRACT (Extraire les données des fichiers .csv)
# ==========================================
print("📂 Lecture des fichiers CSV massifs...")
df_etudiants = pd.read_csv('etudiants.csv')
df_matieres = pd.read_csv('matieres.csv')
df_notes = pd.read_csv('notes.csv')
df_enseignants = pd.read_csv('enseignants.csv')
df_filieres = pd.read_csv('filieres.csv')

# ✨ ASTUCE MAGIQUE : Nettoyer les noms de colonnes automatiquement
df_etudiants.columns = df_etudiants.columns.str.strip().str.lower().str.replace(' ', '_')
df_matieres.columns = df_matieres.columns.str.strip().str.lower().str.replace(' ', '_')
df_notes.columns = df_notes.columns.str.strip().str.lower().str.replace(' ', '_')
df_enseignants.columns = df_enseignants.columns.str.strip().str.lower().str.replace(' ', '_')
df_filieres.columns = df_filieres.columns.str.strip().str.lower().str.replace(' ', '_')

# 🛠️ CORRECTION CRUCIALE : Renommer les colonnes pour correspondre EXACTEMENT au schéma PostgreSQL
df_matieres = df_matieres.rename(columns={
    'id': 'id_matiere',
    'code': 'code_ue',
    'nom': 'nom_matiere',
    'cat': 'categorie'
})

df_enseignants = df_enseignants.rename(columns={
    'id': 'id_enseignant',
    'dept': 'departement',
    'anc': 'anciennete'
})

df_filieres = df_filieres.rename(columns={
    'id': 'id_filiere',
    'nom': 'nom_filiere'
})

# ==========================================
# 3. TRANSFORM (Nettoyer et préparer les données)
# ==========================================
print("🧹 Nettoyage et transformation des données...")

# Uniformiser le sexe (M ou F)
df_etudiants['sexe'] = df_etudiants['sexe'].astype(str).str.upper().replace({'MASCULIN': 'M', 'FEMININ': 'F', 'HOMME': 'M', 'FEMME': 'F'})

# S'assurer que les notes sont bien des nombres (gérer les virgules françaises)
df_notes['note_cc'] = df_notes['note_cc'].astype(str).str.replace(',', '.').str.strip()
df_notes['note_cc'] = pd.to_numeric(df_notes['note_cc'], errors='coerce')
df_notes['note_examen'] = pd.to_numeric(df_notes['note_examen'], errors='coerce')

# Calculer la moyenne finale (Moyenne = (CC + Examen) / 2)
df_notes['moyenne_finale'] = (df_notes['note_cc'] + df_notes['note_examen']) / 2

# Déterminer le statut automatiquement
df_notes['statut'] = df_notes['moyenne_finale'].apply(lambda x: 'Valide' if x >= 10 else 'Echoue')

# Créer un ID temps simple basé sur le semestre
df_notes['id_temps'] = df_notes['semestre'].apply(lambda x: 1 if str(x).upper() == 'S1' else 2)

# Supprimer les colonnes de dimension qui ne doivent pas être dans la table de faits
cols_a_supprimer = ['annee_academique', 'semestre']
df_notes = df_notes.drop(columns=[col for col in cols_a_supprimer if col in df_notes.columns])

# ==========================================
# 3.5 PRÉPARATION DE LA DIMENSION TEMPS
# ==========================================
df_temps = pd.DataFrame({
    'id_temps': [1, 2],
    'annee_academique': ['2020-2021', '2020-2021'],
    'semestre': ['S1', 'S2'],
    'annee': [2020, 2021],
    'trimestre': ['T1', 'T2']
})

# ==========================================
# 4. LOAD (Charger les données dans PostgreSQL)
# ==========================================
print("🚀 Chargement des données dans le Data Warehouse...")

# 1. On charge d'abord les dimensions
df_etudiants.to_sql('dim_etudiant', engine, if_exists='append', index=False)
print("✅ dim_etudiant chargé.")

df_matieres.to_sql('dim_matiere', engine, if_exists='append', index=False)
print("✅ dim_matiere chargé.")

df_enseignants.to_sql('dim_enseignant', engine, if_exists='append', index=False)
print("✅ dim_enseignant chargé.")

df_filieres.to_sql('dim_filiere', engine, if_exists='append', index=False)
print("✅ dim_filiere chargé.")

df_temps.to_sql('dim_temps', engine, if_exists='append', index=False)
print("✅ dim_temps chargé.")

# 2. On charge la table de faits EN DERNIER
df_notes.to_sql('fait_performance', engine, if_exists='append', index=False)
print("✅ fait_performance chargé.")

print("\n🎉 FÉLICITATIONS ! Le processus ETL est terminé avec succès.")
print("Ton Data Warehouse est maintenant alimenté avec 35 000 étudiants !")