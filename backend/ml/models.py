"""
Model architectures and ensemble pipeline builder.
"""
import os
import joblib
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from config import (
    NUMERIC_FEATURES, TEXT_FEATURE,
    TFIDF_MAX_FEATURES, TFIDF_NGRAM_RANGE,
    MODELS_DIR
)
from utils import get_logger

logger = get_logger('models')

def build_ensemble_pipeline() -> Pipeline:
    """
    Builds the Master Ensemble ML Pipeline.
    Routes heterogeneous features (numeric vs text) and combines 3 base models via Soft Voting.
    """
    logger.info("Building heterogeneous data preprocessor (Scaler + TF-IDF)...")
    
    # 1. Feature Preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), NUMERIC_FEATURES),
            ('text', TfidfVectorizer(
                max_features=TFIDF_MAX_FEATURES, 
                ngram_range=TFIDF_NGRAM_RANGE,
                stop_words='english' # ignore standard text if it accidentally gets into class
            ), TEXT_FEATURE)
        ],
        remainder='drop'
    )

    logger.info("Initializing base models (RF, LR, GradientBoost)...")
    
    # 2. Base Models
    # Model A: Random Forest (Excellent for non-linear tabular structural data)
    rf = RandomForestClassifier(random_state=42)
    
    # Model B: Logistic Regression (Excellent for sparse text/TF-IDF data)
    lr = LogisticRegression(class_weight='balanced', random_state=42)
    
    # Model C: Gradient Boosting (Strong all-rounder to catch edge cases)
    gb = GradientBoostingClassifier(random_state=42)

    # 3. Ensemble Fusion
    logger.info("Fusing models into Soft Voting Ensemble...")
    ensemble = VotingClassifier(
        estimators=[
            ('rf', rf), 
            ('lr', lr), 
            ('gb', gb)
        ],
        voting='soft' # Uses probabilities rather than hard class predictions
    )

    # 4. Master Pipeline
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', ensemble)
    ])

    return pipeline

def save_model(pipeline: Pipeline, filename='ui_critic_ensemble.pkl') -> str:
    """Persists the trained scikit-learn pipeline to disk."""
    path = os.path.join(MODELS_DIR, filename)
    joblib.dump(pipeline, path)
    logger.info(f"Model saved successfully to {path}")
    return path

def load_model(filename='ui_critic_ensemble.pkl') -> Pipeline:
    """Loads a persisted model from disk."""
    path = os.path.join(MODELS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at {path}. Have you run train.py?")
    
    pipeline = joblib.load(path)
    logger.info(f"Model loaded successfully from {path}")
    return pipeline
