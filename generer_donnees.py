import pandas as pd
import random
import numpy as np

# ==========================================
# CONFIGURATION DU GÉNÉRATEUR DE DONNÉES MASSIVES
# ==========================================
NB_ETUDIANTS = 3000
ANNEES_ACADEMIQUES = ['2020-2021', '2021-2022', '2022-2023', '2023-2024']
SEMESTRES = ['S1', 'S2']

# Données réalistes pour l'IUT de Douala
PRENOMS_M = ['Jean', 'Paul', 'Marc', 'David', 'Eric', 'Samuel', 'Patrick', 'Yves', 'Roger', 'Alain', 'Pierre', 'Joseph', 'Emmanuel', 'Serge', 'Christian']
PRENOMS_F = ['Marie', 'Amina', 'Sarah', 'Léa', 'Esther', 'Blandine', 'Carine', 'Viviane', 'Christelle', 'Audrey', 'Nathalie', 'Brigitte', 'Sandrine', 'Claudine', 'Hélène']
NOMS = ['NGUEMA', 'MBALLA', 'TCHOUA', 'FOFACK', 'KAMGA', 'BIYA', 'NDONGO', 'ESSOMBA', 'TSOATA', 'MBOUOP', 'KWETCHE', 'NJOMO', 'DONGMO', 'FEUDJIO', 'TATCHO', 'NGONO', 'ABEGA', 'BELINGA', 'EKOBO', 'MEKA']
REGIONS = ['Littoral', 'Centre', 'Ouest', 'Nord-Ouest', 'Sud', 'Sud-Ouest', 'Est', 'Adamaoua', 'Nord', 'Extrême-Nord']
TYPES_BAC = ['BAC A', 'BAC C', 'BAC D', 'BAC E', 'BAC F', 'BAC G2']
STATUTS_BOURSE = ['Oui', 'Non']
STATUTS_PAIEMENT = ['A jour', 'En retard', 'Exonéré']

FILIERES = [
    {'id': 1, 'niveau': 'L1', 'nom': 'Génie Logiciel', 'faculte': 'FGI'},
    {'id': 2, 'niveau': 'L2', 'nom': 'Génie Logiciel', 'faculte': 'FGI'},
    {'id': 3, 'niveau': 'L3', 'nom': 'Génie Logiciel', 'faculte': 'FGI'},
    {'id': 4, 'niveau': 'M1', 'nom': 'Génie Logiciel', 'faculte': 'FGI'},
    {'id': 5, 'niveau': 'L1', 'nom': 'Réseaux et Télécoms', 'faculte': 'FGI'},
    {'id': 6, 'niveau': 'L2', 'nom': 'Réseaux et Télécoms', 'faculte': 'FGI'},
    {'id': 7, 'niveau': 'L3', 'nom': 'Réseaux et Télécoms', 'faculte': 'FGI'},
    {'id': 8, 'niveau': 'M1', 'nom': 'Réseaux et Télécoms', 'faculte': 'FGI'},
    {'id': 9, 'niveau': 'L1', 'nom': 'Génie Civil', 'faculte': 'FGI'},
    {'id': 10, 'niveau': 'L2', 'nom': 'Génie Civil', 'faculte': 'FGI'},
    {'id': 11, 'niveau': 'L3', 'nom': 'Génie Civil', 'faculte': 'FGI'},
    {'id': 12, 'niveau': 'M1', 'nom': 'Génie Civil', 'faculte': 'FGI'},
]

MATIERES = [
    {'id': 1, 'code': 'INF101', 'nom': 'Algorithmique', 'credit': 4, 'cat': 'Fondamentale'},
    {'id': 2, 'code': 'INF201', 'nom': 'Base de données', 'credit': 6, 'cat': 'Fondamentale'},
    {'id': 3, 'code': 'INF301', 'nom': 'Programmation Web', 'credit': 4, 'cat': 'Fondamentale'},
    {'id': 4, 'code': 'MTH101', 'nom': 'Mathématiques I', 'credit': 4, 'cat': 'Fondamentale'},
    {'id': 5, 'code': 'MTH201', 'nom': 'Statistiques', 'credit': 3, 'cat': 'Fondamentale'},
    {'id': 6, 'code': 'UO101', 'nom': 'Anglais Technique', 'credit': 2, 'cat': 'Transversale'},
    {'id': 7, 'code': 'UO102', 'nom': 'Communication', 'credit': 2, 'cat': 'Transversale'},
    {'id': 8, 'code': 'RT101', 'nom': 'Réseaux Locaux', 'credit': 5, 'cat': 'Fondamentale'},
    {'id': 9, 'code': 'GC101', 'nom': 'Résistance des Matériaux', 'credit': 5, 'cat': 'Fondamentale'},
    {'id': 10, 'code': 'GL401', 'nom': 'Génie Logiciel Avancé', 'credit': 5, 'cat': 'Fondamentale'},
]

ENSEIGNANTS = [
    {'id': 101, 'nom': 'Prof. TCHINDA', 'grade': 'Maître de Conférences', 'dept': 'Informatique', 'anc': 15},
    {'id': 102, 'nom': 'Dr. MBARGA', 'grade': 'Chargé de Cours', 'dept': 'Informatique', 'anc': 8},
    {'id': 103, 'nom': 'Prof. KEMAJOU', 'grade': 'Professeur', 'dept': 'Mathématiques', 'anc': 20},
    {'id': 104, 'nom': 'Dr. NGUENANG', 'grade': 'Maître Assistant', 'dept': 'Informatique', 'anc': 5},
    {'id': 105, 'nom': 'M. FONKAM', 'grade': 'Vacataire', 'dept': 'Langues', 'anc': 3},
    {'id': 106, 'nom': 'Dr. WAMBA', 'grade': 'Chargé de Cours', 'dept': 'Réseaux', 'anc': 7},
    {'id': 107, 'nom': 'Prof. DJONDE', 'grade': 'Maître de Conférences', 'dept': 'Génie Civil', 'anc': 12},
    {'id': 108, 'nom': 'M. TEMGOUA', 'grade': 'Assistant', 'dept': 'Informatique', 'anc': 2},
]

print("🏭 Génération de données massives pour l'IUT de Douala...")

# ==========================================
# 1. GÉNÉRATION DES ÉTUDIANTS
# ==========================================
etudiants = []
for i in range(1, NB_ETUDIANTS + 1):
    sexe = random.choice(['M', 'F'])
    prenom = random.choice(PRENOMS_M if sexe == 'M' else PRENOMS_F)
    nom = random.choice(NOMS)
    
    # Ajout volontaire de "données sales" pour tester l'ETL
    if random.random() < 0.05:  # 5% de chance d'avoir un format bizarre
        sexe_raw = random.choice(['MASCULIN', 'HOMME', 'feminin', 'Femme'])
    else:
        sexe_raw = sexe
        
    etudiants.append({
        'id_etudiant': i,
        'matricule': f"{random.randint(2020, 2023)}{i:04d}",
        'nom': nom,
        'prenom': prenom,
        'sexe': sexe_raw,  # Données sales volontaires
        'age': random.randint(18, 28),
        'region_origine': random.choice(REGIONS),
        'type_bac': random.choice(TYPES_BAC),
        'statut_bourse': random.choice(STATUTS_BOURSE),
        'statut_paiement': random.choice(STATUTS_PAIEMENT)
    })

df_etudiants = pd.DataFrame(etudiants)
df_etudiants.to_excel('etudiants.xlsx', index=False)
print(f"✅ {len(df_etudiants)} étudiants générés.")

# ==========================================
# 2. GÉNÉRATION DES MATIÈRES ET ENSEIGNANTS (Fixes)
# ==========================================
df_matieres = pd.DataFrame(MATIERES)
df_matieres.to_excel('matieres.xlsx', index=False)
print(f"✅ {len(df_matieres)} matières générées.")

df_enseignants = pd.DataFrame(ENSEIGNANTS)
# On ne sauvegarde pas les enseignants en Excel car ils sont fixes dans le script ETL,
# mais on les garde ici pour référence.

# ==========================================
# 3. GÉNÉRATION DES NOTES (TABLE DE FAITS MASSIVE)
# ==========================================
notes = []
id_perf = 1

# Chaque étudiant a ~5 matières par semestre sur 4 ans
for etud in etudiants:
    nb_annees = random.randint(2, 4)  # Certains abandonnent ou redoublent
    annees_jouees = random.sample(ANNEES_ACADEMIQUES, nb_annees)
    
    for annee in annees_jouees:
        for sem in SEMESTRES:
            # Nombre variable de matières selon le semestre
            nb_matieres = random.randint(4, 7)
            matieres_sem = random.sample(MATIERES, min(nb_matieres, len(MATIERES)))
            
            for mat in matieres_sem:
                ens = random.choice(ENSEIGNANTS)
                fil = random.choice(FILIERES)
                
                # Simulation réaliste des notes (loi normale autour de 10/20)
                note_cc = round(np.random.normal(9, 3), 1)
                note_ex = round(np.random.normal(10, 3.5), 1)
                
                # Bornes réalistes [0, 20]
                note_cc = max(0, min(20, note_cc))
                note_ex = max(0, min(20, note_ex))
                
                moy = round((note_cc + note_ex) / 2, 1)
                credits = mat['credit'] if moy >= 10 else 0
                absences = int(np.random.exponential(3))  # Distribution exponentielle pour les absences
                
                # Statut basé sur la moyenne
                statut = 'Valide' if moy >= 10 else 'Echoue'
                
                # Ajout volontaire de données sales dans les notes
                if random.random() < 0.02:  # 2% de chances
                    note_cc_str = str(note_cc).replace('.', ',')  # Virgule au lieu de point
                else:
                    note_cc_str = note_cc
                    
                notes.append({
                    'id_etudiant': etud['id_etudiant'],
                    'id_matiere': mat['id'],
                    'id_enseignant': ens['id'],
                    'id_filiere': fil['id'],
                    'annee_academique': annee,
                    'semestre': sem,
                    'note_cc': note_cc_str,  # Donnée sale potentielle
                    'note_examen': note_ex,
                    'moyenne_finale': '',  # Sera calculé par l'ETL
                    'credits_obtenus': credits,
                    'heures_absence': absences,
                    'statut': ''  # Sera calculé par l'ETL
                })
                id_perf += 1

df_notes = pd.DataFrame(notes)
df_notes.to_excel('notes.xlsx', index=False)
print(f"✅ {len(df_notes)} lignes de notes générées (Table de Faits).")

print("\n DONNÉES MASSIVES GÉNÉRÉES AVEC SUCCÈS !")
print(f"   - Étudiants : {len(df_etudiants)}")
print(f"   - Matières : {len(df_matieres)}")
print(f"   - Notes (Faits) : {len(df_notes)}")
print("   - Données 'sales' incluses pour tester la robustesse de l'ETL.")