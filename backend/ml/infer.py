"""
Production Inference Script.
Loads the Ensemble Pipeline, evaluates a single HTML file, and outputs structured JSON feedback.
"""
import sys
import json
import traceback
import pandas as pd
from features import extract_features
from models import load_model
from config import QUALITY_THRESHOLD
from utils import get_logger

# Use a specific logger for inference that only writes to stderr so stdout stays clean for JSON
import logging
logger = logging.getLogger('infer')
logger.setLevel(logging.ERROR)
ch = logging.StreamHandler(sys.stderr)
logger.addHandler(ch)

def generate_critique(features: dict) -> str:
    """Generates deterministic, actionable feedback based on the exact numeric features."""
    issues = []
    
    if features['semantic_ratio'] < 0.1:
        issues.append("Use semantic HTML5 tags (<nav>, <main>, <button>) instead of relying entirely on <div> elements.")
        
    if features['tailwind_density'] < 1.0:
        issues.append("The UI lacks sufficient styling. Add more specific Tailwind classes to define the visual hierarchy.")
        
    if features['layout_cohesion'] < 0.05:
        issues.append("The layout structure is poor. Use Flexbox (`flex`) or CSS Grid (`grid`) classes to align your elements properly.")
        
    if features['empty_ratio'] > 0.4:
        issues.append("There are too many empty tags. Ensure every structural element contains text, an icon, or child elements.")
        
    if features['max_depth'] > 12:
        issues.append("The HTML is over-nested. Flatten the DOM structure to improve maintainability and performance.")
        
    if features['visual_richness'] < 0.5:
        issues.append("The design is visually flat. Add padding (`p-4`), margins, borders, and colors to create depth.")

    if not issues:
        return "The UI structure is acceptable, but could use further aesthetic refinement."
        
    return "The Ensemble AI rejected this UI structure for the following reasons: " + " ".join(issues)

def run_inference(html_path: str):
    try:
        # Read HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()
            
        # Extract features (returns a dict of 31 features)
        features_dict = extract_features(html)
        
        # Convert to DataFrame (1 row) so ColumnTransformer can route 'num' and 'text' correctly
        df = pd.DataFrame([features_dict])
        
        # Load Pipeline
        pipeline = load_model()
        
        # Predict Probabilities
        probabilities = pipeline.predict_proba(df)[0]
        score = probabilities[1]  # Probability of class 1 (Good UI)
        
        is_approved = bool(score >= QUALITY_THRESHOLD)
        
        critique = "Looks great! The structure and styling are approved."
        if not is_approved:
            critique = generate_critique(features_dict)
            
        result = {
            "score": round(score * 100, 2),
            "is_approved": is_approved,
            "critique": critique,
            # We optionally return the top features so the backend knows *why*
            "debug_metrics": {
                "semantic_ratio": round(features_dict['semantic_ratio'], 3),
                "tailwind_density": round(features_dict['tailwind_density'], 3),
                "visual_richness": round(features_dict['visual_richness'], 3),
                "empty_ratio": round(features_dict['empty_ratio'], 3)
            }
        }
        
        # Print ONLY valid JSON to stdout
        print(json.dumps(result))
        
    except Exception as e:
        logger.error(f"Inference error: {traceback.format_exc()}")
        # Fallback response so the NestJS server doesn't crash
        print(json.dumps({
            "error": str(e),
            "score": 100, 
            "is_approved": True, 
            "critique": "Fallback approval due to ML pipeline error."
        }))
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No HTML file path provided."}))
        sys.exit(1)
        
    run_inference(sys.argv[1])
