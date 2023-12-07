from flask import Flask, request, jsonify
import pandas as pd
import pickle
import logging
import os

# Chemin du modèle 
model_path = os.path.join(os.path.dirname(__file__), 'model/model.pkl')



# Configurer le logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')




# Chargement du modèle
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Initialisation de l'application Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return 'Api lancée'

# Route pour les prédictions, accessible via une requête HTTP POST
@app.route('/predict', methods=['POST'])
def predict():
    # Récupération des données JSON envoyées à l'API
    data = request.json
    logging.debug(f'Requête reçue avec les données: {data}')

    # Vérification que des données sont fournies
    if data is None:
        logging.error('Aucune donnée fournie')
        return jsonify({'error': 'No data provided'}), 400

    # Conversion des données JSON en DataFrame pandas
    data_df = pd.DataFrame([data])

    # Bloc try pour la gestion d'erreurs lors de la prédiction
    try:
        # Utilisation du modèle pour faire une prédiction de probabilité sur les données fournies
        prediction_proba = model.predict_proba(data_df)[:, 1]  # Récupère seulement la probabilité pour la classe 1
        # Calcul du score intuitif
        score_intuitif = (1 - prediction_proba) * 100
        logging.debug(f'Prédiction réussie: {prediction_proba}, Score intuitif: {score_intuitif}')
    except Exception as e:
        # En cas d'erreur, on retourne une erreur
        logging.error(f'Erreur lors de la prédiction: {e}')
        return jsonify({'error': str(e)}), 500
    
    # Retourne la probabilité et le score sous forme de réponse JSON
    return jsonify({'prediction_proba': prediction_proba.tolist(), 'score_intuitif': score_intuitif.tolist()})

# Point d'entrée principal pour l'exécution de l'application Flask
if __name__ == '__main__':
    app.run(debug=True, port=5050)