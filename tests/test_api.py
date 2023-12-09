import requests
import os

def test_api_root():
    """ Teste la route racine de l'API. """
    # URL de l'API récupérée depuis les variables d'environnement
    url = os.environ.get('API_URL', 'http://127.0.0.1:5050') + '/'

    # Envoyer une requête GET à la route racine
    response = requests.get(url)

    # Vérifier que la réponse est 200 OK
    assert response.status_code == 200
    # Vérifier le contenu de la réponse
    assert response.text == 'Api lancée'
