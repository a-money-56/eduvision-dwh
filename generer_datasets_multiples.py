import pandas as pd
import random
import os

# Création des dossiers
niveaux = ['Primaire', 'College', 'Lycee', 'Universite']
for niveau in niveaux:
    os.makedirs(f"datasets_{niveau}", exist_ok=True)

# --- DONNÉES DE RÉFÉRENCE PAR NIVEAU ---
config = {
    'Primaire': {
        'prefix': 'eleve',
        'classes': ['CP', 'CE1', 'CE2', 'CM1', 'CM2'],
        'matieres': ['Lecture', 'Calcul', 'Éveil', 'Sport'],
        'regions': ['Littoral', 'Centre', 'Ouest'],
        'note_max': 10
    },
    'College': {
        'prefix': 'eleve',
        'classes': ['6ème', '5ème', '4ème', '3ème'],
        'matieres': ['Mathématiques', 'Français', 'Histoire-Géo', 'SVT', 'Anglais'],
        'regions': ['Littoral', 'Centre', 'Ouest', 'Nord'],
        'note_max': 20
    },
    'Lycee': {
        'prefix': 'eleve',
        'classes': ['Seconde', 'Première', 'Terminale'],
        'matieres': ['Mathématiques', 'Philosophie', 'Physique-Chimie', 'SES', 'Anglais'],
        'regions': ['Littoral', 'Centre', 'Ouest', 'Nord', 'Sud'],
        'note_max': 20
    },
    'Universite': {
        'prefix': 'etudiant',
        'classes': ['L1', 'L2', 'L3', 'M1', 'M2'],
        'matieres': ['Algorithmique', 'Base de données', 'Économie', 'Droit', 'Management'],
        'regions': ['Littoral', 'Centre', 'Ouest', 'Nord', 'Sud', 'Est'],
        'note_max': 20
    }
}

noms_famille = ['NGUEMA', 'MBALLA', 'TCHOUA', 'FOFACK', 'KAMGA', 'BIYA', 'NDONGO', 'ESSOMBA', 'MBARGA', 'ATANGANA']
prenoms = ['Jean', 'Marie', 'Paul', 'Amina', 'David', 'Sarah', 'Marc', 'Léa', 'Pierre', 'Claire']

for niveau, cfg in config.items():
    print(f"🔄 Génération des données pour : {niveau}...")
    
    # 1. Fichier Élèves/Étudiants
    nb_personnes = random.randint(200, 500)
    data_personnes = []
    for i in range(1, nb_personnes + 1):
        data_personnes.append({
            'id': i,
            'matricule': f"{niveau[:3].upper()}{2023}{i:04d}",
            'nom': random.choice(noms_famille),
            'prenom': random.choice(prenoms),
            'sexe': random.choice(['M', 'F']),
            'age': random.randint(6, 25),
            'classe': random.choice(cfg['classes']),
            'region_origine': random.choice(cfg['regions']),
            'statut_bourse': random.choice(['Oui', 'Non']) if niveau in ['Lycee', 'Universite'] else 'N/A',
            'statut_paiement': random.choice(['À jour', 'En retard'])
        })
    df_personnes = pd.DataFrame(data_personnes)
    df_personnes.to_excel(f"datasets_{niveau}/{cfg['prefix']}s.xlsx", index=False)

    # 2. Fichier Matières
    data_matieres = []
    for i, mat in enumerate(cfg['matieres'], 1):
        data_matieres.append({
            'id': i,
            'code': f"{mat[:3].upper()}{i}01",
            'nom': mat,
            'credit': random.choice([2, 3, 4, 5]),
            'categorie': 'Fondamentale' if i < 3 else 'Éveil/Option'
        })
    df_matieres = pd.DataFrame(data_matieres)
    df_matieres.to_excel(f"datasets_{niveau}/matieres.xlsx", index=False)

    # 3. Fichier Notes
    data_notes = []
    for pers in data_personnes:
        # Chaque personne a 1 à 3 matières
        nb_mat = random.randint(1, 3)
        matieres_choisies = random.sample(cfg['matieres'], nb_mat)
        for mat in matieres_choisies:
            # Génération de notes avec une corrélation absences/échec
            absences = random.choices([0, 2, 5, 10, 15, 20], weights=[40, 20, 15, 10, 10, 5])[0]
            
            # Si beaucoup d'absences, note plus basse
            if absences > 10:
                note_cc = max(0, random.gauss(cfg['note_max'] * 0.4, 2))
                note_ex = max(0, random.gauss(cfg['note_max'] * 0.4, 3))
            else:
                note_cc = max(0, random.gauss(cfg['note_max'] * 0.65, 2))
                note_ex = max(0, random.gauss(cfg['note_max'] * 0.65, 3))
            
            # Adapter l'ID de la matière
            id_mat = next((m['id'] for m in data_matieres if m['nom'] == mat), 1)
            
            moyenne = (note_cc + note_ex) / 2
            seuil_reussite = cfg['note_max'] / 2
            
            data_notes.append({
                'id_personne': pers['id'],
                'id_matiere': id_mat,
                'id_enseignant': random.randint(101, 120),
                'id_filiere': 1, # Simplifié pour l'exemple
                'annee_academique': '2023-2024',
                'semestre': random.choice(['S1', 'S2']),
                'note_cc': round(note_cc, 2),
                'note_examen': round(note_ex, 2),
                'moyenne_finale': round(moyenne, 2),
                'credits_obtenus': random.choice([0, 2, 3, 4]) if moyenne >= seuil_reussite else 0,
                'heures_absence': absences,
                'statut': 'Valide' if moyenne >= seuil_reussite else 'Echoue'
            })
    
    df_notes = pd.DataFrame(data_notes)
    df_notes.to_excel(f"datasets_{niveau}/notes.xlsx", index=False)

print("✅ Génération terminée ! Vérifie les dossiers 'datasets_Primaire', 'datasets_College', etc.")