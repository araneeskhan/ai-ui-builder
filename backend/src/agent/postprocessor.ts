/**
 * Post-Processor: Deterministic Code Transforms
 * 
 * After the AI generates HTML, this module runs a series of
 * rule-based transforms to fix common mistakes and upgrade
 * the visual quality — things the tiny model consistently gets wrong.
 */

/**
 * Run all post-processing passes on the generated HTML.
 */
export function postProcess(html: string): string {
  let result = html;

  result = removeWrappingTags(result);
  result = fixBrokenImages(result);
  result = upgradeColors(result);
  result = ensureTransitions(result);
  result = fixUnclosedTags(result);
  result = injectFontSmoothing(result);

  return result.trim();
}

/**
 * Remove <html>, <head>, <body>, <style>, <script> tags that the model
 * sometimes hallucinates even when told not to.
 */
function removeWrappingTags(html: string): string {
  return html
    .replace(/<\/?html[^>]*>/gi, '')
    .replace(/<\/?head[^>]*>/gi, '')
    .replace(/<\/?body[^>]*>/gi, '')
    .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
    .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
    .replace(/<link[^>]*>/gi, '')
    .replace(/<meta[^>]*>/gi, '')
    .replace(/<!DOCTYPE[^>]*>/gi, '')
    .trim();
}

/**
 * Replace <img> tags (which always break since there are no real images)
 * with FontAwesome placeholder icons inside styled containers.
 */
function fixBrokenImages(html: string): string {
  // Replace standalone img tags with a nice icon placeholder
  return html.replace(
    /<img[^>]*>/gi,
    '<div class="w-full h-32 rounded-lg bg-zinc-800 flex items-center justify-center text-zinc-600"><i class="fas fa-image text-2xl"></i></div>'
  );
}

/**
 * Upgrade generic/ugly default colors to a refined zinc-based palette.
 * Small models love using bg-gray-*, bg-blue-500, etc.
 */
function upgradeColors(html: string): string {
  return html
    // Gray → Zinc (more premium)
    .replace(/\bbg-gray-(\d+)\b/g, 'bg-zinc-$1')
    .replace(/\btext-gray-(\d+)\b/g, 'text-zinc-$1')
    .replace(/\bborder-gray-(\d+)\b/g, 'border-zinc-$1')
    // Harsh pure black/white backgrounds → zinc tones
    .replace(/\bbg-black\b/g, 'bg-zinc-950')
    .replace(/\bbg-white\b(?!\/)/g, 'bg-zinc-50')
    // Upgrade common harsh button colors to softer versions
    .replace(/\bbg-blue-500\b/g, 'bg-indigo-600')
    .replace(/\bbg-blue-600\b/g, 'bg-indigo-600')
    .replace(/\bbg-blue-700\b/g, 'bg-indigo-700')
    .replace(/\bhover:bg-blue-600\b/g, 'hover:bg-indigo-500')
    .replace(/\bhover:bg-blue-700\b/g, 'hover:bg-indigo-600')
    // Green checkmarks → emerald
    .replace(/\btext-green-(\d+)\b/g, 'text-emerald-$1');
}

/**
 * Add transition-colors to interactive elements that are missing it.
 */
function ensureTransitions(html: string): string {
  // Add transitions to buttons and links that don't have them
  return html.replace(
    /(<(?:button|a)\s[^>]*class="[^"]*)(")(?![^>]*transition)/gi,
    '$1 transition-colors$2'
  );
}

/**
 * Fix common unclosed tags that tiny models produce.
 */
function fixUnclosedTags(html: string): string {
  // Count opening vs closing divs and add missing closers
  const openDivs = (html.match(/<div[\s>]/gi) || []).length;
  const closeDivs = (html.match(/<\/div>/gi) || []).length;
  const missing = openDivs - closeDivs;

  if (missing > 0) {
    html += '\n</div>'.repeat(missing);
  }

  return html;
}

/**
 * Wrap the component in a container that ensures font-smoothing
 * if the model forgot to add it.
 */
function injectFontSmoothing(html: string): string {
  // If the outermost element doesn't have antialiased class, wrap it
  if (!html.includes('antialiased')) {
    return `<div class="antialiased">${html}</div>`;
  }
  return html;
}
