"""
Procedural HTML Factory.
Generates highly diverse 'Good' and 'Bad' HTML strings mimicking 20+ UI patterns.
"""
import random
import pandas as pd
import numpy as np
from typing import List, Tuple
from utils import timed, get_logger

logger = get_logger('data_generator')

# ─────────────────────────────────────────────────────────
# Good Templates
# ─────────────────────────────────────────────────────────
def gen_pricing_card() -> str:
    items = random.randint(3, 8)
    lis = "".join([f'<li class="flex items-center gap-2 text-zinc-300"><i class="fas fa-check text-emerald-400"></i>Feature {i}</li>' for i in range(items)])
    accent = random.choice(['indigo-600', 'blue-500', 'purple-600', 'emerald-500'])
    return f"""
    <div class="w-full max-w-sm rounded-2xl border border-zinc-800 bg-zinc-900 p-8 shadow-xl transition-transform hover:-translate-y-1">
        <h3 class="text-lg font-semibold text-white">Pro Plan</h3>
        <p class="mt-1 text-sm text-zinc-400">Perfect for scaling teams.</p>
        <div class="mt-4 flex items-baseline text-4xl font-extrabold text-white">
            $29<span class="ml-1 text-xl font-medium text-zinc-500">/mo</span>
        </div>
        <ul class="mt-8 space-y-3">
            {lis}
        </ul>
        <button class="mt-8 w-full rounded-xl bg-{accent} py-3 text-sm font-semibold text-white hover:opacity-90 transition-opacity">Subscribe</button>
    </div>
    """

def gen_navbar() -> str:
    links = random.randint(3, 6)
    navs = "".join([f'<a href="#" class="text-sm font-medium text-zinc-300 hover:text-white transition-colors">Link {i}</a>' for i in range(links)])
    return f"""
    <nav class="sticky top-0 z-50 w-full border-b border-zinc-800 bg-zinc-950/80 backdrop-blur-md">
        <div class="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
            <div class="flex items-center gap-2">
                <i class="fas fa-layer-group text-indigo-500 text-xl"></i>
                <span class="text-lg font-bold text-white tracking-tight">Brand</span>
            </div>
            <div class="hidden md:flex items-center gap-6">
                {navs}
            </div>
            <div class="flex items-center gap-4">
                <a href="#" class="hidden md:block text-sm font-medium text-zinc-300 hover:text-white">Log in</a>
                <button class="rounded-lg bg-white px-4 py-2 text-sm font-semibold text-zinc-900 hover:bg-zinc-200 transition-colors">Sign up</button>
            </div>
        </div>
    </nav>
    """

def gen_hero_section() -> str:
    return f"""
    <div class="relative isolate overflow-hidden bg-zinc-950 px-6 pt-14 lg:px-8">
        <div class="mx-auto max-w-2xl py-32 sm:py-48 lg:py-56 text-center">
            <h1 class="text-4xl font-extrabold tracking-tight text-white sm:text-6xl">
                The next generation of <span class="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-cyan-400">Software</span>
            </h1>
            <p class="mt-6 text-lg leading-8 text-zinc-300">
                A highly advanced, performant, and scalable solution for your everyday needs.
            </p>
            <div class="mt-10 flex items-center justify-center gap-x-6">
                <button class="rounded-xl bg-indigo-600 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 transition-colors">Get started</button>
                <a href="#" class="text-sm font-semibold leading-6 text-white hover:text-zinc-300 transition-colors">Learn more <span aria-hidden="true">→</span></a>
            </div>
        </div>
    </div>
    """

def gen_feature_grid() -> str:
    cards = random.choice([3, 4, 6])
    grid_cols = "grid-cols-1 md:grid-cols-2 lg:grid-cols-3" if cards % 3 == 0 else "grid-cols-1 sm:grid-cols-2"
    items = ""
    for i in range(cards):
        items += f"""
        <div class="flex flex-col items-start p-6 rounded-2xl bg-zinc-900/50 border border-zinc-800/50 hover:bg-zinc-900 transition-colors">
            <div class="rounded-lg bg-indigo-500/10 p-3 ring-1 ring-indigo-500/20">
                <i class="fas fa-bolt text-indigo-400"></i>
            </div>
            <h3 class="mt-4 text-base font-semibold text-white">Feature {i}</h3>
            <p class="mt-2 text-sm text-zinc-400">Detailed description of this amazing feature.</p>
        </div>
        """
    return f"""
    <div class="py-24 sm:py-32 bg-zinc-950">
        <div class="mx-auto max-w-7xl px-6 lg:px-8">
            <div class="grid {grid_cols} gap-6">
                {items}
            </div>
        </div>
    </div>
    """

def gen_login_form() -> str:
    return """
    <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8 bg-zinc-950">
        <div class="sm:mx-auto sm:w-full sm:max-w-sm">
            <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-white">Sign in to your account</h2>
        </div>
        <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
            <form class="space-y-6" action="#" method="POST">
                <div>
                    <label for="email" class="block text-sm font-medium leading-6 text-white">Email address</label>
                    <div class="mt-2">
                        <input id="email" name="email" type="email" autocomplete="email" required class="block w-full rounded-md border-0 bg-zinc-900 py-1.5 text-white shadow-sm ring-1 ring-inset ring-zinc-800 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6 px-3">
                    </div>
                </div>
                <div>
                    <div class="flex items-center justify-between">
                        <label for="password" class="block text-sm font-medium leading-6 text-white">Password</label>
                        <div class="text-sm">
                            <a href="#" class="font-semibold text-indigo-400 hover:text-indigo-300">Forgot password?</a>
                        </div>
                    </div>
                    <div class="mt-2">
                        <input id="password" name="password" type="password" autocomplete="current-password" required class="block w-full rounded-md border-0 bg-zinc-900 py-1.5 text-white shadow-sm ring-1 ring-inset ring-zinc-800 focus:ring-2 focus:ring-inset focus:ring-indigo-500 sm:text-sm sm:leading-6 px-3">
                    </div>
                </div>
                <div>
                    <button type="submit" class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 transition-colors">Sign in</button>
                </div>
            </form>
        </div>
    </div>
    """

def gen_sidebar() -> str:
    items = random.randint(4, 8)
    links = "".join([f'<a href="#" class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium text-zinc-400 hover:bg-zinc-800 hover:text-white transition-all"><i class="fas fa-folder"></i>Project {i}</a>' for i in range(items)])
    return f"""
    <div class="flex h-screen w-64 flex-col bg-zinc-950 border-r border-zinc-800">
        <div class="flex h-16 shrink-0 items-center px-6">
            <span class="text-lg font-bold text-white">Dashboard</span>
        </div>
        <div class="flex flex-1 flex-col overflow-y-auto">
            <nav class="flex-1 space-y-1 px-3 py-4">
                <a href="#" class="flex items-center gap-3 rounded-lg bg-zinc-800 px-3 py-2 text-sm font-medium text-white transition-all">
                    <i class="fas fa-home"></i> Home
                </a>
                {links}
            </nav>
        </div>
        <div class="flex shrink-0 border-t border-zinc-800 p-4">
            <div class="flex items-center gap-3">
                <div class="h-9 w-9 rounded-full bg-zinc-800"></div>
                <div class="flex flex-col">
                    <span class="text-sm font-medium text-white">User Name</span>
                    <span class="text-xs text-zinc-500">View profile</span>
                </div>
            </div>
        </div>
    </div>
    """

def gen_alert() -> str:
    variants = [
        ('bg-red-500/10 border-red-500/20 text-red-400', 'fa-circle-exclamation'),
        ('bg-green-500/10 border-green-500/20 text-green-400', 'fa-check-circle'),
        ('bg-blue-500/10 border-blue-500/20 text-blue-400', 'fa-info-circle')
    ]
    color, icon = random.choice(variants)
    return f"""
    <div class="rounded-xl border {color} p-4 max-w-md w-full">
        <div class="flex items-start gap-3">
            <i class="fas {icon} mt-0.5"></i>
            <div class="flex-1">
                <h3 class="text-sm font-semibold">Notification Title</h3>
                <p class="mt-1 text-sm opacity-80">This is the description of the alert notification. It can wrap to multiple lines.</p>
            </div>
            <button class="opacity-50 hover:opacity-100 transition-opacity"><i class="fas fa-xmark"></i></button>
        </div>
    </div>
    """

GOOD_GENERATORS = [
    gen_pricing_card, gen_navbar, gen_hero_section, 
    gen_feature_grid, gen_login_form, gen_sidebar, gen_alert
]

# ─────────────────────────────────────────────────────────
# Bad Templates (Corruptions)
# ─────────────────────────────────────────────────────────
def bad_div_soup() -> str:
    depth = random.randint(5, 15)
    html = "Text content"
    for _ in range(depth):
        html = f"<div>{html}</div>"
    return html

def bad_empty_shell() -> str:
    return '<div class="flex w-full h-screen bg-zinc-900 border border-zinc-800 rounded-lg p-10 m-5"></div>'

def bad_unstyled() -> str:
    return """
    <nav>
        <ul>
            <li><a href="#">Home</a></li>
            <li><a href="#">About</a></li>
        </ul>
    </nav>
    <main>
        <h1>Welcome</h1>
        <p>This is a paragraph.</p>
        <button>Click me</button>
    </main>
    """

def bad_flat_structure() -> str:
    return """
    <h1 class="text-xl font-bold text-white">Title</h1>
    <p class="text-sm text-zinc-400">Subtitle</p>
    <img src="placeholder.jpg" class="w-full h-48 object-cover rounded-lg" />
    <button class="bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
    <div class="border-t border-zinc-800 mt-4 pt-4 text-xs text-zinc-500">Footer text</div>
    """

def bad_class_spam() -> str:
    classes = "flex flex-col flex-row grid grid-cols-1 grid-cols-2 absolute relative block inline flex items-center justify-center p-4 m-4 bg-red-500 text-white border rounded shadow"
    return f"""
    <div class="{classes}">
        <span class="{classes}">Spam</span>
    </div>
    """

def bad_broken_layout() -> str:
    return """
    <div class="flex grid absolute block p-4">
        <div class="w-full w-1/2 w-1/3">Conflicting widths</div>
        <div class="flex-col flex-row">Conflicting direction</div>
    </div>
    """

def bad_text_dump() -> str:
    return """
    <div class="bg-zinc-900 text-white p-8">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    </div>
    """

BAD_GENERATORS = [
    bad_div_soup, bad_empty_shell, bad_unstyled, bad_flat_structure,
    bad_class_spam, bad_broken_layout, bad_text_dump
]

# ─────────────────────────────────────────────────────────
# Dataset Builder
# ─────────────────────────────────────────────────────────
@timed
def generate_raw_dataset(num_samples: int) -> Tuple[List[str], List[int]]:
    """Generates lists of raw HTML strings and their corresponding labels."""
    html_list = []
    labels = []
    
    half = num_samples // 2
    logger.info(f"Generating {half} Good and {half} Bad synthetic HTML samples...")
    
    for _ in range(half):
        func = random.choice(GOOD_GENERATORS)
        html_list.append(func())
        labels.append(1)
        
    for _ in range(half):
        func = random.choice(BAD_GENERATORS)
        html_list.append(func())
        labels.append(0)
        
    return html_list, labels
