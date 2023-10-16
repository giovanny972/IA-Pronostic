from flask import Flask, jsonify, request
from flask_cors import CORS
import csv
import json

app = Flask(__name__)
CORS(app)

# Fonction pour lire le fichier CSV et renvoyer un objet avec les données
@app.route('/load_data', methods=['GET'])
def load_data():
    horse_data = {}

    # Charger les données du fichier CSV
    with open('chevaux.csv', newline='', encoding='utf-8') as csvfile:
        data = list(csv.reader(csvfile, delimiter=';'))  # Spécifier le délimiteur

    # Ajouter les données du CSV à l'objet
    for row in data[1:]:  # Ignorer la première ligne d'en-tête
        horse_name = row[0].strip()  # Supprimer les espaces autour du nom
        wins = int(row[5])  # Changer l'index en fonction de votre fichier CSV
        horse_data[horse_name] = {"victoires": wins}
        
    # Charger les données du fichier JSON
    with open('chevaux.json', 'r', encoding='utf-8') as jsonfile:
        json_data = json.load(jsonfile)

    # Effectuer une analyse et obtenir les pronostics de victoire
    horse_name_to_analyze = request.args.get('horse_name')  # Obtenir le nom du cheval à analyser depuis les paramètres de l'URL

    win_predictions = []

    for horse_name, data in json_data.items():
        if horse_name == horse_name_to_analyze:
            win_predictions.append(data)

    return jsonify({
        "horse_data": horse_data,
        "win_predictions": win_predictions
    })


if __name__ == '__main__':
    app.run()

























# from flask import Flask, jsonify
# import csv
# import json

# app = Flask(__name__)

# # Fonction pour lire le fichier CSV et JSON et renvoyer un objet avec les données
# @app.route('/')
# def load_data():
#     # Charger les données du fichier CSV
#     with open('chevaux.csv', newline='', encoding='utf-8') as csvfile:
#         csvreader = csv.reader(csvfile, delimiter=';')
#         next(csvreader)  # Ignorer la première ligne (en-têtes)
#         data = list(csvreader)

#     # Charger les données du fichier JSON
#     with open('chevaux.json', 'r', encoding='utf-8') as jsonfile:
#         json_data = json.load(jsonfile)

#     # Créer un objet pour stocker les données
#     horse_data = {}

#     # Ajouter les données du CSV à l'objet
#     for row in data:
#         horse_name = row[0]
#         if len(row) >= 2:
#             wins = int(row[1])
#         else:
#             wins = 0
#         horse_data[horse_name] = {"victoires": wins}

#     # Ajouter les données du JSON à l'objet
#     for entry in json_data:
#         horse_name = entry['name']
#         wins = entry['wins']
#         if horse_name in horse_data:
#             horse_data[horse_name]["victoires"] += wins
#         else:
#             horse_data[horse_name] = {"victoires": wins}

#     return jsonify(horse_data)

# if __name__ == '__main__':
#     app.run()
