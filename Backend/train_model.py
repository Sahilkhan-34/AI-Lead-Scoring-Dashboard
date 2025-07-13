import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

# Load data
df = pd.read_csv("C:/Users/sahil/OneDrive/Naresh IT Class/ML_End_To_End_Projects/Internship Projects/AI Lead Scoring Dashboard Prototype/Backend/lead_data.csv")

# Define features (X) and target (y)
# We drop non-informative features for the initial model
features = ['CreditScore', 'AgeGroup', 'FamilyBackground', 'Income']
target = 'Intent'

X = df[features]
y = df[target]

# Identify categorical and numerical features
categorical_features = ['AgeGroup', 'FamilyBackground']
numerical_features = ['CreditScore', 'Income']

# Create preprocessing pipelines for numerical and categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Define the model pipeline
model = Pipeline(steps=[('preprocessor', preprocessor),
                      ('classifier', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42))])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Evaluate the model
accuracy = model.score(X_test, y_test)
print(f"Model Accuracy: {accuracy:.4f}")

# Save the entire pipeline to a file
joblib.dump(model, "model.pkl")

print("Model trained and saved as 'model.pkl'.")