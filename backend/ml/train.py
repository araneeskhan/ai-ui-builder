"""
Master Training Orchestrator.
Generates data, extracts features, trains the ensemble, evaluates, and saves reports.
"""
import time
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

from config import NUM_SAMPLES, TRAIN_TEST_SPLIT, RANDOM_SEED
from data_generator import generate_raw_dataset
from features import extract_features_batch
from models import build_ensemble_pipeline, save_model
from evaluate import run_full_evaluation
from utils import get_logger, timed, save_training_report

logger = get_logger('train')

@timed
def main():
    print("\n" + "="*60)
    print("🚀 INITIALIZING MASTER'S LEVEL ML ENSEMBLE PIPELINE")
    print("="*60 + "\n")
    
    start_time = time.time()

    # ─────────────────────────────────────────────────────────
    # 1. Data Generation
    # ─────────────────────────────────────────────────────────
    logger.info("PHASE 1: Data Engineering")
    html_list, labels = generate_raw_dataset(NUM_SAMPLES)
    
    # ─────────────────────────────────────────────────────────
    # 2. Feature Extraction
    # ─────────────────────────────────────────────────────────
    logger.info("PHASE 2: Advanced Feature Extraction")
    X = extract_features_batch(html_list)
    y = pd.Series(labels)
    
    logger.info(f"Dataset Shape: {X.shape[0]} samples, {X.shape[1]} features")

    # ─────────────────────────────────────────────────────────
    # 3. Train/Test Split
    # ─────────────────────────────────────────────────────────
    logger.info("PHASE 3: Dataset Splitting")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=TRAIN_TEST_SPLIT, 
        random_state=RANDOM_SEED, 
        stratify=y  # Ensure balanced classes in both splits
    )
    logger.info(f"Training on {len(X_train)} samples, validating on {len(X_test)} samples.")

    # ─────────────────────────────────────────────────────────
    # 4. Model Building & Training
    # ─────────────────────────────────────────────────────────
    logger.info("PHASE 4: Ensemble Training")
    pipeline = build_ensemble_pipeline()
    
    logger.info("Fitting Pipeline (StandardScaler -> TF-IDF -> Soft Voting Ensemble)...")
    pipeline.fit(X_train, y_train)
    logger.info("Training complete.")

    # ─────────────────────────────────────────────────────────
    # 5. Evaluation
    # ─────────────────────────────────────────────────────────
    logger.info("PHASE 5: Evaluation")
    
    # Predict classes and probabilities
    preds = pipeline.predict(X_test)
    probs = pipeline.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, preds)
    logger.info(f"Test Accuracy: {acc * 100:.2f}%")
    
    report_str = classification_report(y_test, preds, digits=4)
    print("\n" + "="*40)
    print("CLASSIFICATION REPORT")
    print("="*40)
    print(report_str)
    
    # Generate Charts
    run_full_evaluation(y_test, preds, probs, pipeline)

    # ─────────────────────────────────────────────────────────
    # 6. Persistence
    # ─────────────────────────────────────────────────────────
    logger.info("PHASE 6: Saving Production Assets")
    
    model_path = save_model(pipeline, 'ui_critic_ensemble.pkl')
    
    # Extract classification report as dict for JSON
    report_dict = classification_report(y_test, preds, output_dict=True)
    
    metrics = {
        'accuracy': acc,
        'precision': report_dict['1']['precision'],
        'recall': report_dict['1']['recall'],
        'f1_score': report_dict['1']['f1-score'],
    }
    
    save_training_report(metrics, {'ensemble_type': 'soft_voting'}, 'ui_critic')
    
    total_time = time.time() - start_time
    print("\n" + "="*60)
    print(f"✅ PIPELINE COMPLETE IN {total_time:.2f} SECONDS")
    print(f"Model saved to: {model_path}")
    print("Evaluation charts saved to the /reports/ directory.")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
