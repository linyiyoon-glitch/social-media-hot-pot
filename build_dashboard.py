import json
import os
from datetime import datetime

blacklist = [
    "viral", "trending", "explore", "fyp", "reels", "followme", "instagood",
    "photooftheday", "instalike", "beautiful", "love", "art", "happy",
    "picoftheday", "nature", "cute", "style", "motivation", "fitness",
    "food", "travel", "selfie", "life", "model", "design", "photography",
    "illustration", "digitalart", "sketch", "drawing", "painting", "handmade",
    "craft", "wedding", "baby", "pets", "animals", "sunset", "beach",
    "mountain", "coffee", "music", "game", "movie", "book", "health",
    "workout", "gym", "ootd", "outfit", "makeup", "hair", "school",
    "weekend", "party", "holiday", "newyear", "christmas", "halloween"
]

def is_generic(title):
    t = title.lower().replace("#", "").strip()
    return any(b == t for b in blacklist)

data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hotspot_data.json")
with open(data_file, "r", encoding="utf-8-sig") as f:
    hotspots = json.load(f)

cards = hotspots.get("cards", [])
now = datetime.now().strftime("%Y/%m/%d %H:%M")

filtered = [c for c in cards if not is_generic(c.get("title", ""))]
generic_count = len(cards) - len(filtered)

platform_groups = {}
for card in filtered:
    plat = card.get("platform", "Unknown")
    if plat not in platform_groups:
        platform_groups[plat] = []
    platform_groups[plat].append(card)

cards_html = ""
stats_html = ""
filter_buttons = ""
emoji_map = {"Twitter/X": "🐦", "YouTube": "▶️", "Instagram": "📸"}
platform_order = ["Twitter/X", "YouTube", "Instagram"]

for platform in platform_order:
    if platform not in platform_groups:
        continue
    pcards = platform_groups[platform]
    emoji = emoji_map.get(platform, "🔷")
    stats_html += '<div class="stat"><div class="num">' + str(len(pcards)) + '</div><div class="label">' + platform + '</div></div>'
    filter_buttons += '<button class="nav-btn" data-platform="' + platform + '">' + emoji + " " + platform + ' (' + str(len(pcards)) + ')</button>'
    for c in pcards[:20]:
        views_val = c.get("views") or ""
        vb = '<span class="views-badge">' + views_val + '</span>' if views_val else ""
        title_val = c.get("title") or "Untitled"
        proposal_val = c.get("proposal") or ""
        copy_val = c.get("copy") or ""
        link_val = c.get("link") or "#"
        heat_val = c.get("heat") or "⭐⭐☆☆"
        cards_html += '<div class="trend-card" data-platform="' + platform + '">'
        cards_html += '<div class="card-top"><span class="platform-indicator">' + emoji + platform + '</span><span class="heat-stars">' + heat_val + '</span>' + vb + '</div>'
        cards_html += '<h3 class="trend-title">' + title_val + '</h3>'
        cards_html += '<div class="trend-content">'
        if proposal_val: cards_html += '<p class="proposal"><strong>创意方向:</strong>' + proposal_val + '</p>'
        if copy_val: cards_html += '<p class="copy-text"><em>文案草稿:</em> "' + copy_val + '"</p>'
        cards_html += '</div><a href="' + link_val + '" target="_blank" class="view-source-btn">查看原文 →</a></div>'

sidebar_items = ""
for platform in platform_order:
    if platform not in platform_groups: continue
    emoji = emoji_map.get(platform, "🔷")
    sidebar_items += '<div class="sidebar-item" data-platform="' + platform + '"><span class="sidebar-icon">' + emoji + '</span><span class="sidebar-label">' + platform + '</span></div>'

h = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hellvape Trend Radar v2.0</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f8f9fa;color:#1a1a2e;display:flex;min-height:100vh}
.sidebar{width:260px;background:#fff;border-right:1px solid #e5e7eb;padding:24px 0;position:fixed;top:0;left:0;height:100vh;overflow-y:auto;z-index:100;transition:transform .3s}
.sidebar.collapsed{translateX(-260px)}
.sidebar-toggle{position:fixed;top:20px;left:260px;background:#1a1a2e;color:#fff;border:none;width:36px;height:36px;cursor:pointer;z-index:101;border-radius:0 8px 8px 0;font-size:18px;transition:left .3s;display:flex;align-items:center;justify-content:center}
.sidebar-toggle.collapsed{left:0}
.main-content{margin-left:260px;padding:24px;transition:margin .3s}
.main-content.expanded{margin-left:0}
.stats-row{display:flex;gap:16px;margin-bottom:24px;flex-wrap:wrap}
.stat{background:#fff;padding:12px 20px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,.06);text-align:center;min-width:120px}
.stat .num{font-size:24px;font-weight:700;color:#1a1a2e}
.stat .label{font-size:12px;color:#6b7280;margin-top:4px}
.timestamp-bar{background:#fef3c7;border:1px solid #f59e0b;border-radius:10px;padding:12px 20px;margin-bottom:24px;font-size:13px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px}
.filter-buttons{display:flex;gap:12px;margin-bottom:24px;flex-wrap:wrap}
.nav-btn{padding:8px 16px;border:1px solid #e5e7eb;background:#fff;border-radius:20px;cursor:pointer;font-size:14px;transition:all .2s}
.nav-btn:hover,.nav-btn.active{background:#1a1a2e;color:#fff;border-color:#1a1a2e}
.trends-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}
.trend-card{background:#fff;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.06);border:1px solid #f0f0f0;transition:transform .2s}
.trend-card:hover{transform:translateY(-4px);box-shadow:0 4px 16px rgba(0,0,0,.1)}.trend-card:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.1)}
.card-top{display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap}
.platform-indicator{background:#1a1a2e;color:#fff;padding:4px 10px;border-radius:6px;font-size:11px;font-weight:600}
.heat-stars{font-size:14px}.views-badge{font-size:12px;color:#9ca3af;background:#f3f4f6;padding:3px 10px;border-radius:6px}
.trend-title{font-size:16px;font-weight:600;margin-bottom:12px;min-height:20px}
.proposal{font-size:13px;color:#4b5563;margin-bottom:6px}.copy-text{font-size:12px;color:#6b7280;font-style:italic}
.view-source-btn{display:inline-block;padding:6px 14px;background:#1a1a2e;color:#fff;text-decoration:none;border-radius:6px;font-size:12px;margin-top:8px;transition:background .2s}
.view-source-btn:hover{background:#2d3748}
@media(max-width:768px){.sidebar{translateX(-260px)}.sidebar-toggle{left:0!important}.main-content{margin-left:0!important}}</style>
</head>
<body>
<button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>
<div class="sidebar" id="sidebar"><div class="sidebar-header"><h1>🔥 Hellvape Trend Radar</h1><p>Plugin Architecture v2.0 · </p></div>""" + sidebar_items + """</div>
<div class="main-content" id="mainContent">
<div class="stats-row">""" + stats_html + """</div>
<div class="timestamp-bar"><span>已过滤 """ + str(generic_count) + """ 条泛标签 | 显示 """ + str(len(filtered)) + """ 条有效热点 | 更新于 """ + now + """</span><label style="white-space:nowrap;font-size:13px"><input type="checkbox" id="toggleFilter" checked onchange="toggleGeneric()">仅显示时效热点</label></div>
<div class="filter-buttons">""" + filter_buttons + '''<button class="nav-btn" data-platform="all" onclick="showAll()">全部 (' + str(len(cards)) + ')</button></div>
<div class="trends-grid">''' + cards_html + '''</div></div>
<script>
function toggleSidebar(){var s=document.getElementById(\'sidebar\'),m=document.getElementById(\'mainContent\'),t=document.querySelector(\'.sidebar-toggle\');s.classList.toggle(\'collapsed\');m.classList.toggle(\'expanded\');t.classList.toggle(\'collapsed\')}
function showAll(){document.querySelectorAll(".trend-card").forEach(function(c){c.style.display="";});document.querySelectorAll(".nav-btn").forEach(function(b){b.classList.remove("active")});document.querySelector(\'[data-platform="all"]').classList.add("active")}
function toggleFilter(){var show=document.getElementById("toggleFilter").checked,bl=[];cards=document.querySelectorAll(".trend-card");cards.forEach(function(card){var t=card.querySelector(".trend-title");if(t&&bl.some(function(b){return t.textContent.toLowerCase().includes(b)})){card.style.display="none"}else{card.style.display=""}})}
function filterByPlatform(p){document.querySelectorAll(".trend-card").forEach(function(c){c.style.display=c.dataset.platform===p?"":""});document.querySelectorAll(".nav-btn").forEach(function(b){b.classList.remove("active")});document.querySelector(\'[data-platform="\'+p+"\"]').classList.add("active")}
document.querySelectorAll(".nav-btn").forEach(function(btn){btn.addEventListener("click",function(){var p=this.getAttribute("data-platform");if(p==="all"){showAll()}else{filterByPlatform(p)}})};
</script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(h)
print("OK: index.html generated with fixed interaction")