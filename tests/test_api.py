import pytest
import json
import requests
import random
import os

# URL de l'API
url = os.environ.get('API_URL','http://127.0.0.1:5050/predict')

def load_random_client():
    """ Charge un client aléatoire du fichier JSON. """
    with open('sample_clients.json', 'r') as file:
        data_json = json.load(file)
    return random.choice(data_json)

def test_api_response():
    """ Teste la réponse de base de l'API. """
    random_client = load_random_client()
    response = requests.post(url, json=random_client)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

def test_prediction_probability():
    """ Teste que la probabilité de prédiction est entre 0 et 1. """
    random_client = load_random_client()
    response = requests.post(url, json=random_client)
    prediction_proba = response.json()['prediction_proba'][0]
    assert 0 <= prediction_proba <= 1

def test_intuitive_score():
    """ Teste que le score intuitif est entre 0 et 100. """
    random_client = load_random_client()
    response = requests.post(url, json=random_client)
    score_intuitif = response.json()['score_intuitif'][0]
    assert 0 <= score_intuitif <= 100

def test_predict_with_invalid_data():
    """ Teste la réponse de l'API avec des données invalides. """
    invalid_data = {'some_invalid_key': 'invalid_value'}
    response = requests.post(url, json=invalid_data)
    assert response.status_code in [400, 500]
