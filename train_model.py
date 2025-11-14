# train_model.py
import pandas as pd
import pickle
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import r2_score

# Charger les données
df = pd.read_csv("Car_Purchasing_Data.csv")

# Préparation des données
# NOTE: include 'Gender' to match API and Streamlit expectations
features = ['Gender', 'Age', 'Annual Salary', 'Credit Card Debt', 'Net Worth']
X = df[features]
y = df['Car Purchase Amount']

# Split (faire le split avant de scaler pour éviter la fuite)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Construire pipeline avec préprocessing pour numériques et catégoriques
numeric_features = ['Age', 'Annual Salary', 'Credit Card Debt', 'Net Worth']
categorical_features = ['Gender']

numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])
categorical_transformer = Pipeline(steps=[('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ],
    remainder='drop'
)

# Pipelines pour modèles
knn_pipeline = Pipeline(steps=[('pre', preprocessor), ('knn', KNeighborsRegressor())])
svr_pipeline = Pipeline(steps=[('pre', preprocessor), ('svr', SVR())])

# Entraînement
knn_pipeline.fit(X_train, y_train)
svr_pipeline.fit(X_train, y_train)

knn_pred = knn_pipeline.predict(X_test)
svr_pred = svr_pipeline.predict(X_test)

knn_r2 = r2_score(y_test, knn_pred)
svr_r2 = r2_score(y_test, svr_pred)

print(f"KNN R²: {knn_r2:.4f}")
print(f"SVR R²: {svr_r2:.4f}")

if knn_r2 >= svr_r2:
    best_pipeline = knn_pipeline
    best_name = 'KNN'
    best_r2 = knn_r2
else:
    best_pipeline = svr_pipeline
    best_name = 'SVR'
    best_r2 = svr_r2

print(f"\nMeilleur modèle: {best_name} avec R²: {best_r2:.4f}")

# Sauvegarde du pipeline + metadata (unified artifact for API and app)
model_artifact = {
    'model': best_pipeline,
    'model_name': best_name,
    'features': features,
    'metrics': {'r2': float(best_r2)},
    'created_at': datetime.utcnow().isoformat()
}

with open('best_model.pkl', 'wb') as f:
    pickle.dump(model_artifact, f, protocol=pickle.HIGHEST_PROTOCOL)

print("Pipeline sauvegardée: best_model.pkl")