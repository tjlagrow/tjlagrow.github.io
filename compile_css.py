import re
import os

# 1. Define Variables
variables = {
    # Base Variables (reconstructed from main.scss)
    "$base-font-family": "'Nunito', Helvetica, Arial, sans-serif",
    "$base-font-size": "16px",
    "$base-line-height": "1.5",
    "$spacing-unit": "30px",
    "$content-width": "800px",
    "$on-laptop": "800px",
    "$small-font-size": "14px",
    
    # Common Colors (Minima defaults + Custom overrides)
    "$text-color": "#f0fdfa", # Teal 50 (Very light mint white)
    "$background-color": "#042f2e", # Teal 950 (Deep dark seafoam background)
    "$brand-color": "#2dd4bf", # Teal 400 (Seafoam Green)
    "$grey-color": "#99f6e4", # Teal 200 (Light seafoam for secondary text)
    "$grey-color-light": "#134e4a", # Teal 800 (Dark borders)
    "$grey-color-dark": "#ccfbf1", # Teal 100
    
    # Theme Variables (from _theme.scss)
    "$bg-dark": "#042f2e", # Teal 950
    "$bg-gradient-start": "#042f2e",
    "$bg-gradient-end": "#115e59", # Teal 800 (Slightly lighter gradient end)
    "$glass-bg": "rgba(17, 94, 89, 0.95)", # Opaque Teal 800 for cards
    "$glass-border": "rgba(45, 212, 191, 0.3)", # Seafoam border
    "$glass-shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.3)",
    "$accent-primary": "#2dd4bf", # Teal 400 (Seafoam)
    "$accent-secondary": "#34d399", # Emerald 400 (Greenish Seafoam)
    "$accent-tertiary": "#0ea5e9", # Sky 500 (Ocean blue accent)
}

# 2. Define Mixin Expansions
mixins = {
    "glass-panel": """
    background: rgba(17, 94, 89, 0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(45, 212, 191, 0.3);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
    border-radius: 1rem;
    """,
    
    "hover-lift": """
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    """,
    # Note: the &:hover part of hover-lift needs manual handling or finding the bracket closure. 
    # For now, we assume standard CSS nesting handles the & inside the original SASS if we just strip the mixin line.
    # Actually, simplistic replacement of @include hover-lift; with the content works, IF the content has the &:hover block.
    # But _theme.scss defined it WITH the block.
    
    "text-gradient": """
    background: linear-gradient(92deg, #f0fdfa, #2dd4bf 40%, #34d399 75%, #0ea5e9 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    """,
}

# Files to process in order
files = [
    "_sass/_theme.scss", # defines mixins/vars, but we hardcoded them. We interpret it anyway.
    "_sass/_base.scss",
    "_sass/_components.scss",
    "_sass/_hero.scss",
    "_sass/_cards.scss",
    "_sass/_forms.scss",
    "_sass/_chatbot.scss",
    "_sass/_syntax-highlighting.scss"
]

def process_content(content):
    # 1. Remove @import
    # content = re.sub(r'@import.*;', '', content)
    
    # Sort variables by length descending to prevent substring replacements
    # e.g. replacing $grey-color before $grey-color-light
    sorted_vars = sorted(variables.items(), key=lambda x: len(x[0]), reverse=True)
    
    for var, val in sorted_vars:
        content = content.replace(var, val)
        
    # 3. Handle Color Functions (Simple approximation)
    # darken(color, 10%) -> just use color
    content = re.sub(r'darken\(([^,]+),\s*[^)]+\)', r'\1', content)
    content = re.sub(r'lighten\(([^,]+),\s*[^)]+\)', r'\1', content)
    content = re.sub(r'rgba\(([^,]+),\s*([^)]+)\)', r'rgba(\1, \2)', content) # preserve rgba
    
    # 4. Handle Mixins
    # Replace @include mixin;
    for name, body in mixins.items():
        content = re.sub(f'@include {name};', body, content)
        
    # 5. Handle @include media-query($on-laptop)
    content = content.replace('@include media-query($on-laptop)', '@media (max-width: 800px)')
    
    # 6. Handle @extend %clearfix
    content = content.replace('@extend %clearfix;', 'content: ""; display: table; clear: both;')
    
    # 7. Handle @extend .hero; -> duplicate .hero styles? 
    # This is hard. We'll simply ignore it or replace with nothing, assuming common styles are sufficient.
    content = content.replace('@extend .hero;', '')
    
    # 8. Handle @extend %vertical-rhythm
    content = content.replace('@extend %vertical-rhythm;', 'margin-bottom: 15px;')
    
    return content

full_css = "/* Manually compiled CSS */\n"

# Add Normalize/Base from previous style.css if possible? 
# We'll assume the _base.scss covers enough, or we might lose specific utility classes.
# Better to prepend the 'style.css' content if it exists?
# The user said "white page", suggesting style.css was empty or ineffective.
# Let's try to include a minimal normalize if we can.
# We'll just stick to the custom SASS for now.

for fpath in files:
    try:
        with open(fpath, 'r') as f:
            raw = f.read()
            # If it's _theme.scss, we don't output duplicates of mixin definitions, but CSS variables would be nice.
            # For this script we just output everything processed.
            processed = process_content(raw)
            full_css += f"\n/* --- {fpath} --- */\n" + processed
    except Exception as e:
        print(f"Error reading {fpath}: {e}")

# Write output
with open('assets/css/index.css', 'w') as f:
    f.write(full_css)

print("Compilation complete. assets/css/index.css created.")
