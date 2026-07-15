import sys
import json
import os
import pandas as pd
import joblib
from features import extract_advanced_features

def run_inference(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
            
        base_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(base_dir, 'ui_critic_ensemble.pkl')
        
        if not os.path.exists(model_path):
            print(json.dumps({"error": "Ensemble Pipeline not found. Run train.py first."}))
            sys.exit(1)
            
        # Load the Master Ensemble Pipeline (includes Preprocessor + VotingClassifier)
        pipeline = joblib.load(model_path)
        
        # Extract features (returns dict)
        raw_features_dict = extract_advanced_features(html)
        
        # Pipeline expects a DataFrame for ColumnTransformer routing
        df = pd.DataFrame([raw_features_dict])
        
        # Predict
        prediction = pipeline.predict(df)[0]
        probabilities = pipeline.predict_proba(df)[0]
        score = probabilities[1] * 100  
        
        # Generate deterministic critique based on the raw metrics
        critique = "Looks good"
        if prediction == 0:
            critique = "The Ensemble Model rejected this UI. "
            if raw_features_dict['tailwind_density'] < 0.5:
                critique += "It lacks Tailwind class density. "
            if raw_features_dict['layout_cohesion'] < 0.1:
                critique += "It is missing layout structure (flex, grid). "
            if raw_features_dict['empty_ratio'] > 0.5:
                critique += "There are too many empty tags. "
            if raw_features_dict['semantic_ratio'] < 0.1:
                critique += "Use semantic HTML tags (nav, main, button) instead of just divs. "
                
            critique += "Please rewrite the HTML to fix these structural issues."
        
        print(json.dumps({
            "score": round(score, 2),
            "is_approved": bool(prediction == 1),
            "critique": critique
        }))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No HTML file path provided."}))
        sys.exit(1)
        
    run_inference(sys.argv[1])
