for filename in ['engineers.html', 'apply.html', 'profile.html', 'terms.html', 'privacy.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace('html[dir="rtl"]</style>', '</style>')
    content = content.replace('html[dir="rtl"]\n</style>', '</style>')
    content = content.replace('html[dir="rtl"]  html[dir="rtl"] ul', 'html[dir="rtl"] ul')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

