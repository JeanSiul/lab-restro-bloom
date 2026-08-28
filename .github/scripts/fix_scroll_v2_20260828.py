from pathlib import Path

p = Path('public/index.html')
s = p.read_text(encoding='utf-8')

replacements = {
    'body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--txt);overflow:auto}':
    'body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--txt);overflow:hidden}',
    '#app{display:flex;flex-direction:column;min-height:100vh;height:auto}':
    '#app{display:flex;flex-direction:column;height:100vh;height:100dvh;min-height:0}',
    '.main{flex:1;display:flex;flex-direction:column;min-width:0}':
    '.main{flex:1;display:flex;flex-direction:column;min-width:0;min-height:0;overflow:hidden}',
    '.view{flex:1;overflow:auto;padding:18px}':
    '.view{flex:1;min-height:0;overflow-y:auto;overflow-x:auto;padding:18px;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}'
}

for old, new in replacements.items():
    if old not in s:
        raise SystemExit(f'Missing expected CSS fragment: {old}')
    s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
print('Applied flex scroll fix v2')
