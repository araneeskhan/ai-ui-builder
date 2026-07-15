"""
Utility functions for the UI Critic ML Pipeline.
Provides logging, timing decorators, and file management helpers.
"""
import os
import time
import json
import functools
import logging
from datetime import datetime
from config import REPORTS_DIR

# ─────────────────────────────────────────────────────────
# Logging Setup
# ─────────────────────────────────────────────────────────
def get_logger(name: str, level=logging.INFO) -> logging.Logger:
    """Creates a named logger with both console and file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt='%(asctime)s | %(name)-18s | %(levelname)-7s | %(message)s',
        datefmt='%H:%M:%S'
    )

    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File handler
    log_path = os.path.join(REPORTS_DIR, f'{name}.log')
    fh = logging.FileHandler(log_path, mode='a', encoding='utf-8')
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


# ─────────────────────────────────────────────────────────
# Decorators
# ─────────────────────────────────────────────────────────
def timed(func):
    """Decorator that logs the execution time of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger('timer')
        logger.info(f'Starting: {func.__name__}')
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f'Finished: {func.__name__} in {elapsed:.3f}s')
        return result
    return wrapper


# ─────────────────────────────────────────────────────────
# Report Generation
# ─────────────────────────────────────────────────────────
def save_training_report(metrics: dict, params: dict, model_name: str):
    """Saves a JSON report of training results for reproducibility."""
    report = {
        'timestamp': datetime.now().isoformat(),
        'model_name': model_name,
        'best_params': params,
        'metrics': metrics,
    }

    report_path = os.path.join(REPORTS_DIR, f'training_report_{model_name}.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)

    logger = get_logger('reports')
    logger.info(f'Training report saved to: {report_path}')
    return report_path


def load_latest_report(model_name: str) -> dict:
    """Loads the latest training report for a given model."""
    report_path = os.path.join(REPORTS_DIR, f'training_report_{model_name}.json')
    if not os.path.exists(report_path):
        return {}
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ─────────────────────────────────────────────────────────
# Data Helpers
# ─────────────────────────────────────────────────────────
def ensure_directory(path: str):
    """Creates a directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def get_file_size_mb(path: str) -> float:
    """Returns the size of a file in megabytes."""
    if os.path.exists(path):
        return os.path.getsize(path) / (1024 * 1024)
    return 0.0
