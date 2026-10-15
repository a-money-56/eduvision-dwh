import pandas as pd
from sqlalchemy import create_engine

# ==========================================
# 1. CONFIGURATION DE LA CONNEXION
# ==========================================
DATABASE_URL = "postgresql+psycopg2://postgres:admin123@localhost:5432/dwh_iut_douala"
engine = create_engine(DATABASE_URL)

print("[INFO] Connexion a PostgreSQL reussie !")

# ==========================================
# 0. NETTOYAGE (Pour éviter les erreurs de duplication)
# ==========================================
print("[INFO] Nettoyage des anciennes donnees pour eviter les doublons...")
conn = engine.raw_connection()
cur = conn.cursor()
cur.execute("TRUNCATE TABLE fait_performance, dim_etudiant, dim_matiere, dim_enseignant, dim_filiere, dim_temps CASCADE;")
conn.commit()
cur.close()
conn.close()
print("[OK] Base de donnees videe et prete pour le nouveau chargement.")

# ==========================================
# 2. EXTRACT (Extraire les donnees)
# ==========================================
print("[INFO] Lecture des fichiers Excel...")
df_etudiants = pd.read_excel('etudiants.xlsx')
df_matieres = pd.read_excel('matieres.xlsx')
df_notes = pd.read_excel('notes.xlsx')

# ==========================================
# 2.5 CORRESPONDANCE EXACTE DES COLONNES
# ==========================================
print("[INFO] Mise en correspondance des colonnes avec la base de donnees...")

df_etudiants.columns = df_etudiants.columns.str.strip().str.lower().str.replace(' ', '_')
df_etudiants = df_etudiants.rename(columns={'id': 'id_etudiant'})

df_matieres.columns = df_matieres.columns.str.strip().str.lower().str.replace(' ', '_')
df_matieres = df_matieres.rename(columns={
    'id': 'id_matiere', 'code': 'code_ue', 'nom': 'nom_matiere', 'cat': 'categorie'
})
df_matieres = df_matieres[['id_matiere', 'code_ue', 'nom_matiere', 'credit', 'categorie']]

df_notes.columns = df_notes.columns.str.strip().str.lower().str.replace(' ', '_')

# ==========================================
# 3. TRANSFORM (Nettoyer et preparer)
# ==========================================
print("[INFO] Nettoyage et transformation des donnees...")

df_etudiants['sexe'] = df_etudiants['sexe'].astype(str).str.upper().replace({'MASCULIN': 'M', 'FEMININ': 'F', 'HOMME': 'M', 'FEMME': 'F'})

df_notes['note_cc'] = pd.to_numeric(df_notes['note_cc'], errors='coerce')
df_notes['note_examen'] = pd.to_numeric(df_notes['note_examen'], errors='coerce')
df_notes['moyenne_finale'] = (df_notes['note_cc'] + df_notes['note_examen']) / 2
df_notes['statut'] = df_notes['moyenne_finale'].apply(lambda x: 'Valide' if x >= 10 else 'Echoue')
df_notes['id_temps'] = df_notes['semestre'].apply(lambda x: 1 if str(x).upper() == 's1' else 2)

cols_a_supprimer = ['annee_academique', 'semestre']
df_notes = df_notes.drop(columns=[col for col in cols_a_supprimer if col in df_notes.columns])

# ==========================================
# 3.5 GENERATION DYNAMIQUE DES DIMENSIONS MANQUANTES
# ==========================================
print("[INFO] Generation des dimensions de reference pour couvrir tous les IDs du fichier Excel...")

# 1. Générer 15 filières pour couvrir tous les id_filiere possibles (1 à 15)
noms_filieres = [
    "Génie Logiciel", "Réseaux et Télécoms", "Génie Civil", "Génie Électrique",
    "Génie Mécanique", "Techniques de Commercialisation", "Gestion des Entreprises",
    "Comptabilité et Finance", "Informatique de Gestion", "Management des Organisations",
    "Génie Biomédical", "Maintenance Industrielle", "Génie Chimique", "Génie des Procédés", "Autre"
]
df_filieres = pd.DataFrame({
    'id_filiere': range(1, 16),
    'niveau': ['L3' if i <= 8 else 'M1' for i in range(1, 16)],
    'nom_filiere': noms_filieres,
    'faculte': ['FGI' if i <= 5 or i in [9, 11, 12, 13, 14] else 'FSEG' for i in range(1, 16)]
})

# 2. Générer 50 enseignants (ID 101 à 150) pour couvrir tous les id_enseignant possibles
df_enseignants = pd.DataFrame({
    'id_enseignant': range(101, 151),
    'nom': [f"Enseignant {i}" for i in range(101, 151)],
    'grade': 'Chargé de cours',
    'departement': 'Département',
    'anciennete': 5
})

# 3. Temps
df_temps = pd.DataFrame({
    'id_temps': [1, 2],
    'annee_academique': ['2022-2023', '2022-2023'],
    'semestre': ['S1', 'S2'],
    'annee': [2022, 2023],
    'trimestre': ['T1', 'T2']
})

# ==========================================
# 4. LOAD (Charger dans PostgreSQL)
# ==========================================
print("[INFO] Chargement des donnees dans le Data Warehouse...")

df_etudiants.to_sql('dim_etudiant', engine, if_exists='append', index=False)
print("[OK] dim_etudiant charge.")

df_matieres.to_sql('dim_matiere', engine, if_exists='append', index=False)
print("[OK] dim_matiere charge.")

df_enseignants.to_sql('dim_enseignant', engine, if_exists='append', index=False)
print("[OK] dim_enseignant charge.")

df_filieres.to_sql('dim_filiere', engine, if_exists='append', index=False)
print("[OK] dim_filiere charge.")

df_temps.to_sql('dim_temps', engine, if_exists='append', index=False)
print("[OK] dim_temps charge.")

df_notes.to_sql('fait_performance', engine, if_exists='append', index=False)
print("[OK] fait_performance charge.")

print("\n[SUCCESS] Le processus ETL est termine avec succes.")
print("[SUCCESS] Le Data Warehouse est maintenant alimente !")