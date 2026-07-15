"""
Advanced Feature Extraction Module.
Extracts 30 numerical features and 1 NLP corpus from raw HTML.
"""
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from typing import Dict, Any, List
from config import (
    LAYOUT_CLASSES, TYPOGRAPHY_CLASSES, SEMANTIC_TAGS, INTERACTIVE_TAGS,
    ALL_FEATURES
)
from utils import timed, get_logger

logger = get_logger('features')

def extract_features(html: str) -> Dict[str, Any]:
    """Extracts a feature dictionary from a single HTML string."""
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(True)
    
    num_tags = len(tags)
    
    # Base fallback for completely empty strings
    if num_tags == 0:
        return {f: 0 for f in ALL_FEATURES if f != 'class_text'} | {'class_text': ''}

    # ─────────────────────────────────────────────────────────
    # A. Structural Metrics
    # ─────────────────────────────────────────────────────────
    depths = [len(list(tag.parents)) for tag in tags]
    max_depth = max(depths)
    avg_depth = sum(depths) / num_tags
    nesting_variance = np.var(depths) if len(depths) > 1 else 0

    sibling_counts = []
    for tag in tags:
        if tag.parent:
            # Count elements that are direct children of the same parent
            sibling_counts.append(len([c for c in tag.parent.children if c.name]))
    
    max_siblings = max(sibling_counts) if sibling_counts else 0
    avg_siblings = sum(sibling_counts) / len(sibling_counts) if sibling_counts else 0
    
    unique_tags = len(set(tag.name for tag in tags))
    tag_diversity = unique_tags / num_tags

    # ─────────────────────────────────────────────────────────
    # B. Semantic Quality
    # ─────────────────────────────────────────────────────────
    semantic_count = sum(1 for tag in tags if tag.name in SEMANTIC_TAGS)
    div_count = sum(1 for tag in tags if tag.name == 'div')
    interactive_count = sum(1 for tag in tags if tag.name in INTERACTIVE_TAGS)
    heading_count = sum(1 for tag in tags if tag.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    list_item_count = sum(1 for tag in tags if tag.name == 'li')

    semantic_ratio = semantic_count / num_tags
    div_ratio = div_count / num_tags

    # ─────────────────────────────────────────────────────────
    # C. & D. & E. Tailwind / CSS Metrics
    # ─────────────────────────────────────────────────────────
    all_classes = []
    layout_count = 0
    color_count = 0
    spacing_count = 0
    typography_count = 0
    border_count = 0
    responsive_count = 0
    hover_count = 0
    transition_count = 0

    for tag in tags:
        cls_list = tag.get('class', [])
        all_classes.extend(cls_list)
        
        for c in cls_list:
            if c in LAYOUT_CLASSES: layout_count += 1
            if c.startswith('bg-') or c.startswith('text-'): color_count += 1
            if c.startswith('p-') or c.startswith('m-') or c.startswith('px-') or c.startswith('py-') or c.startswith('gap-'): spacing_count += 1
            if c in TYPOGRAPHY_CLASSES: typography_count += 1
            if c.startswith('rounded') or c.startswith('border'): border_count += 1
            if c.startswith('sm:') or c.startswith('md:') or c.startswith('lg:') or c.startswith('xl:'): responsive_count += 1
            if c.startswith('hover:'): hover_count += 1
            if c.startswith('transition') or c.startswith('duration'): transition_count += 1

    total_class_count = len(all_classes)
    unique_class_count = len(set(all_classes))
    avg_classes_per_tag = total_class_count / num_tags
    tailwind_density = total_class_count / num_tags
    layout_cohesion = layout_count / num_tags
    visual_richness = (color_count + spacing_count + typography_count + border_count) / num_tags

    # ─────────────────────────────────────────────────────────
    # F. Content Metrics
    # ─────────────────────────────────────────────────────────
    empty_tags = sum(1 for tag in tags if not tag.text.strip() and not tag.find_all())
    empty_ratio = empty_tags / num_tags
    
    text_content_length = len(soup.get_text(strip=True))
    icon_count = sum(1 for tag in tags if tag.name in ['i', 'svg'])
    
    # Heuristic: does the root/body have a wrapping container?
    has_container = 0
    root_divs = [t for t in tags if t.name == 'div' and len(list(t.parents)) <= 2]
    for rd in root_divs:
        c = rd.get('class', [])
        if any(x.startswith('max-w-') for x in c) or 'container' in c:
            has_container = 1
            break

    # ─────────────────────────────────────────────────────────
    # G. NLP Feature
    # ─────────────────────────────────────────────────────────
    class_text = " ".join(all_classes)

    return {
        'num_tags': num_tags,
        'max_depth': max_depth,
        'avg_depth': avg_depth,
        'nesting_variance': nesting_variance,
        'max_siblings': max_siblings,
        'avg_siblings': avg_siblings,
        'tag_diversity': tag_diversity,
        'semantic_ratio': semantic_ratio,
        'div_ratio': div_ratio,
        'interactive_element_count': interactive_count,
        'heading_count': heading_count,
        'list_item_count': list_item_count,
        'total_class_count': total_class_count,
        'unique_class_count': unique_class_count,
        'avg_classes_per_tag': avg_classes_per_tag,
        'tailwind_density': tailwind_density,
        'layout_class_count': layout_count,
        'layout_cohesion': layout_cohesion,
        'color_class_count': color_count,
        'spacing_class_count': spacing_count,
        'visual_richness': visual_richness,
        'typography_class_count': typography_count,
        'border_class_count': border_count,
        'responsive_class_count': responsive_count,
        'hover_class_count': hover_count,
        'transition_class_count': transition_count,
        'empty_ratio': empty_ratio,
        'text_content_length': text_content_length,
        'icon_count': icon_count,
        'has_container_structure': has_container,
        'class_text': class_text
    }

@timed
def extract_features_batch(html_list: List[str]) -> pd.DataFrame:
    """Processes a list of HTML strings and returns a pandas DataFrame."""
    logger.info(f"Extracting 30+ features for {len(html_list)} samples...")
    data = [extract_features(html) for html in html_list]
    df = pd.DataFrame(data)
    
    # Ensure columns match config EXACTLY
    df = df[ALL_FEATURES]
    return df
