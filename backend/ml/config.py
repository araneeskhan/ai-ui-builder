"""
Configuration module for the UI Critic ML Pipeline.
Centralizes all hyperparameters, paths, and feature definitions.
"""
import os

# ─────────────────────────────────────────────────────────
# Paths
# ─────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARTIFACTS_DIR = os.path.join(BASE_DIR, 'artifacts')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

# Ensure directories exist at import time
for d in [ARTIFACTS_DIR, MODELS_DIR, DATA_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)

# ─────────────────────────────────────────────────────────
# Data Generation
# ─────────────────────────────────────────────────────────
NUM_SAMPLES = 3000          # Total samples to generate (50/50 split)
RANDOM_SEED = 42            # Reproducibility seed
TRAIN_TEST_SPLIT = 0.20     # 20% held out for testing
VALIDATION_SPLIT = 0.15     # 15% of training data for validation during tuning

# ─────────────────────────────────────────────────────────
# Feature Engineering
# ─────────────────────────────────────────────────────────
NUMERIC_FEATURES = [
    'num_tags',
    'max_depth',
    'avg_depth',
    'semantic_ratio',
    'div_ratio',
    'tailwind_density',
    'layout_class_count',
    'layout_cohesion',
    'color_class_count',
    'spacing_class_count',
    'visual_richness',
    'typography_class_count',
    'border_class_count',
    'responsive_class_count',
    'hover_class_count',
    'transition_class_count',
    'empty_ratio',
    'text_content_length',
    'avg_classes_per_tag',
    'unique_class_count',
    'total_class_count',
    'tag_diversity',
    'interactive_element_count',
    'heading_count',
    'list_item_count',
    'nesting_variance',
    'max_siblings',
    'avg_siblings',
    'icon_count',
    'has_container_structure',
]

TEXT_FEATURE = 'class_text'

ALL_FEATURES = NUMERIC_FEATURES + [TEXT_FEATURE]

# ─────────────────────────────────────────────────────────
# Tailwind Class Categories (for feature extraction)
# ─────────────────────────────────────────────────────────
LAYOUT_CLASSES = frozenset([
    'flex', 'grid', 'inline-flex', 'inline-grid', 'block', 'inline-block',
    'absolute', 'relative', 'fixed', 'sticky',
    'items-center', 'items-start', 'items-end', 'items-stretch',
    'justify-center', 'justify-between', 'justify-around', 'justify-end', 'justify-start',
    'flex-col', 'flex-row', 'flex-wrap',
    'col-span-1', 'col-span-2', 'col-span-3', 'col-span-4',
    'grid-cols-1', 'grid-cols-2', 'grid-cols-3', 'grid-cols-4',
])

TYPOGRAPHY_CLASSES = frozenset([
    'font-bold', 'font-semibold', 'font-medium', 'font-light', 'font-normal',
    'text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl', 'text-3xl', 'text-4xl',
    'tracking-tight', 'tracking-wide', 'leading-tight', 'leading-relaxed', 'leading-snug',
    'uppercase', 'lowercase', 'capitalize', 'truncate',
    'line-clamp-1', 'line-clamp-2', 'line-clamp-3',
])

SEMANTIC_TAGS = frozenset([
    'nav', 'main', 'section', 'article', 'aside', 'footer', 'header',
    'button', 'a', 'input', 'select', 'textarea', 'label', 'form',
    'ul', 'ol', 'li', 'dl', 'dt', 'dd',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'span', 'strong', 'em', 'small',
    'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'figure', 'figcaption', 'blockquote', 'code', 'pre',
])

INTERACTIVE_TAGS = frozenset(['button', 'a', 'input', 'select', 'textarea'])

# ─────────────────────────────────────────────────────────
# Model Hyperparameters (GridSearchCV spaces)
# ─────────────────────────────────────────────────────────
RF_PARAM_GRID = {
    'n_estimators': [50, 100, 200],
    'max_depth': [3, 5, 10, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

LR_PARAM_GRID = {
    'C': [0.01, 0.1, 1, 10],
    'max_iter': [1000],
}

TFIDF_MAX_FEATURES = 500
TFIDF_NGRAM_RANGE = (1, 2)  # Unigrams and bigrams for class combinations

# ─────────────────────────────────────────────────────────
# Evaluation Thresholds
# ─────────────────────────────────────────────────────────
QUALITY_THRESHOLD = 0.55    # Probability threshold above which a UI is "approved"
MIN_ACCEPTABLE_F1 = 0.85    # Pipeline warns if F1 drops below this
