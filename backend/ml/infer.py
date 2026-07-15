import sys
import json
import os
from bs4 import BeautifulSoup
import joblib

def extract_features(html: str):
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(True)
    
    num_tags = len(tags)
    depths = [len(list(tag.parents)) for tag in tags]
    max_depth = max(depths) if depths else 0
    
    classes = []
    for tag in tags:
        classes.extend(tag.get('class', []))
    num_classes = len(classes)
    
    has_layout = int(any(c in ['flex', 'grid', 'absolute', 'relative'] for c in classes))
    has_colors = int(any(c.startswith('bg-') or c.startswith('text-') for c in classes))
    has_padding = int(any(c.startswith('p-') or c.startswith('px-') or c.startswith('py-') for c in classes))
    
    empty_tags = sum(1 for tag in tags if not tag.text.strip() and not tag.find_all())
    empty_ratio = empty_tags / num_tags if num_tags > 0 else 1.0

    return [[
        num_tags,
        max_depth,
        num_classes,
        has_layout,
        has_colors,
        has_padding,
        empty_ratio
    ]]

def run_inference(html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
            
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ui_critic_model.pkl')
        
        if not os.path.exists(model_path):
            print(json.dumps({"error": "Model not found. Run train.py first."}))
            sys.exit(1)
            
        clf = joblib.load(model_path)
        features = extract_features(html)
        
        prediction = clf.predict(features)[0]
        probabilities = clf.predict_proba(features)[0]
        score = probabilities[1] * 100  # Probability of being "Good"
        
        # Generate deterministic critique based on feature analysis
        critique = "Looks good"
        if prediction == 0:
            critique = "The UI is structurally poor. "
            feat = features[0]
            if feat[0] < 10:
                critique += "It doesn't have enough elements (too blank). "
            if feat[2] < 10:
                critique += "It is missing Tailwind classes (unstyled). "
            if feat[3] == 0:
                critique += "It is missing layout classes like flex or grid. "
            if feat[6] > 0.5:
                critique += "There are too many empty tags without text. "
                
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
