import json; 
css_variables = {}; 
def process_colors(data, prefix=''):
    for key, value in data.items():
        if isinstance(value, dict):
            process_colors(value, f'{prefix}-{key}' if prefix else key)
        elif key == '$value':
            css_variables[prefix] = value;

with open('tokens-procraft.json', 'r') as f:
    data = json.load(f);

for key, value in data.items():
    if key.startswith('Color/'):
        process_colors(value, key);

for key, value in data.items():
    if key.startswith('Primitive/Mode 1'):
        process_colors(value, key)

with open('tokens.css', 'w') as f:
    f.write(':root {\n')
    for name, value in css_variables.items():
        css_name = '--' + name.replace('/', '-').replace(' ', '-').replace('(', '').replace(')', '').lower()
        if isinstance(value, str) and value.startswith('{'):
            ref_name = value.strip('{}').replace('.', '-').lower()
            f.write(f'  {css_name}: var(--{ref_name});\n')
        else:
            f.write(f'  {css_name}: {value};\n')
    f.write('}')