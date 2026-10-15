import pandas as pd
import numpy as np
import random
import time

print("🏭 LANCEMENT DE LA GÉNÉRATION MASSIVE (35 000 ÉTUDIANTS)...")
start_time = time.time()

# --- CONFIGURATION ---
NB_ETUDIANTS = 35000
ANNEES = ['2020-2021', '2021-2022', '2022-2023', '2023-2024']
SEMESTRES = ['S1', 'S2']

# --- DONNÉES RÉALISTES IUT DOUALA ---
PRENOMS_M = ['Jean', 'Paul', 'Marc', 'David', 'Eric', 'Samuel', 'Patrick', 'Yves', 'Roger', 'Alain', 'Pierre', 'Joseph', 'Emmanuel', 'Serge', 'Christian', 'Armel', 'Boris', 'Kevin']
PRENOMS_F = ['Marie', 'Amina', 'Sarah', 'Léa', 'Esther', 'Blandine', 'Carine', 'Viviane', 'Christelle', 'Audrey', 'Nathalie', 'Brigitte', 'Sandrine', 'Claudine', 'Hélène', 'Aïcha', 'Bérénice', 'Diane']
NOMS = ['NGUEMA', 'MBALLA', 'TCHOUA', 'FOFACK', 'KAMGA', 'BIYA', 'NDONGO', 'ESSOMBA', 'TSOATA', 'MBOUOP', 'KWETCHE', 'NJOMO', 'DONGMO', 'FEUDJIO', 'TATCHO', 'NGONO', 'ABEGA', 'BELINGA', 'EKOBO', 'MEKA', 'ATANGANA', 'OWONA', 'ZOA', 'EYINGA']
REGIONS = ['Littoral', 'Centre', 'Ouest', 'Nord-Ouest', 'Sud', 'Sud-Ouest', 'Est', 'Adamaoua', 'Nord', 'Extrême-Nord']
TYPES_BAC = ['BAC A', 'BAC C', 'BAC D', 'BAC E', 'BAC F', 'BAC G2', 'BAC TI']

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
    {'id': 13, 'niveau': 'L1', 'nom': 'Génie Électrique', 'faculte': 'FGI'},
    {'id': 14, 'niveau': 'L2', 'nom': 'Génie Électrique', 'faculte': 'FGI'},
    {'id': 15, 'niveau': 'L3', 'nom': 'Génie Électrique', 'faculte': 'FGI'},
    {'id': 16, 'niveau': 'M1', 'nom': 'Génie Électrique', 'faculte': 'FGI'},
    {'id': 17, 'niveau': 'L1', 'nom': 'Techniques de Commercialisation', 'faculte': 'FGSE'},
    {'id': 18, 'niveau': 'L2', 'nom': 'Techniques de Commercialisation', 'faculte': 'FGSE'},
    {'id': 19, 'niveau': 'L3', 'nom': 'Techniques de Commercialisation', 'faculte': 'FGSE'},
    {'id': 20, 'niveau': 'M1', 'nom': 'Techniques de Commercialisation', 'faculte': 'FGSE'},
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
    {'id': 11, 'code': 'GE101', 'nom': 'Électrotechnique', 'credit': 5, 'cat': 'Fondamentale'},
    {'id': 12, 'code': 'TC101', 'nom': 'Marketing Fondamental', 'credit': 4, 'cat': 'Fondamentale'},
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
    {'id': 109, 'nom': 'Dr. KAMDEM', 'grade': 'Maître Assistant', 'dept': 'Génie Électrique', 'anc': 6},
    {'id': 110, 'nom': 'Prof. NOAH', 'grade': 'Professeur', 'dept': 'Commerce', 'anc': 18},
]

# --- 1. GÉNÉRATION DES ÉTUDIANTS ---
print("👥 Génération de 35 000 étudiants...")
etudiants = []
for i in range(1, NB_ETUDIANTS + 1):
    sexe = random.choice(['M', 'F'])
    prenom = random.choice(PRENOMS_M if sexe == 'M' else PRENOMS_F)
    nom = random.choice(NOMS)
    
    # Données "sales" volontaires (5% de cas) pour tester l'ETL
    sexe_raw = random.choice(['MASCULIN', 'HOMME', 'feminin', 'Femme']) if random.random() < 0.05 else sexe
        
    etudiants.append({
        'id_etudiant': i,
        'matricule': f"{random.randint(2020, 2023)}{i:05d}",
        'nom': nom,
        'prenom': prenom,
        'sexe': sexe_raw,
        'age': random.randint(18, 28),
        'region_origine': random.choice(REGIONS),
        'type_bac': random.choice(TYPES_BAC),
        'statut_bourse': random.choice(['Oui', 'Non']),
        'statut_paiement': random.choice(['A jour', 'En retard', 'Exonéré'])
    })

df_etudiants = pd.DataFrame(etudiants)
df_etudiants.to_csv('etudiants.csv', index=False) # CSV pour la performance
print(f"✅ {len(df_etudiants)} étudiants sauvegardés en CSV.")

# --- 2. SAUVEGARDE DES DONNÉES DE RÉFÉRENCE ---
pd.DataFrame(MATIERES).to_csv('matieres.csv', index=False)
pd.DataFrame(ENSEIGNANTS).to_csv('enseignants.csv', index=False)
pd.DataFrame(FILIERES).to_csv('filieres.csv', index=False)
print("✅ Données de référence (Matières, Enseignants, Filières) sauvegardées.")

# --- 3. GÉNÉRATION MASSIVE DES NOTES (TABLE DE FAITS) ---
print(" Génération de ~1 500 000 lignes de notes (cela peut prendre 1 à 2 minutes)...")
notes = []

# Pour aller vite, on pré-calcule les listes
list_matieres = MATIERES
list_enseignants = ENSEIGNANTS
list_filieres = FILIERES

for etud in etudiants:
    # Simulation de parcours : 2 à 4 années (certains abandonnent ou redoublent)
    nb_annees = random.choices([1, 2, 3, 4], weights=[0.1, 0.2, 0.3, 0.4])[0]
    annees_jouees = random.sample(ANNEES, nb_annees)
    
    for annee in annees_jouees:
        for sem in SEMESTRES:
            nb_matieres = random.randint(4, 7)
            matieres_sem = random.sample(list_matieres, min(nb_matieres, len(list_matieres)))
            
            for mat in matieres_sem:
                ens = random.choice(list_enseignants)
                fil = random.choice(list_filieres)
                
                # Notes réalistes (loi normale)
                note_cc = round(np.random.normal(9.5, 3.5), 1)
                note_ex = round(np.random.normal(10.5, 4.0), 1)
                
                # Bornes [0, 20]
                note_cc = max(0, min(20, note_cc))
                note_ex = max(0, min(20, note_ex))
                
                moy = round((note_cc + note_ex) / 2, 1)
                credits = mat['credit'] if moy >= 10 else 0
                absences = int(np.random.exponential(4)) 
                
                # Données sales volontaires (2% de cas)
                note_cc_final = str(note_cc).replace('.', ',') if random.random() < 0.02 else note_cc
                
                notes.append({
                    'id_etudiant': etud['id_etudiant'],
                    'id_matiere': mat['id'],
                    'id_enseignant': ens['id'],
                    'id_filiere': fil['id'],
                    'annee_academique': annee,
                    'semestre': sem,
                    'note_cc': note_cc_final,
                    'note_examen': note_ex,
                    'moyenne_finale': '', # Calculé par ETL
                    'credits_obtenus': credits,
                    'heures_absence': absences,
                    'statut': '' # Calculé par ETL
                })

df_notes = pd.DataFrame(notes)
df_notes.to_csv('notes.csv', index=False)
print(f"✅ {len(df_notes)} lignes de notes générées et sauvegardées en CSV.")

print(f"\n🎉 GÉNÉRATION TERMINÉE EN {round(time.time() - start_time, 2)} SECONDES !")
print("Ton Data Warehouse est prêt pour le Big Data académique.")