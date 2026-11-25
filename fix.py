import re

with open('C:/Users/sison/ai-builds/BuildDay/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "import time" in line:
        new_lines.append(line)
        new_lines.append("import requests\n")
    elif line.strip() == "import requests":
        continue
    elif line.strip() == 'OPENROUTER_API_KEY = "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"':
        continue
    else:
        new_lines.append(line)

with open('C:/Users/sison/ai-builds/BuildDay/app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
    
with open('C:/Users/sison/ai-builds/BuildDay/app.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("def deterministic_route", "OPENROUTER_API_KEY = \"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\"\n\ndef deterministic_route")

with open('C:/Users/sison/ai-builds/BuildDay/app.py', 'w', encoding='utf-8') as f:
    f.write(text)
