/**
 * Component Scaffolds & Few-Shot Examples
 * 
 * Instead of asking a tiny 1.5B model to invent beautiful UI from nothing,
 * we detect the component type from the user's prompt and provide:
 * 1. A structural skeleton the model fills in
 * 2. A high-quality example it can pattern-match against
 */

export interface ComponentScaffold {
  type: string;
  keywords: string[];
  skeleton: string;
  example: string;
  tips: string;
}

export const SCAFFOLDS: ComponentScaffold[] = [
  {
    type: 'pricing-card',
    keywords: ['pricing', 'plan', 'subscribe', 'subscription', 'price', 'tier', 'premium', 'pro plan', 'monthly', 'yearly'],
    tips: 'Use a subtle ring/border highlight for the recommended plan. Use a badge for "Popular". Use font-semibold for the price.',
    skeleton: `<div class="w-full max-w-sm rounded-2xl border border-zinc-800 bg-zinc-900 p-8">
  <!-- Badge (optional) -->
  <div class="mb-4"><span class="rounded-full bg-indigo-500/10 px-3 py-1 text-xs font-semibold text-indigo-400">BADGE_TEXT</span></div>
  <!-- Plan name -->
  <h3 class="text-lg font-semibold text-white">PLAN_NAME</h3>
  <p class="mt-1 text-sm text-zinc-400">PLAN_DESCRIPTION</p>
  <!-- Price -->
  <div class="mt-6 flex items-baseline gap-1">
    <span class="text-4xl font-bold text-white">PRICE</span>
    <span class="text-sm text-zinc-500">/month</span>
  </div>
  <!-- Features -->
  <ul class="mt-8 space-y-3">
    <li class="flex items-center gap-3 text-sm text-zinc-300"><i class="fas fa-check text-emerald-400 text-xs"></i>FEATURE_1</li>
    <li class="flex items-center gap-3 text-sm text-zinc-300"><i class="fas fa-check text-emerald-400 text-xs"></i>FEATURE_2</li>
    <li class="flex items-center gap-3 text-sm text-zinc-300"><i class="fas fa-check text-emerald-400 text-xs"></i>FEATURE_3</li>
  </ul>
  <!-- CTA -->
  <button class="mt-8 w-full rounded-xl bg-indigo-600 py-3 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors">CTA_TEXT</button>
</div>`,
    example: `<div class="w-full max-w-sm rounded-2xl border border-zinc-800 bg-zinc-900 p-8 relative overflow-hidden">
  <div class="mb-4"><span class="rounded-full bg-violet-500/10 px-3 py-1 text-xs font-semibold text-violet-400">Most Popular</span></div>
  <h3 class="text-lg font-semibold text-white">Pro Plan</h3>
  <p class="mt-1 text-sm text-zinc-400">Everything you need to scale your business.</p>
  <div class="mt-6 flex items-baseline gap-1">
    <span class="text-4xl font-bold text-white">$29</span>
    <span class="text-sm text-zinc-500">/month</span>
  </div>
  <ul class="mt-8 space-y-3">
    <li class="flex items-center gap-3 text-sm text-zinc-300"><i class="fas fa-check text-emerald-400 text-xs"></i>Unlimited projects</li>
    <li class="flex items-center gap-3 text-sm text-zinc-300"><i class="fas fa-check text-emerald-400 text-xs"></i>Priority support</li>
    <li class="flex items-center gap-3 text-sm text-zinc-300"><i class="fas fa-check text-emerald-400 text-xs"></i>Custom integrations</li>
    <li class="flex items-center gap-3 text-sm text-zinc-300"><i class="fas fa-check text-emerald-400 text-xs"></i>Advanced analytics</li>
  </ul>
  <button class="mt-8 w-full rounded-xl bg-violet-600 py-3 text-sm font-semibold text-white hover:bg-violet-500 transition-colors">Get Started</button>
</div>`,
  },
  {
    type: 'navbar',
    keywords: ['navbar', 'nav', 'navigation', 'header', 'menu', 'topbar', 'top bar'],
    tips: 'Keep it horizontal with flexbox. Use font-medium for links. Add a CTA button on the right.',
    skeleton: `<nav class="w-full max-w-5xl mx-auto flex items-center justify-between px-6 py-4 border-b border-zinc-800">
  <div class="flex items-center gap-2">
    <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-sm font-bold">LOGO</div>
    <span class="text-base font-semibold text-white">BRAND_NAME</span>
  </div>
  <div class="flex items-center gap-8">
    <a href="#" class="text-sm font-medium text-zinc-400 hover:text-white transition-colors">LINK_1</a>
    <a href="#" class="text-sm font-medium text-zinc-400 hover:text-white transition-colors">LINK_2</a>
    <a href="#" class="text-sm font-medium text-zinc-400 hover:text-white transition-colors">LINK_3</a>
  </div>
  <button class="rounded-lg bg-white text-zinc-900 px-4 py-2 text-sm font-semibold hover:bg-zinc-200 transition-colors">CTA_TEXT</button>
</nav>`,
    example: `<nav class="w-full max-w-5xl mx-auto flex items-center justify-between px-6 py-4 border-b border-zinc-800/50">
  <div class="flex items-center gap-2.5">
    <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white text-sm font-bold">A</div>
    <span class="text-base font-semibold text-white tracking-tight">Acme Inc</span>
  </div>
  <div class="flex items-center gap-8">
    <a href="#" class="text-sm font-medium text-zinc-400 hover:text-white transition-colors">Products</a>
    <a href="#" class="text-sm font-medium text-zinc-400 hover:text-white transition-colors">Pricing</a>
    <a href="#" class="text-sm font-medium text-zinc-400 hover:text-white transition-colors">Docs</a>
    <a href="#" class="text-sm font-medium text-zinc-400 hover:text-white transition-colors">Blog</a>
  </div>
  <div class="flex items-center gap-3">
    <a href="#" class="text-sm font-medium text-zinc-400 hover:text-white transition-colors">Sign in</a>
    <button class="rounded-lg bg-white text-zinc-900 px-4 py-2 text-sm font-semibold hover:bg-zinc-200 transition-colors">Get Started</button>
  </div>
</nav>`,
  },
  {
    type: 'login-form',
    keywords: ['login', 'sign in', 'signin', 'auth', 'authentication', 'email', 'password', 'form'],
    tips: 'Center the form. Use proper label/input pairs. Add a divider with "or continue with" text.',
    skeleton: `<div class="w-full max-w-sm mx-auto">
  <div class="text-center mb-8">
    <h1 class="text-2xl font-bold text-white">TITLE</h1>
    <p class="mt-2 text-sm text-zinc-400">SUBTITLE</p>
  </div>
  <form class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-zinc-300 mb-1.5">Email</label>
      <input type="email" placeholder="you@example.com" class="w-full h-10 rounded-lg bg-zinc-900 border border-zinc-800 px-3 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:border-zinc-600" />
    </div>
    <div>
      <label class="block text-sm font-medium text-zinc-300 mb-1.5">Password</label>
      <input type="password" placeholder="••••••••" class="w-full h-10 rounded-lg bg-zinc-900 border border-zinc-800 px-3 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:border-zinc-600" />
    </div>
    <button type="submit" class="w-full h-10 rounded-lg bg-indigo-600 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors">CTA_TEXT</button>
  </form>
</div>`,
    example: `<div class="w-full max-w-sm mx-auto">
  <div class="text-center mb-8">
    <h1 class="text-2xl font-bold text-white">Welcome back</h1>
    <p class="mt-2 text-sm text-zinc-400">Sign in to your account to continue</p>
  </div>
  <form class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-zinc-300 mb-1.5">Email</label>
      <input type="email" placeholder="you@example.com" class="w-full h-10 rounded-lg bg-zinc-900 border border-zinc-800 px-3 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:border-zinc-600" />
    </div>
    <div>
      <div class="flex items-center justify-between mb-1.5">
        <label class="text-sm font-medium text-zinc-300">Password</label>
        <a href="#" class="text-xs text-indigo-400 hover:text-indigo-300">Forgot password?</a>
      </div>
      <input type="password" placeholder="••••••••" class="w-full h-10 rounded-lg bg-zinc-900 border border-zinc-800 px-3 text-sm text-white placeholder:text-zinc-600 focus:outline-none focus:border-zinc-600" />
    </div>
    <button type="submit" class="w-full h-10 rounded-lg bg-indigo-600 text-sm font-semibold text-white hover:bg-indigo-500 transition-colors">Sign In</button>
    <div class="flex items-center gap-3 my-2"><div class="flex-1 h-px bg-zinc-800"></div><span class="text-xs text-zinc-600">or</span><div class="flex-1 h-px bg-zinc-800"></div></div>
    <button type="button" class="w-full h-10 rounded-lg bg-zinc-900 border border-zinc-800 text-sm font-medium text-zinc-300 hover:bg-zinc-800 transition-colors flex items-center justify-center gap-2"><i class="fab fa-google text-sm"></i>Continue with Google</button>
  </form>
  <p class="mt-6 text-center text-xs text-zinc-500">Don't have an account? <a href="#" class="text-indigo-400 hover:text-indigo-300">Sign up</a></p>
</div>`,
  },
  {
    type: 'hero-section',
    keywords: ['hero', 'landing', 'homepage', 'headline', 'call to action', 'cta', 'banner', 'above the fold'],
    tips: 'Center text. Use a large bold heading. Two CTA buttons side by side (primary + secondary).',
    skeleton: `<section class="w-full max-w-3xl mx-auto text-center py-20 px-4">
  <div class="mb-6"><span class="rounded-full bg-indigo-500/10 border border-indigo-500/20 px-4 py-1.5 text-xs font-semibold text-indigo-400">BADGE</span></div>
  <h1 class="text-5xl font-bold text-white leading-tight tracking-tight">HEADLINE</h1>
  <p class="mt-6 text-lg text-zinc-400 max-w-xl mx-auto leading-relaxed">SUBTITLE</p>
  <div class="mt-10 flex items-center justify-center gap-4">
    <button class="rounded-xl bg-white text-zinc-900 px-6 py-3 text-sm font-semibold hover:bg-zinc-200 transition-colors">PRIMARY_CTA</button>
    <button class="rounded-xl bg-zinc-900 border border-zinc-800 text-white px-6 py-3 text-sm font-semibold hover:bg-zinc-800 transition-colors">SECONDARY_CTA</button>
  </div>
</section>`,
    example: `<section class="w-full max-w-3xl mx-auto text-center py-20 px-4">
  <div class="mb-6"><span class="rounded-full bg-indigo-500/10 border border-indigo-500/20 px-4 py-1.5 text-xs font-semibold text-indigo-400">Now in Public Beta</span></div>
  <h1 class="text-5xl font-bold text-white leading-tight tracking-tight">Build faster with<br/>intelligent tools</h1>
  <p class="mt-6 text-lg text-zinc-400 max-w-xl mx-auto leading-relaxed">Ship products 10x faster with AI-powered development tools. From idea to production in minutes, not months.</p>
  <div class="mt-10 flex items-center justify-center gap-4">
    <button class="rounded-xl bg-white text-zinc-900 px-6 py-3 text-sm font-semibold hover:bg-zinc-200 transition-colors">Start Building</button>
    <button class="rounded-xl bg-zinc-900 border border-zinc-800 text-white px-6 py-3 text-sm font-semibold hover:bg-zinc-800 transition-colors flex items-center gap-2"><i class="fab fa-github text-sm"></i>View on GitHub</button>
  </div>
</section>`,
  },
  {
    type: 'dashboard-card',
    keywords: ['dashboard', 'stats', 'metric', 'analytics', 'chart', 'kpi', 'overview', 'summary', 'revenue', 'users'],
    tips: 'Use a compact card with a label, big number, and a small percentage badge.',
    skeleton: `<div class="grid grid-cols-3 gap-4 w-full max-w-3xl">
  <div class="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
    <p class="text-xs font-medium text-zinc-500 uppercase tracking-wider">LABEL_1</p>
    <p class="mt-2 text-2xl font-bold text-white">VALUE_1</p>
    <p class="mt-1 text-xs text-emerald-400 font-medium">CHANGE_1</p>
  </div>
  <div class="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
    <p class="text-xs font-medium text-zinc-500 uppercase tracking-wider">LABEL_2</p>
    <p class="mt-2 text-2xl font-bold text-white">VALUE_2</p>
    <p class="mt-1 text-xs text-emerald-400 font-medium">CHANGE_2</p>
  </div>
  <div class="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
    <p class="text-xs font-medium text-zinc-500 uppercase tracking-wider">LABEL_3</p>
    <p class="mt-2 text-2xl font-bold text-white">VALUE_3</p>
    <p class="mt-1 text-xs text-red-400 font-medium">CHANGE_3</p>
  </div>
</div>`,
    example: `<div class="grid grid-cols-3 gap-4 w-full max-w-3xl">
  <div class="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
    <p class="text-xs font-medium text-zinc-500 uppercase tracking-wider">Revenue</p>
    <p class="mt-2 text-2xl font-bold text-white">$45,231</p>
    <p class="mt-1 text-xs text-emerald-400 font-medium flex items-center gap-1"><i class="fas fa-arrow-up text-[10px]"></i>+20.1% from last month</p>
  </div>
  <div class="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
    <p class="text-xs font-medium text-zinc-500 uppercase tracking-wider">Active Users</p>
    <p class="mt-2 text-2xl font-bold text-white">2,350</p>
    <p class="mt-1 text-xs text-emerald-400 font-medium flex items-center gap-1"><i class="fas fa-arrow-up text-[10px]"></i>+15.3% from last month</p>
  </div>
  <div class="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
    <p class="text-xs font-medium text-zinc-500 uppercase tracking-wider">Bounce Rate</p>
    <p class="mt-2 text-2xl font-bold text-white">24.5%</p>
    <p class="mt-1 text-xs text-red-400 font-medium flex items-center gap-1"><i class="fas fa-arrow-down text-[10px]"></i>-4.2% from last month</p>
  </div>
</div>`,
  },
];

/**
 * Detect which scaffold best matches the user's prompt.
 * Returns the scaffold if found, null if no match.
 */
export function detectScaffold(prompt: string): ComponentScaffold | null {
  const lower = prompt.toLowerCase();
  let bestMatch: ComponentScaffold | null = null;
  let bestScore = 0;

  for (const scaffold of SCAFFOLDS) {
    let score = 0;
    for (const keyword of scaffold.keywords) {
      if (lower.includes(keyword)) {
        score += keyword.length; // Longer keyword matches are weighted higher
      }
    }
    if (score > bestScore) {
      bestScore = score;
      bestMatch = scaffold;
    }
  }

  return bestScore > 0 ? bestMatch : null;
}
