from bs4 import BeautifulSoup

def extract_advanced_features(html: str):
    """
    Extracts both numeric structural features AND semantic text features (class names).
    Returns a dictionary so pandas can easily map it to columns.
    """
    soup = BeautifulSoup(html, 'html.parser')
    tags = soup.find_all(True)
    
    num_tags = len(tags)
    if num_tags == 0:
        return {
            'num_tags': 0, 'max_depth': 0, 'semantic_ratio': 0, 
            'tailwind_density': 0, 'layout_cohesion': 0, 
            'visual_richness': 0, 'empty_ratio': 0, 'class_text': ""
        }
        
    depths = [len(list(tag.parents)) for tag in tags]
    max_depth = max(depths) if depths else 0
    
    semantic_tags = ['nav', 'main', 'section', 'button', 'ul', 'li', 'header', 'footer', 'h1', 'h2', 'h3', 'p', 'span', 'a']
    semantic_count = sum(1 for tag in tags if tag.name in semantic_tags)
    semantic_ratio = semantic_count / num_tags
    
    classes = []
    layout_count = 0
    color_count = 0
    spacing_count = 0
    
    for tag in tags:
        tag_classes = tag.get('class', [])
        classes.extend(tag_classes)
        for c in tag_classes:
            if c in ['flex', 'grid', 'absolute', 'relative', 'block']:
                layout_count += 1
            if c.startswith('bg-') or c.startswith('text-') or c.startswith('border-'):
                color_count += 1
            if c.startswith('p-') or c.startswith('m-') or c.startswith('px-') or c.startswith('py-'):
                spacing_count += 1

    tailwind_density = len(classes) / num_tags if num_tags > 0 else 0
    layout_cohesion = layout_count / num_tags
    visual_richness = (color_count + spacing_count) / num_tags
    
    empty_tags = sum(1 for tag in tags if not tag.text.strip() and not tag.find_all())
    empty_ratio = empty_tags / num_tags

    # The Semantic NLP Corpus: all CSS classes joined as a space-separated string
    class_text = " ".join(classes)

    return {
        'num_tags': num_tags,
        'max_depth': max_depth,
        'semantic_ratio': semantic_ratio,
        'tailwind_density': tailwind_density,
        'layout_cohesion': layout_cohesion,
        'visual_richness': visual_richness,
        'empty_ratio': empty_ratio,
        'class_text': class_text
    }

NUMERIC_FEATURES = [
    'num_tags', 
    'max_depth', 
    'semantic_ratio', 
    'tailwind_density', 
    'layout_cohesion', 
    'visual_richness', 
    'empty_ratio'
]
TEXT_FEATURE = 'class_text'
