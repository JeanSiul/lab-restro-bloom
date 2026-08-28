from pathlib import Path
p = Path('public/index.html')
s = p.read_text(encoding='utf-8')
old = 'body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--txt);overflow:hidden}'
new = 'body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--txt);overflow:auto}'
if old not in s:
    raise SystemExit('body overflow rule not found')
s = s.replace(old, new, 1)
old2 = '#app{display:flex;flex-direction:column;height:100vh}'
new2 = '#app{display:flex;flex-direction:column;min-height:100vh;height:auto}'
if old2 not in s:
    raise SystemExit('#app height rule not found')
s = s.replace(old2, new2, 1)
p.write_text(s, encoding='utf-8')
print('scroll patch applied')
