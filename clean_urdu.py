import re

for filename in ['engineers.html', 'apply.html', 'profile.html', 'terms.html', 'privacy.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove CSS
    content = re.sub(r'[ \t]*/\* urdu summary block \(used in EN mode only\) \*/\r?\n', '', content)
    content = re.sub(r'[ \t]*/\* hide the EN-mode Urdu summary blocks when the whole page is already Urdu \*/\r?\n', '', content)
    content = re.sub(r'[ \t]*\.urdu\{.*?\}\r?\n?', '', content)
    content = re.sub(r'[ \t]*\.urdu small\{.*?\}\r?\n?', '', content)
    content = re.sub(r'[ \t]*html\[dir="rtl"\] \.urdu\{display:none;\}\r?\n?', '', content)
    
    # Remove HTML blocks
    content = re.sub(r'[ \t]*<div class="urdu"[^>]*>.*?</div>\r?\n?', '', content, flags=re.DOTALL)
    # in apply and profile, there's a <br> just before the span
    content = re.sub(r'[ \t]*<br>\r?\n[ \t]*<span class="urdu"[^>]*>.*?</span>\r?\n?', '', content, flags=re.DOTALL)
    content = re.sub(r'[ \t]*<span class="urdu"[^>]*>.*?</span>\r?\n?', '', content, flags=re.DOTALL)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

