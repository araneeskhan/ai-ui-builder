import os
import random
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from features import extract_advanced_features, NUMERIC_FEATURES, TEXT_FEATURE

def generate_good_html():
    items = random.randint(3, 8)
    lis = "".join([f'<li class="flex items-center gap-2 text-zinc-300"><i class="fas fa-check text-emerald-400"></i>Item {i}</li>' for i in range(items)])
    return f"""
    <div class="w-full max-w-sm rounded-2xl border border-zinc-800 bg-zinc-900 p-8">
        <h3 class="text-lg font-semibold text-white">Pro Plan</h3>
        <p class="mt-1 text-sm text-zinc-400">Description here</p>
        <ul class="mt-8 space-y-3">
            {lis}
        </ul>
        <button class="mt-8 w-full rounded-xl bg-indigo-600 py-3 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors">Subscribe</button>
    </div>
    """

def generate_bad_html():
    bad_type = random.choice(['div_soup', 'empty', 'unstyled'])
    if bad_type == 'div_soup':
        return "<div>" * 10 + "Text" + "</div>" * 10
    elif bad_type == 'empty':
        return '<div class="flex bg-zinc-900"></div>'
    else:
        return '<div><h1>Title</h1><p>Text</p><button class="btn">Click</button></div>'

def build_dataset(num_samples=2000):
    print(f"Procedurally generating {num_samples} raw HTML strings...")
    data = []
    labels = []
    
    for _ in range(num_samples // 2):
        html = generate_good_html()
        data.append(extract_advanced_features(html))
        labels.append(1)
        
    for _ in range(num_samples // 2):
        html = generate_bad_html()
        data.append(extract_advanced_features(html))
        labels.append(0)
        
    df = pd.DataFrame(data)
    return df, np.array(labels)

def train_ensemble_pipeline():
    print("==============================================")
    print("   Starting High-Level Ensemble ML Pipeline")
    print("==============================================")
    
    X, y = build_dataset(2000)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\n--- 1. Building Heterogeneous Pipeline ---")
    # ColumnTransformer routes numeric data to the Scaler, and text data to the TF-IDF Vectorizer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), NUMERIC_FEATURES),
            ('text', TfidfVectorizer(max_features=500), TEXT_FEATURE)
        ]
    )
    
    print("--- 2. Building Ensemble Classifier ---")
    # Model A: Structural features handled primarily by Random Forest
    rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    
    # Model B: Semantic text features handled well by Logistic Regression (SVM-like)
    lr = LogisticRegression(max_iter=1000, random_state=42)
    
    # The Fusion: Soft Voting Classifier combines their probabilities
    ensemble = VotingClassifier(
        estimators=[('rf', rf), ('lr', lr)],
        voting='soft'
    )
    
    # Complete Pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', ensemble)
    ])
    
    print("--- 3. Training Ensemble Model... ---")
    pipeline.fit(X_train, y_train)
    
    print("\n--- 4. Evaluation ---")
    preds = pipeline.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, preds) * 100:.2f}%\n")
    print("Classification Report:\n", classification_report(y_test, preds))
    
    print("\n--- 5. Saving Production Pipeline ---")
    save_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(save_dir, 'ui_critic_ensemble.pkl')
    joblib.dump(pipeline, model_path)
    print(f"-> Master Pipeline saved successfully to {model_path}.")
    print("\n[Done] Your Ensemble AI is ready for inference!")

if __name__ == '__main__':
    train_ensemble_pipeline()
