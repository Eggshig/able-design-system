
import json
import os

def resolve_alias(value, all_tokens):
    if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
        path = value[1:-1].split('.')
        ref = all_tokens
        for p in path:
            ref = ref.get(p)
            if ref is None:
                return value # Return original alias if not found
        if isinstance(ref, dict) and '$value' in ref:
            return resolve_alias(ref['$value'], all_tokens)
        return ref
    return value

def flatten_dict(d, parent_key='', sep='-'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, dict):
            if '$value' in v:
                items.append((new_key.lower(), v['$value']))
            else:
                items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key.lower(), v))
    return dict(items)

def generate_css_from_tokens(tokens, all_tokens, unit_mappings={}):
    css_vars = {}
    flat_tokens = flatten_dict(tokens)

    for name, value in flat_tokens.items():
        resolved_value = resolve_alias(value, all_tokens)
        unit = ''
        for key, u in unit_mappings.items():
            if key in name:
                unit = u
                break
        css_vars[f"--{name}"] = f"{resolved_value}{unit}"

    css_string = ":root {\n"
    for var, val in css_vars.items():
        css_string += f"  {var}: {val};\n"
    css_string += "}\n"
    return css_string


# Load the JSON file
with open('tokens-procraft.json', 'r') as f:
    data = json.load(f)

# Create a single dictionary to hold all tokens for easy alias resolution
all_tokens_for_alias_resolution = {}
for token_set_name, token_set_values in data.items():
    # Split the token set name to create the nested structure
    parts = token_set_name.split('/')
    current_level = all_tokens_for_alias_resolution
    for part in parts:
        current_level = current_level.setdefault(part, {})
    current_level.update(token_set_values)

# Ensure the output directory exists
output_dir = 'build/css'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# --- Generate Color CSS files ---
token_sets_to_process = ["Color/Light", "Color/Dark"]
for token_set_name in token_sets_to_process:
    theme_tokens = data.get(token_set_name, {})
    primitives = data.get("Primitive/Mode 1", {})
    # Deep merge primitives into the theme tokens
    merged_tokens = {**primitives, **theme_tokens} 
    
    css_output = generate_css_from_tokens(merged_tokens, all_tokens_for_alias_resolution)
    file_name = f"tokens-{token_set_name.replace('/', '-').lower()}.css"
    with open(os.path.join(output_dir, file_name), 'w') as f:
        f.write(css_output)

# --- Generate other CSS files ---
other_token_sets = {
    "Typography/Modern": {"font-size": "px", "font-height": "px", "letter-spacing": "px"},
    "Typography/Classic": {"font-size": "px", "font-height": "px", "letter-spacing": "px"},
    "Spacing/default": {"space": "px"},
    "Responsive/Desktop": {"font-size": "px", "font-height": "px", "letter-spacing": "px"},
    "Responsive/Mobile": {"font-size": "px", "font-height": "px", "letter-spacing": "px"},
}

for name, units in other_token_sets.items():
    tokens = data.get(name, {})
    css_output = generate_css_from_tokens(tokens, all_tokens_for_alias_resolution, units)
    file_name = f"tokens-{name.replace('/', '-').lower()}.css"
    with open(os.path.join(output_dir, file_name), 'w') as f:
        f.write(css_output)

# --- Generate Corner Radius CSS ---    
corner_radius_tokens = {}
corner_radius_token_names = ["Corner Radius/rounded", "Corner Radius/circle", "Corner Radius/rectangular"]
for name in corner_radius_token_names:
    corner_radius_tokens.update(data.get(name, {}))

css_output = generate_css_from_tokens(corner_radius_tokens, all_tokens_for_alias_resolution, {'radius': 'px'})
with open(os.path.join(output_dir, 'tokens-corner-radius.css'), 'w') as f:
    f.write(css_output)

print("All CSS files have been generated successfully.")
