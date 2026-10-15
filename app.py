from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import psycopg2
import subprocess
import sys
import os

# ==========================================
# CONFIGURATION
# ==========================================
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="dwh_iut_douala",
        user="postgres",
        password="admin123"
    )

# ==========================================
# ROUTES D'AFFICHAGE
# ==========================================
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# ==========================================
# API : DONNÉES POUR LES GRAPHIQUES
# ==========================================
@app.route('/api/taux_reussite_global')
def taux_reussite_global():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT ROUND(100.0 * SUM(CASE WHEN statut = 'Valide' THEN 1 ELSE 0 END) / COUNT(*), 1) FROM fait_performance;")
        taux = cur.fetchone()[0]
        cur.close(); conn.close()
        return jsonify({'taux': float(taux) if taux else 0.0})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/moyenne_filiere')
def moyenne_filiere():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT f.nom_filiere, ROUND(AVG(fp.moyenne_finale)::numeric, 2) as moyenne 
            FROM fait_performance fp JOIN dim_filiere f ON fp.id_filiere = f.id_filiere 
            GROUP BY f.nom_filiere ORDER BY moyenne DESC;
        """)
        data = [{'label': row[0], 'value': float(row[1])} for row in cur.fetchall()]
        cur.close(); conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/repartition_statut')
def repartition_statut():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT statut, COUNT(*) FROM fait_performance GROUP BY statut;")
        data = [{'label': row[0], 'value': int(row[1])} for row in cur.fetchall()]
        cur.close(); conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/impact_absences')
def impact_absences():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                CASE WHEN heures_absence <= 5 THEN '0-5h' WHEN heures_absence <= 10 THEN '6-10h' WHEN heures_absence <= 15 THEN '11-15h' ELSE '16h et +' END as tranche,
                COUNT(*) as total,
                ROUND(100.0 * SUM(CASE WHEN statut = 'Echoue' THEN 1 ELSE 0 END) / COUNT(*), 1) as taux_echec
            FROM fait_performance GROUP BY tranche 
            ORDER BY CASE tranche WHEN '0-5h' THEN 1 WHEN '6-10h' THEN 2 WHEN '11-15h' THEN 3 ELSE 4 END;
        """)
        data = [{'tranche': row[0], 'total': int(row[1]), 'taux_echec': float(row[2])} for row in cur.fetchall()]
        cur.close(); conn.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==========================================
# API : TÉLÉVERSEMENT ET MISE À JOUR (ÉTAPE 2)
# ==========================================
@app.route('/api/upload', methods=['POST'])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({'statut': 'erreur', 'message': 'Aucun fichier envoyé.'}), 400
        
        files = request.files.getlist('files')
        fichiers_recus = [f.filename for f in files]
        
        # Vérifier qu'on a bien les 3 fichiers attendus
        requis = {'etudiants.xlsx', 'matieres.xlsx', 'notes.xlsx'}
        if not requis.issubset(set(fichiers_recus)):
            return jsonify({'statut': 'erreur', 'message': f'Fichiers manquants. Attendus: etudiants.xlsx, matieres.xlsx, notes.xlsx. Reçus: {", ".join(fichiers_recus)}'}), 400

        # Sauvegarder (écraser) les fichiers
        for file in files:
            if file.filename in requis:
                file.save(os.path.join(os.getcwd(), file.filename))

        # Lancer le script ETL avec les nouveaux fichiers
        resultat = subprocess.run([sys.executable, 'etl_iut.py'], capture_output=True, text=True, cwd=os.getcwd())
        
        if resultat.returncode == 0:
            return jsonify({'statut': 'succes', 'message': 'Fichiers téléversés et Data Warehouse mis à jour avec succès !'})
        else:
            return jsonify({'statut': 'erreur', 'message': f'Erreur ETL : {resultat.stderr}'}), 500
            
    except Exception as e:
        return jsonify({'statut': 'erreur', 'message': str(e)}), 500

# ==========================================
# DÉMARRAGE DU SERVEUR
# ==========================================
if __name__ == '__main__':
    print("✅ Serveur EduVision démarré sur http://127.0.0.1:5000")
    app.run(debug=True, port=5000)