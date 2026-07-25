import json
from datetime import datetime

with open("hotspot_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

cards_html = ""
for c in data["cards"]:
    pc = {"Twitter/X": "#1DA1F2", "YouTube": "#FF0000", "Instagram": "#E1306C"}.get(c["platform"], "#999")
    vb = '<span class="views-badge">' + c.get("views", "") + "</span>" if c.get("views") else ""
    cards_html += """<div class="card">
        <div class="card-header">
            <span class="platform-tag" style="background:{p}">{e} {pl}</span>
            <span class="heat-stars">{h}</span>{v}
        </div>
        <h3 class="card-title">{t}</h3>
        <p class="card-proposal"><strong>?????</strong>{pr}</p>
        <p class="card-copy"><em>?????</em> "{c}"</p>
        <a href="#" onclick="openModal('{u}'); return false;" class="view-link">???? -&gt;</a>
    </div>""".format(p=pc, e=c["emoji"], pl=c["platform"], h=c["heat"], v=vb, t=c["title"], pr=c["proposal"], c=c["copy"], u=c["link"].replace("'", "\\'"))

cj = json.dumps(data["cards"], ensure_ascii=False)
now = datetime.now().strftime("%Y-%m-%d %H:%M")
n = str(data["total_cards"])

h = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hellvape Hotspot Creative Board</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:#f8f9fa; color:#1a1a2e; line-height:1.6; }
.container { max-width:1200px; margin:0 auto; padding:20px; }
header { text-align:center; padding:40px 20px; background:#fff; border-radius:16px; margin-bottom:30px; box-shadow:0 2px 12px rgba(0,0,0,0.04); }
header h1 { font-size:28px; font-weight:700; color:#1a1a2e; margin-bottom:8px; }
header p { color:#6b7280; font-size:14px; }
.header-stats { display:flex; gap:20px; justify-content:center; margin-top:20px; flex-wrap:wrap; }
.stat { background:#f8f9fa; padding:12px 24px; border-radius:10px; text-align:center; }
.stat .num { font-size:24px; font-weight:700; color:#1a1a2e; }
.stat .label { font-size:12px; color:#9ca3af; text-transform:uppercase; letter-spacing:1px; }
.platform-filter { display:flex; gap:10px; justify-content:center; margin:30px 0; flex-wrap:wrap; }
.filter-btn { padding:8px 20px; border:1px solid #e5e7eb; border-radius:20px; background:#fff; cursor:pointer; font-size:14px; color:#4b5563; transition:all .2s; }
.filter-btn:hover, .filter-btn.active { background:#1a1a2e; color:#fff; border-color:#1a1a2e; }
.cards-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(360px,1fr)); gap:20px; }
.card { background:#fff; border-radius:12px; padding:24px; box-shadow:0 2px 12px rgba(0,0,0,0.06); border:1px solid #f0f0f0; transition:transform .2s,box-shadow .2s; }
.card:hover { transform:translateY(-2px); box-shadow:0 4px 20px rgba(0,0,0,0.1); }
.card-header { display:flex; align-items:center; gap:12px; margin-bottom:16px; flex-wrap:wrap; }
.platform-tag { display:inline-flex; align-items:center; gap:6px; padding:4px 12px; border-radius:16px; font-size:12px; font-weight:600; color:#fff; }
.heat-stars { font-size:14px; letter-spacing:2px; }
.views-badge { font-size:12px; color:#9ca3af; background:#f3f4f6; padding:3px 10px; border-radius:8px; }
.card-title { font-size:17px; font-weight:600; color:#1a1a2e; margin-bottom:12px; }
.card-proposal { font-size:14px; color:#4b5563; margin-bottom:8px; }
.card-copy { font-size:13px; color:#6b7280; margin-bottom:16px; font-style:italic; }
.view-link { display:inline-block; padding:8px 16px; background:#f0f0f0; color:#4b5563; text-decoration:none; border-radius:8px; font-size:13px; font-weight:500; transition:background .2s; }
.view-link:hover { background:#e5e7eb; color:#1a1a2e; }
.footer { text-align:center; padding:40px 20px; color:#9ca3af; font-size:13px; }
.modal-overlay { position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.4);backdrop-filter:blur(4px);z-index:9999;display:none;justify-content:center;align-items:center;animation:fadeIn .25s ease; }
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes slideUp{from{transform:translateY(30px);opacity:0}to{transform:translateY(0);opacity:1}}
.modal-box { width:90vw;height:80vh;background:#fff;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,.15);display:flex;flex-direction:column;overflow:hidden;animation:slideUp .3s ease; }
.modal-header { display:flex;justify-content:space-between;align-items:center;padding:16px 24px;border-bottom:1px solid #f0f0f0;background:#fafafa; }
.modal-header h2 { font-size:16px;font-weight:600;color:#1a1a2e; }
.modal-close { width:32px;height:32px;border-radius:8px;border:none;background:#f0f0f0;color:#6b7280;font-size:18px;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:all .2s; }
.modal-close:hover { background:#e5e7eb;color:#1a1a2e; }
.modal-body { flex:1;position:relative; }
.modal-body iframe { width:100%;height:100%;border:none; }
.modal-loading { position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;color:#9ca3af; }
.modal-loading .spinner { width:32px;height:32px;border:3px solid #f0f0f0;border-top-color:#1a1a2e;border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 12px; }
@keyframes spin { to{transform:rotate(360deg)} }
.modal-error { position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;color:#6b7280; }
.modal-error a { color:#1a1a2e;font-weight:500; }
@media(max-width:768px){ .cards-grid{grid-template-columns:1fr} header h1{font-size:22px} .modal-box{width:98vw;height:95vh;border-radius:12px} }
</style>
</head>
<body>
<div class="container">
<header>
    <h1>Hellvape Hotspot Creative Board</h1>
    <p>Daily trending topics with brand-aligned creative proposals</p>
    <p style="font-size:12px;color:#9ca3af;margin-top:4px;">Generated at __GEN_AT__ ? __TOTAL__ trends analyzed</p>
    <div class="header-stats">
        <div class="stat"><div class="num">__TOTAL__</div><div class="label">Trends</div></div>
        <div class="stat"><div class="num">3</div><div class="label">Platforms</div></div>
    </div>
</header>
<div class="platform-filter">
    <button class="filter-btn active" onclick="filterCards('all')">All Platforms (__TOTAL__)</button>
    <button class="filter-btn" onclick="filterCards('Twitter/X')">Twitter/X</button>
    <button class="filter-btn" onclick="filterCards('YouTube')">YouTube</button>
    <button class="filter-btn" onclick="filterCards('Instagram')">Instagram</button>
</div>
<div class="cards-grid">
__CARDS__
</div>
<div class="footer"><p>Built for Hellvape | Built for Vapers | Born to Build</p></div>
<div class="modal-overlay" id="modalOverlay" onclick="if(event.target===this)closeModal()">
    <div class="modal-box">
        <div class="modal-header">
            <h2 id="modalTitle">Loading...</h2>
            <button class="modal-close" onclick="closeModal()" title="Close">&times;</button>
        </div>
        <div class="modal-body">
            <div class="modal-loading" id="modalLoading"><div class="spinner"></div><div>Loading original page...</div></div>
            <div class="modal-error" id="modalError" style="display:none"><p>This site blocks embedded viewing.</p><p style="margin-top:8px;"><a id="fallbackLink" href="#" target="_blank">Click here to open directly -&gt;</a></p></div>
            <iframe id="modalIframe" src="" style="display:none"></iframe>
        </div>
    </div>
</div>
<script>
var allCards=JSON.parse('__ALLCARDS__');
function filterCards(platform){var cards=document.querySelectorAll('.card'),btns=document.querySelectorAll('.filter-btn');btns.forEach(function(b){b.classList.remove('active')});event.target.classList.add('active');cards.forEach(function(card){if(platform==='all'){card.style.display='';return}var hp=card.querySelector('.platform-tag').textContent.toLowerCase();card.style.display=hp.includes(platform.toLowerCase())?'':'none'})}
var currentUrl='',currentTitle='';
function openModal(url){currentUrl=url;var o=document.getElementById('modalOverlay'),l=document.getElementById('modalLoading'),e=document.getElementById('modalError'),f=document.getElementById('modalIframe'),t=document.getElementById('modalTitle');for(var i=0;i<allCards.length;i++){if(allCards[i].link===url){currentTitle=allCards[i].title;break}}l.style.display='block';e.style.display='none';f.style.display='none';t.textContent=currentTitle||'Preview';f.src=url;o.style.display='flex';document.body.style.overflow='hidden'}
function closeModal(){var o=document.getElementById('modalOverlay'),f=document.getElementById('modalIframe');o.style.display='none';f.src='';document.body.style.overflow=''}
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeModal()})
</script>
</body>
</html>"""

h = h.replace("__GEN_AT__", now).replace("__TOTAL__", n).replace("__CARDS__", cards_html).replace("__ALLCARDS__", cj)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(h)

print("OK: index.html", len(h), "bytes")
