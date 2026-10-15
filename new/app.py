from flask import Flask, render_template
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# Connexion à ton DWH existant
engine = create_engine("postgresql+psycopg2://postgres:admin123@localhost:5432/dwh_iut_douala")

@app.route('/')
def dashboard():
    # 1. Données pour le graphique (Taux de réussite par filière)
    query_chart = """
        SELECT f.nom_filiere, 
               ROUND(100.0 * SUM(CASE WHEN fp.statut = 'Valide' THEN 1 ELSE 0 END) / COUNT(*), 1) as taux_reussite
        FROM fait_performance fp
        JOIN dim_filiere f ON fp.id_filiere = f.id_filiere
        GROUP BY f.nom_filiere
        ORDER BY taux_reussite DESC;
    """
    df_chart = pd.read_sql(query_chart, engine)
    
    # 2. Données pour le tableau interactif (Échantillon de 200 évaluations)
    query_table = """
        SELECT e.matricule, e.nom, e.prenom, f.nom_filiere, m.nom_matiere, 
               ROUND(fp.moyenne_finale::numeric, 2) as moyenne, fp.statut
        FROM fait_performance fp
        JOIN dim_etudiant e ON fp.id_etudiant = e.id_etudiant
        JOIN dim_filiere f ON fp.id_filiere = f.id_filiere
        JOIN dim_matiere m ON fp.id_matiere = m.id_matiere
        LIMIT 200;
    """
    df_table = pd.read_sql(query_table, engine)
    
    # 3. KPI Globaux (CORRECTION ICI : on nomme la colonne 'total' pour éviter le bug KeyError)
    df_count = pd.read_sql('SELECT COUNT(*) as total FROM fait_performance', engine)
    kpi_total = f"{int(df_count['total'].iloc[0]):,}"
    
    # Calcul du taux de réussite moyen global
    kpi_reussite = f"{round(df_chart['taux_reussite'].mean(), 1)}%"

    # On envoie toutes les variables au fichier HTML
    return render_template('dashboard.html', 
                           labels=df_chart['nom_filiere'].tolist(), 
                           values=df_chart['taux_reussite'].tolist(),
                           kpi_total=kpi_total,
                           kpi_reussite=kpi_reussite,
                           table_html=df_table.to_html(classes='table table-striped table-hover datatable', index=False))

if __name__ == '__main__':
    app.run(debug=True, port=5000)