from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

# Global variables
model = None
model_name = "Aucun modèle chargé"
model_features = None

# Robust model loader: supports either a dict artifact or a raw pipeline
def load_model_file(path='best_model.pkl'):
    try:
        with open(path, 'rb') as f:
            obj = pickle.load(f)
    except FileNotFoundError:
        print(f"Fichier modèle {path} non trouvé")
        return None, "Aucun modèle chargé", None
    except Exception as e:
        print(f"Erreur lors du chargement du modèle: {str(e)}")
        return None, "Aucun modèle chargé", None

    # Debug: print what we loaded
    print(f"Type d'objet chargé: {type(obj)}")

    if isinstance(obj, dict):
        model = obj.get('model')
        model_name = obj.get('model_name', 'Modèle inconnu')
        features = obj.get('features')
        print(f"Modèle chargé depuis dict: {model_name}")
    else:
        model = obj
        model_name = getattr(obj, 'name', 'Pipeline')
        features = None
        print(f"Modèle chargé directement: {model_name}")

    return model, model_name, features

# Load at startup (will return None if missing)
print("Chargement du modèle...")
loaded_model, loaded_name, loaded_features = load_model_file('best_model.pkl')

# Update global variables
if loaded_model is not None:
    model = loaded_model
    model_name = loaded_name
    model_features = loaded_features
    print(f"✓ Modèle chargé avec succès: {model_name}")
else:
    print("✗ ERREUR: Le modèle n'a pas été trouvé. Veuillez d'abord exécuter l'entraînement.")

@app.route('/')
def home():
    return jsonify({
        'message': 'API de prédiction du prix des voitures',
        'model': model_name,
        'endpoints': {
            '/health': 'GET - Statut de l\'API',
            '/predict': 'POST - Prédire le prix d\'une voiture',
            '/batch_predict': 'POST - Prédictions par lot'
        },
        'documentation': 'Voir /help pour plus d\'informations'
    })


@app.route('/health')
def health():
    if model is not None:
        status = 'healthy'
        model_status = model_name
    else:
        status = 'no model loaded'
        model_status = 'Aucun modèle chargé'

    return jsonify({'status': status, 'model': model_status})

@app.route('/help')
def help():
    return jsonify({
        'documentation': {
            'input_format': {
                'Gender': 'int (0=Femme, 1=Homme)',
                'Age': 'int',
                'Annual Salary': 'float',
                'Credit Card Debt': 'float',
                'Net Worth': 'float'
            },
            'endpoints': {
                'POST /predict': {
                    'description': 'Prédiction unique',
                    'example_request': {
                        'Gender': 1,
                        'Age': 45,
                        'Annual Salary': 70000,
                        'Credit Card Debt': 10000,
                        'Net Worth': 400000
                    }
                },
                'POST /batch_predict': {
                    'description': 'Prédictions par lot',
                    'example_request': {
                        'records': [
                            {
                                'Gender': 1,
                                'Age': 35,
                                'Annual Salary': 60000,
                                'Credit Card Debt': 8000,
                                'Net Worth': 300000
                            }
                        ]
                    }
                }
            }
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Modèle non disponible. Entraînez d\'abord le modèle.'}), 500
    
    try:
        # Récupération des données JSON
        data = request.get_json()

        if not data:
            return jsonify({'error': 'Aucune donnée JSON fournie'}), 400

        # Validation des champs requis
        required_fields = ['Gender', 'Age', 'Annual Salary', 'Credit Card Debt', 'Net Worth']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ manquant: {field}'}), 400

        # Validation des types and construct DataFrame
        try:
            input_data = pd.DataFrame([{
                'Gender': int(data['Gender']),
                'Age': float(data['Age']),
                'Annual Salary': float(data['Annual Salary']),
                'Credit Card Debt': float(data['Credit Card Debt']),
                'Net Worth': float(data['Net Worth'])
            }])
        except (ValueError, TypeError) as e:
            return jsonify({'error': f'Type de données invalide: {str(e)}'}), 400

        # If saved features are available, reorder and validate
        if model_features:
            missing = [c for c in model_features if c not in input_data.columns]
            if missing:
                return jsonify({'error': f'Missing columns required by model: {missing}'}), 400
            input_data = input_data[model_features]

        # Prédiction
        prediction = model.predict(input_data)[0]

        return jsonify({
            'predicted_car_price': round(float(prediction), 2),
            'model_used': model_name,
            'input_data': data
        })

    except Exception as e:
        return jsonify({'error': f'Erreur lors de la prédiction: {str(e)}'}), 500

@app.route('/batch_predict', methods=['POST'])
def batch_predict():
    if model is None:
        return jsonify({'error': 'Modèle non disponible'}), 500
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Aucune donnée JSON fournie'}), 400
        
        records = data.get('records', [])

        if not records:
            return jsonify({'error': 'Aucun enregistrement fourni'}), 400

        if not isinstance(records, list):
            return jsonify({'error': 'Le champ "records" doit être une liste'}), 400

        # Validation des enregistrements
        validated_records = []
        for i, record in enumerate(records):
            if not isinstance(record, dict):
                return jsonify({'error': f'L\'enregistrement {i} doit être un objet JSON'}), 400

            required_fields = ['Gender', 'Age', 'Annual Salary', 'Credit Card Debt', 'Net Worth']
            for field in required_fields:
                if field not in record:
                    return jsonify({'error': f'Champ manquant dans l\'enregistrement {i}: {field}'}), 400

            try:
                validated_records.append({
                    'Gender': int(record['Gender']),
                    'Age': float(record['Age']),
                    'Annual Salary': float(record['Annual Salary']),
                    'Credit Card Debt': float(record['Credit Card Debt']),
                    'Net Worth': float(record['Net Worth'])
                })
            except (ValueError, TypeError) as e:
                return jsonify({'error': f'Type de données invalide dans l\'enregistrement {i}: {str(e)}'}), 400

        # Conversion en DataFrame
        input_data = pd.DataFrame(validated_records)

        # If saved features are available, reorder and validate
        if model_features:
            missing = [c for c in model_features if c not in input_data.columns]
            if missing:
                return jsonify({'error': f'Missing columns required by model: {missing}'}), 400
            input_data = input_data[model_features]

        # Prédictions
        predictions = model.predict(input_data)

        results = []
        for i, (record, pred) in enumerate(zip(records, predictions)):
            results.append({
                'record_id': i,
                'predicted_car_price': round(float(pred), 2),
                'input_data': record
            })

        return jsonify({
            'predictions': results,
            'model_used': model_name,
            'total_predictions': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la prédiction par lot: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)