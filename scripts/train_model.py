import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sentence_transformers import SentenceTransformer
import os

def train_and_evaluate():
    print("Loading dataset...")
    df = pd.read_csv("data/processed/cooked_dataset.csv")
    df['text'] = df['text'].fillna("")
    
    print("Loading SentenceTransformer model...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Embedding texts (this might take a minute)...")
    X_embeddings = embedder.encode(df['text'].tolist(), show_progress_bar=True)
    
    y_level = df['cooked_level']
    y_category = df['category']
    
    X_train, X_test, y_level_train, y_level_test, y_cat_train, y_cat_test = train_test_split(
        X_embeddings, y_level, y_category, test_size=0.2, random_state=42, stratify=y_level
    )
    
    print("\nTraining Logistic Regression on Semantic Embeddings for Cooked Level...")
    clf_level = LogisticRegression(max_iter=2000, class_weight='balanced')
    clf_level.fit(X_train, y_level_train)
    
    y_level_pred = clf_level.predict(X_test)
    print("Classification Report (Level):")
    print(classification_report(y_level_test, y_level_pred))
    
    print("\nTraining Logistic Regression for Category...")
    clf_cat = LogisticRegression(max_iter=2000, class_weight='balanced')
    clf_cat.fit(X_train, y_cat_train)
    
    y_cat_pred = clf_cat.predict(X_test)
    print("Classification Report (Category):")
    print(classification_report(y_cat_test, y_cat_pred))
    
    print("\nSaving lightweight LR models to backend/models/...")
    joblib.dump(clf_level, "backend/models/cooked_level_model.joblib")
    joblib.dump(clf_cat, "backend/models/category_model.joblib")
    print("Models saved successfully!")

if __name__ == "__main__":
    train_and_evaluate()
