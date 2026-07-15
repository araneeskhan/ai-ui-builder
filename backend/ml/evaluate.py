"""
Evaluation Suite.
Generates Confusion Matrix, ROC curves, and Feature Importance charts.
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.pipeline import Pipeline
from config import REPORTS_DIR, NUMERIC_FEATURES
from utils import get_logger, timed

logger = get_logger('evaluate')

# Set standard plotting style
plt.style.use('dark_background')
sns.set_palette("husl")

@timed
def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, model_name='ensemble'):
    """Generates and saves a heatmap of the confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    ax = sns.heatmap(cm, annot=True, fmt='d', cmap='Purples', 
                     xticklabels=['Bad UI (0)', 'Good UI (1)'],
                     yticklabels=['Bad UI (0)', 'Good UI (1)'],
                     cbar=False, annot_kws={"size": 16})
    
    plt.title('Confusion Matrix', fontsize=18, pad=20)
    plt.ylabel('Actual Label', fontsize=14)
    plt.xlabel('Predicted Label', fontsize=14)
    plt.tight_layout()
    
    path = os.path.join(REPORTS_DIR, f'confusion_matrix_{model_name}.png')
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"Confusion matrix saved to {path}")

@timed
def plot_roc_curve(y_true: np.ndarray, y_prob: np.ndarray, model_name='ensemble'):
    """Generates and saves the Receiver Operating Characteristic (ROC) curve."""
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='mediumpurple', lw=2, label=f'ROC curve (AUC = {roc_auc:.3f})')
    plt.plot([0, 1], [0, 1], color='gray', lw=1, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Receiver Operating Characteristic', fontsize=16)
    plt.legend(loc="lower right", fontsize=12)
    
    # Grid lines for easier reading
    plt.grid(True, linestyle=':', alpha=0.3)
    
    path = os.path.join(REPORTS_DIR, f'roc_curve_{model_name}.png')
    plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.close()
    logger.info(f"ROC curve saved to {path}")

@timed
def plot_feature_importance(pipeline: Pipeline, model_name='ensemble'):
    """
    Extracts and plots feature importances from the Random Forest component 
    of the Voting Classifier.
    """
    try:
        # Navigate through the pipeline to get the Random Forest
        # pipeline -> classifier (VotingClassifier) -> estimators_[0] (RandomForest)
        voting_clf = pipeline.named_steps['classifier']
        rf_model = voting_clf.estimators_[0] 
        importances = rf_model.feature_importances_
        
        # Sort features by importance
        indices = np.argsort(importances)[::-1]
        
        # Top 15 features for clarity
        top_k = min(15, len(NUMERIC_FEATURES))
        top_indices = indices[:top_k]
        top_features = [NUMERIC_FEATURES[i] for i in top_indices]
        top_importances = importances[top_indices]
        
        plt.figure(figsize=(10, 8))
        sns.barplot(x=top_importances, y=top_features, palette="Purples_r")
        plt.title('Top 15 Structural Feature Importances (Random Forest)', fontsize=16)
        plt.xlabel('Gini Importance', fontsize=12)
        plt.tight_layout()
        
        path = os.path.join(REPORTS_DIR, f'feature_importance_{model_name}.png')
        plt.savefig(path, dpi=300, bbox_inches='tight')
        plt.close()
        logger.info(f"Feature importance chart saved to {path}")
        
    except Exception as e:
        logger.warning(f"Could not extract feature importance: {e}")

def run_full_evaluation(y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray, pipeline: Pipeline):
    """Executes the full suite of evaluation plots."""
    logger.info("Running evaluation suite...")
    plot_confusion_matrix(y_true, y_pred)
    plot_roc_curve(y_true, y_prob)
    plot_feature_importance(pipeline)
