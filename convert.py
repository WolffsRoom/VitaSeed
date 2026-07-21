import json
import re

with open('js/data.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# Extract the array content
match = re.search(r'const projectsData\s*=\s*(\[\s*\{.*\}\s*\]);', js_code, re.DOTALL)
if match:
    array_str = match.group(1)
    
    # Fix unquoted keys:
    # Match an identifier followed by a colon
    json_str = re.sub(r'([{,]\s*)([A-Za-z0-9_]+)(\s*:)', r'\1"\2"\3', array_str)
    
    # Clean up any trailing commas
    json_str = re.sub(r',\s*\}', '}', json_str)
    json_str = re.sub(r',\s*\]', ']', json_str)

    try:
        data = json.loads(json_str)
        out = {"projects": data}
        with open('api/catalog.json', 'w', encoding='utf-8') as out_f:
            json.dump(out, out_f, indent=2, ensure_ascii=False)
        print("Success!")
    except Exception as e:
        print("JSON Decode Error:", e)
else:
    print("Could not find array.")
