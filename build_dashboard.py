import json
import os
from datetime import datetime

# 黑名单标签
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

# 加载数据
data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hotspot_data.json")
with open(data_file, "r", encoding="utf-8") as f:
    hotspots = json.load(f)

cards = hotspots.get("cards", [])
now = datetime.now().strftime("%Y/%m/%d %H:%M")

# 过滤泛标签
filtered = [c for c in cards if not is_generic(c.get("title", ""))]
generic_count = len(cards) - len(filtered)

# 按平台分组
platform_groups = {}
for card in filtered:
    plat = card.get("platform", "Unknown")
    if plat not in platform_groups:
        platform_groups[plat] = []
    platform_groups[plat].append(card)

# 生成卡片 HTML
cards_html = ""
stats_html = ""
filter_buttons = ""
emoji_map = {"Twitter/X": "\U0001F426", "YouTube": "\u25B6\uFE0F", "Instagram": "\U0001F4F8"}

for platform, pcards in platform_groups.items():
    emoji = emoji_map.get(platform, "\U0001F525")
    stats_html += '<div class="stat"><div class="num">' + str(len(pcards)) + '</div><div class="label">' + platform + '</div></div>'
    filter_buttons += '<button class="nav-btn"' + ' data-platform="' + platform + '">' + emoji + ' ' + platform + ' (' + str(len(pcards)) + ')</button>'
    for c in pcards[:20]:
        views_val = c.get("views", "") or ""
        vb = '<span class="views-badge">' + views_val + '</span>' if views_val else ""
        title_val = c.get("title", "Untitled") or "Untitled"
        proposal_val = c.get("proposal", "") or ""
        copy_val = c.get("copy", "") or ""
        link_val = c.get("link", "#") or "#"
        heat_val = c.get("heat", "") or "☆☆☆☆☆"
        cards_html += '<div class="trend-card" data-platform="' + platform + '">'
        cards_html += '<div class="card-top">'
        cards_html += '<span class="platform-indicator">' + emoji + platform + '</span>'
        cards_html += '<span class="heat-stars">' + heat_val + '</span>'
        cards_html += vb
        cards_html += '</div>'
        cards_html += '<h3 class="trend-title">' + title_val + '</h3>'
        cards_html += '<div class="trend-content">'
        if proposal_val:
            cards_html += '<p class="proposal"><strong>创意方向:</strong> ' + proposal_val + '</p>'
        if copy_val:
            cards_html += '<p class="copy-text"><em>文案草稿:</em> "' + copy_val + '"</p>'
        cards_html += '</div>'
        cards_html += '<a href="' + link_val + '" target="_blank" class="view-source-btn">查看原文 →</a>'
        cards_html += '</div>'

sidebar_items = ""
for platform in platform_groups:
    emoji = emoji_map.get(platform, "\U0001F525")
    sidebar_items += '<div class="sidebar-item" data-platform="' + platform + '"><span class="sidebar-icon">' + emoji + '</span><span class="sidebar-label">' + platform + '</span></div>'

plugins_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugins.json")
plugins_list = []
if os.path.exists(plugins_json):
    with open(plugins_json, "r", encoding="utf-8-sig") as f:
        plugins_list = json.load(f).get("plugins", [])

for plugin in plugins_list:
    pname = plugin.get("name", "Unknown")
    icon = plugin.get("icon", "\U0001F4E6")
    sidebar_items += '<div class="sidebar-item" data-platform="' + pname.replace(" ", "-").lower() + '"><span class="sidebar-icon">' + icon + '</span><span class="sidebar-label">' + pname + '</span></div>'

h = '<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>Hellvape Trend Radar v2.0</title>\n<style>\n'

h += '*{margin:0;padding:0;box-sizing:border-box}\n'
h += 'body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#f8f9fa;color:#1a1a2e;display:flex;min-height:100vh}\n'
h += '.sidebar{width:260px;background:#fff;border-right:1px solid #e5e7eb;padding:24px 0;position:fixed;height:100vh;overflow-y:auto;z-index:100;transition:left .3s}\n'
h += '.sidebar.collapsed{left:-260px}\n'
h += '.sidebar-toggle{position:fixed;left:260px;top:24px;background:#1a1a2e;color:#fff;border:none;padding:8px 12px;cursor:pointer;z-index:101;border-radius:0 8px 8px 0;font-size:16px;transition:left .3s}\n'
h += '.sidebar-toggle.collapsed{left:0}\n'
h += '.sidebar-header{padding:0 24px 20px;border-bottom:1px solid #f0f0f0;margin-bottom:16px}\n'
h += '.sidebar-header h1{font-size:18px;font-weight:700;color:#1a1a2e;margin-bottom:4px}\n'
h += '.sidebar-header p{font-size:12px;color:#6b7280}\n'
h += '.sidebar-item{display:flex;align-items:center;gap:12px;padding:12px 24px;cursor:pointer;transition:background .2s}\n'
h += '.sidebar-item:hover,.sidebar-item.active{background:#f3f4f6}\n'
h += '.sidebar-icon{font-size:20px}.sidebar-label{flex:1;font-size:14px;font-weight:500}\n'
h += '.main-content{flex:1;margin-left:260px;padding:32px;max-width:1400px;transition:margin-left .3s}\n'
h += '.main-content.expanded{margin-left:0}\n'
h += '.stats-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin-bottom:24px}\n'
h += '.stat{background:#fff;border-radius:12px;padding:16px;text-align:center;border:1px solid #f0f0f0}\n'
h += '.stat .num{font-size:28px;font-weight:700;color:#1a1a2e}.stat .label{font-size:12px;color:#6b7280;margin-top:4px}\n'
h += '.timestamp-bar{background:#fef3c7;border:1px solid #f59e0b;border-radius:10px;padding:12px 20px;margin-bottom:24px;font-size:13px;display:flex;justify-content:space-between;align-items:center}\n'
h += '.filter-buttons{display:flex;gap:12px;margin-bottom:24px;flex-wrap:wrap}\n'
h += '.nav-btn{padding:8px 16px;border:1px solid #e5e7eb;background:#fff;border-radius:20px;cursor:pointer;font-size:14px;transition:all .2s}\n'
h += '.nav-btn:hover,.nav-btn.active{background:#1a1a2e;color:#fff;border-color:#1a1a2e}\n'
h += '.trends-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}\n'
h += '.trend-card{background:#fff;border-radius:12px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.06);border:1px solid #f0f0f0;transition:transform .2s}\n'
h += '.trend-card:hover{transform:translateY(-2px);box-shadow:0 4px 16px rgba(0,0,0,.1)}\n'
h += '.card-top{display:flex;gap:10px;margin-bottom:12px;flex-wrap:wrap}\n'
h += '.platform-indicator{background:#1a1a2e;color:#fff;padding:4px 10px;border-radius:6px;font-size:11px;font-weight:600}\n'
h += '.heat-stars{font-size:14px}.views-badge{font-size:12px;color:#9ca3af;background:#f3f4f6;padding:3px 10px;border-radius:6px}\n'
h += '.trend-title{font-size:16px;font-weight:600;margin-bottom:12px}\n'
h += '.proposal{font-size:13px;color:#4b5563;margin-bottom:6px}\n'
h += '.copy-text{font-size:12px;color:#6b7280;font-style:italic}\n'
h += '.view-source-btn{display:inline-block;padding:6px 14px;background:#1a1a2e;color:#fff;text-decoration:none;border-radius:6px;font-size:12px;margin-top:8px;transition:background .2s}\n'
h += '.view-source-btn:hover{background:#2d3748}\n'
h += '@media(max-width:768px){.sidebar{left:-260px}.sidebar-toggle{left:0!important}.main-content{margin-left:0!important}}\n'

h += '</style>\n</head>\n<body>\n<button class="sidebar-toggle" onclick="toggleSidebar()">☰</button>\n'
h += '<div class="sidebar" id="sidebar">\n<div class="sidebar-header">\n<h1>🔥 Hellvape Trend Radar</h1>\n<p>Plugin Architecture v2.0 · ' + now + '</p>\n</div>\n'
h += sidebar_items + '\n</div>\n<div class="main-content" id="mainContent">\n'
h += '<div class="stats-row">' + stats_html + '</div>\n'
h += '<div class="timestamp-bar">\n<span>已过滤 ' + str(generic_count) + ' 条泛标签 | 显示 ' + str(len(filtered)) + ' 条有效热点 | 更新于 ' + now + '</span>\n'
h += '<label style="white-space:nowrap"><input type="checkbox" id="toggleFilter" checked onchange="toggleGeneric()">仅显示时效热点</label>\n</div>\n'
h += '<div class="filter-buttons">' + filter_buttons + '<button class="nav-btn active" data-platform="all" onclick="showAll()">全部 (' + str(len(cards)) + ')</button></div>\n'
h += '<div class="trends-grid">' + cards_html + '</div>\n</div>\n<script>\n'
h += 'function toggleSidebar(){var s=document.getElementById("sidebar"),m=document.getElementById("mainContent"),t=document.querySelector(".sidebar-toggle");s.classList.toggle("collapsed");m.classList.toggle("expanded");t.classList.toggle("collapsed")}\n'
h += 'function toggleGeneric(){var show=document.getElementById("toggleFilter").checked,cards=document.querySelectorAll(".trend-card"),bl=[' + json.dumps(blacklist) + '];cards.forEach(function(card){var t=card.querySelector(".trend-title").textContent.toLowerCase();if(show&&bl.some(function(b){return t.includes(b)})){card.style.display="none"}else{card.style.display=""}})}\n'
h += 'function showAll(){document.querySelectorAll(".trend-card").forEach(function(c){c.style.display=""});document.querySelectorAll(".nav-btn").forEach(function(b){b.classList.remove("active")});document.querySelector("[data-platform=\\"all\\"]").classList.add("active")}\n'
h += 'document.querySelectorAll(".nav-btn").forEach(function(btn){btn.addEventListener("click",function(){var p=this.getAttribute("data-platform");document.querySelectorAll(".nav-btn").forEach(function(b){b.classList.remove("active")});this.classList.add("active");if(p==="all"){showAll()}else{document.querySelectorAll(".trend-card").forEach(function(card){card.style.display=card.dataset.platform===p?"":"none"})}})}\n'
h += 'document.querySelectorAll(".sidebar-item").forEach(function(item){item.addEventListener("click",function(){var p=item.getAttribute("data-platform");if(p&&document.querySelector("[data-platform=\\"" + p + "\\"]")){document.querySelector("[data-platform=\\"" + p + "\\"]").click()}})});\n'
h += '</script>\n</body>\n</html>'

with open("index.html", "w", encoding="utf-8") as f:
    f.write(h)
print("OK: index.html generated (" + str(len(h)) + " bytes), " + str(len(filtered)) + " trends shown, " + str(generic_count) + " filtered")
