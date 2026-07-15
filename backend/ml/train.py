import os
import random
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

def generate_synthetic_data(num_samples=2000):
    """
    Generates a synthetic dataset.
    Label 1 = Good UI (complex, many Tailwind classes, deep layout)
    Label 0 = Bad UI (blank, broken, unstyled, mostly empty)
    """
    data = []
    
    # 1. Generate Good UIs
    for _ in range(num_samples // 2):
        tags = random.randint(15, 60)
        classes = random.randint(20, 100)
        depth = random.randint(3, 8)
        
        data.append({
            'num_tags': tags,
            'max_depth': depth,
            'num_classes': classes,
            'has_layout': 1,
            'has_colors': 1,
            'has_padding': 1,
            'empty_ratio': random.uniform(0.0, 0.2),
            'label': 1
        })
        
    # 2. Generate Bad UIs (Blank pages, simple text, broken structure)
    for _ in range(num_samples // 2):
        tags = random.randint(1, 10)
        classes = random.randint(0, 10)
        depth = random.randint(1, 3)
        has_layout = random.choice([0, 1])
        has_colors = random.choice([0, 1])
        has_padding = random.choice([0, 1])
        
        # If it has styling, it must be mostly empty tags to be "bad"
        if has_layout and has_colors and has_padding:
            empty_ratio = random.uniform(0.6, 1.0)
        else:
            empty_ratio = random.uniform(0.1, 1.0)
            
        data.append({
            'num_tags': tags,
            'max_depth': depth,
            'num_classes': classes,
            'has_layout': has_layout,
            'has_colors': has_colors,
            'has_padding': has_padding,
            'empty_ratio': empty_ratio,
            'label': 0
        })
        
    return pd.DataFrame(data)

def train_model():
    print("Generating synthetic dataset (N=2000)...")
    df = generate_synthetic_data(2000)
    
    X = df.drop('label', axis=1)
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Classifier (CPU)...")
    clf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    clf.fit(X_train, y_train)
    
    preds = clf.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Accuracy on Test Set: {acc * 100:.2f}%")
    
    # Save model
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_critic_model.pkl')
    joblib.dump(clf, model_path)
    print(f"Model successfully saved to {model_path}")

if __name__ == '__main__':
    train_model()
