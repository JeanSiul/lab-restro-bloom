from pathlib import Path

p = Path('public/index.html')
s = p.read_text(encoding='utf-8')

repls = {
"*{box-sizing:border-box}html{margin:0;min-height:100%;height:auto}body{margin:0;min-height:100vh;height:auto}": "*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden}",
"body{font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,Arial,sans-serif;background:var(--bg);color:var(--txt);overflow-x:auto;overflow-y:scroll}": "body{font-family:-apple-system,BlinkMacSystemFont,\"Segoe UI\",Roboto,Arial,sans-serif;background:var(--bg);color:var(--txt);overflow:hidden}",
"#app{display:block;min-height:100vh;height:auto;overflow:visible}": "#app{display:flex;flex-direction:column;width:100%;height:100vh;height:100dvh;overflow:hidden}",
".main{display:block;min-width:0;min-height:0;overflow:visible}": ".main{display:flex;flex:1;flex-direction:column;min-width:0;min-height:0;overflow:hidden}",
".view{display:block;min-height:0;height:auto;overflow:visible;padding:18px}": ".view{display:block;flex:1;min-height:0;height:0;overflow-x:auto;overflow-y:scroll;padding:18px;-webkit-overflow-scrolling:touch;scrollbar-gutter:stable}",
".pos{display:grid;grid-template-columns:1fr 380px;gap:16px;min-height:calc(100vh - 180px);height:auto}": ".pos{display:grid;grid-template-columns:1fr 380px;gap:16px;min-height:100%;height:auto}"
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit('missing pattern: ' + old[:80])
    s=s.replace(old,new,1)

marker = "</body>"
probe = """
<script>
(function(){
  function enforceScrollableView(){
    const view=document.querySelector('.view');
    const app=document.querySelector('#app');
    const sidebar=document.querySelector('.sidebar');
    const topbar=document.querySelector('.topbar');
    if(!view||!app) return;
    const used=(sidebar?sidebar.getBoundingClientRect().height:0)+(topbar?topbar.getBoundingClientRect().height:0);
    const h=Math.max(180, window.innerHeight-used);
    view.style.height=h+'px';
    view.style.maxHeight=h+'px';
    view.style.minHeight='0';
    view.style.overflowY='scroll';
    view.style.overflowX='auto';
    view.style.touchAction='pan-y';
  }
  window.addEventListener('load',enforceScrollableView);
  window.addEventListener('resize',enforceScrollableView);
  document.addEventListener('click',()=>setTimeout(enforceScrollableView,0),true);
  new MutationObserver(()=>setTimeout(enforceScrollableView,0)).observe(document.body,{subtree:true,childList:true});
  setTimeout(enforceScrollableView,100);
})();
</script>
"""
if probe.strip() not in s:
    s=s.replace(marker,probe+marker,1)

p.write_text(s,encoding='utf-8')
print('scroll v4 applied')
