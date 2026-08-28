from pathlib import Path
p=Path('public/index.html')
s=p.read_text(encoding='utf-8')
repls={
"*{box-sizing:border-box}html,body{margin:0;height:100%}":"*{box-sizing:border-box}html{margin:0;min-height:100%;height:auto}body{margin:0;min-height:100vh;height:auto}",
"body{font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,Arial,sans-serif;background:var(--bg);color:var(--txt);overflow:hidden}":"body{font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,Arial,sans-serif;background:var(--bg);color:var(--txt);overflow-x:auto;overflow-y:scroll}",
"#app{display:flex;flex-direction:column;height:100vh;height:100dvh;min-height:0}":"#app{display:block;min-height:100vh;height:auto;overflow:visible}",
".main{flex:1;display:flex;flex-direction:column;min-width:0;min-height:0;overflow:hidden}":".main{display:block;min-width:0;min-height:0;overflow:visible}",
".view{flex:1;min-height:0;overflow-y:auto;overflow-x:auto;padding:18px;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}":".view{display:block;min-height:0;height:auto;overflow:visible;padding:18px}",
".pos{display:grid;grid-template-columns:1fr 380px;gap:16px;height:100%}":".pos{display:grid;grid-template-columns:1fr 380px;gap:16px;min-height:calc(100vh - 180px);height:auto}"
}
for a,b in repls.items():
    if a not in s:
        raise SystemExit('missing pattern: '+a[:80])
    s=s.replace(a,b,1)
p.write_text(s,encoding='utf-8')
print('scroll v3 applied')
