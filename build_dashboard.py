import json
import os
from datetime import datetime

# 读取插件注册表
with open("plugins.json", "r", encoding="utf-8") as f:
    plugins_config = json.load(f)

# 读取趋势数据（所有格式兼容）
data_files = ["hotspot_data.json", "trends_combined.json"]
all_cards = []
for df in data_files:
    if os.path.exists(df):
        with open(df, "r", encoding="utf-8") as f:
            content = f.read()
            try:
                parsed = json.loads(content)
                if isinstance(parsed, dict) and "cards" in parsed:
                    all_cards.extend(parsed["cards"])
                elif isinstance(parsed, list):
                    all_cards.extend(parsed)
                print(f"Loaded {df}: {len(all_cards)} cards total")
            except:
                pass

# 泛标签黑名单
blacklist = [
    'viral', 'trending', 'explore', 'fyp', 'reels', 'followme', 'instagood',
    'photooftheday', 'instalike', 'beautiful', 'love', 'art', 'happy',
    'picoftheday', 'nature', 'cute', 'style', 'motivation', 'fitness',
    'food', 'travel', 'selfie', 'life', 'model', 'design', 'photography',
    'illustration', 'digitalart', 'sketch', 'drawing', 'painting', 'handmade',
    'craft', 'wedding', 'baby', 'pets', 'animals', 'sunset', 'beach',
    'mountain', 'coffee', 'music', 'game', 'movie', 'book', 'health',
    'workout', 'gym', 'ootd', 'outfit', 'makeup', 'hair', 'school',
    'weekend', 'party', 'holiday', 'newyear', 'christmas', 'halloween'
]

def is_generic_tag(title):
    lower = title.lower().replace(r"[^a-z0-9]", "")
    return any(b == lower for b in blacklist)

# 过滤泛标签
filtered_cards = [c for c in all_cards if not is_generic_tag(c["title"])]
generic_count = len(all_cards) - len(filtered_cards)

# 按平台分组
platform_groups = {}
for card in filtered_cards:
    plat = card.get("platform", "Unknown")
    if plat not in platform_groups:
        platform_groups[plat] = []
    platform_groups[plat].append(card)

now = datetime.now().strftime("%Y-%m-%d %H:%M")
plugins_list = plugins_config.get("plugins", [])

# 生成每个插件的 HTML 模块
plugin_modules = ""
sidebar_entries = ""
filter_buttons = ''
stats_html = ''

for plugin in plugins_list:
    pid = plugin["id"]
    pname = plugin["name"]
    icon = plugin["icon"]
    platform = plugin["platform"]
    
    # 获取该平台的卡片
    cards_in_group = platform_groups.get(platform, [])
    count = len(cards_in_group)
    
    sidebar_entries += f'''<div class="sidebar-item active" data-platform="{platform}">
        <span class="sidebar-icon">{icon}</span>
        <span class="sidebar-label">{pname}</span>
        <span class="sidebar-count">{count}</span>
    </div>'''
    
    filter_buttons += f'<button class="nav-btn active" onclick="filterByPlatform(\'{platform}\')">{icon} {pname}</button>'
    stats_html += f'<div class="stat"><div class="num">{count}</div><div class="label">{platform}</div></div>'
    
    # 生成该插件的卡片HTML
    cards_html = ""
    for c in cards_in_group[:20]:  # 每个平台最多显示20条
        views_html = c.get("views", "")
        vb = f'<span class="views-badge">{views_html}</span>' if views_html else ""
        propsal_text = c.get("proposal", "")
        copy_text = c.get("copy", "")
        
        cards_html += f'''<div class="trend-card" data-platform="{platform}">
            <div class="card-top">
                <span class="platform-indicator">{icon} {platform}</span>
                <span class="heat-stars">{c.get("heat", "")}</span>
                {vb}
            </div>
            <h3 class="trend-title">{c["title"]}</h3>
            <div class="trend-content">
                <p class="proposal"><strong>创意方向:</strong> {propsal_text}</p>
                <p class="copy-text"><em>文案草稿:</em> "{copy_text}"</p>
            </div>
            <div class="card-footer">
                <a href="{c["link"]}" target="_blank" rel="noopener" class="view-source-btn">查看原文 →</a>
            </div>
        </div>'''
    
    plugin_modules += f'''<section class="plugin-section" id="section-{pid}" data-status="active">
        <div class="section-header">
            <h2>{icon} {pname}</h2>
            <div class="section-meta">
                <span class="badge badge-active">● Active</span>
                <span class="update-time">Updated: {now}</span>
            </div>
        </div>
        <div class="section-stats">
            <span class="stat-item">Total Trends: <strong>{count}</strong></span>
            <span class="stat-item">Data Source: {plugin.get("source", "N/A")}</span>
            <span class="stat-item">Status: <strong>Operational</strong></span>
        </div>
        <div class="trends-grid">
            {cards_html}
        </div>
    </section>'''

# 通用统计
total_trends = len(filtered_cards)
ts = f"数据更新于: {now} | 已过滤 {generic_count} 条泛标签 | 显示 {total_trends} 条有效热点"

h = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hellvape Trend Radar - Plugin Architecture</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; color: #1a1a2e; display: flex; min-height: 100vh; }}

/* Sidebar */
.sidebar {{ width: 260px; background: #fff; border-right: 1px solid #e5e7eb; padding: 24px 0; position: fixed; height: 100vh; overflow-y: auto; }}
.sidebar-header {{ padding: 0 24px 20px; border-bottom: 1px solid #f0f0f0; margin-bottom: 16px; }}
.sidebar-header h1 {{ font-size: 18px; font-weight: 700; color: #1a1a2e; margin-bottom: 4px; }}
.sidebar-header p {{ font-size: 12px; color: #6b7280; }}
.sidebar-item {{ display: flex; align-items: center; gap: 12px; padding: 12px 24px; cursor: pointer; transition: background .2s; }}
.sidebar-item:hover, .sidebar-item.active {{ background: #f9fafb; }}
.sidebar-item.active {{ border-left: 3px solid #1a1a2e; }}
.sidebar-icon {{ font-size: 20px; }}
.sidebar-label {{ flex: 1; font-size: 14px; font-weight: 500; }}
.sidebar-count {{ background: #f3f4f6; color: #6b7280; font-size: 12px; padding: 2px 8px; border-radius: 10px; }}

/* Main Content */
.main-content {{ flex: 1; margin-left: 260px; padding: 32px; max-width: 1400px; }}
.page-header {{ margin-bottom: 32px; }}
.page-header h2 {{ font-size: 24px; font-weight: 700; color: #1a1a2e; margin-bottom: 8px; }}
.timestamp-bar {{ background: #fef3c7; border: 1px solid #f59e0b; border-radius: 10px; padding: 12px 20px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; font-size: 13px; }}
.timestamp-bar button {{ padding: 6px 14px; border-radius: 8px; border: 1px solid #d1d5db; background: #fff; cursor: pointer; font-size: 12px; }}

.section-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }}
.section-header h2 {{ font-size: 20px; font-weight: 700; color: #1a1a2e; }}
.badge {{ padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; }}
.badge-active {{ background: #dcfce7; color: #166534; }}
.update-time {{ font-size: 12px; color: #9ca3af; }}

.section-stats {{ display: flex; gap: 20px; margin-bottom: 20px; padding: 12px; background: #f9fafb; border-radius: 8px; font-size: 12px; color: #6b7280; }}
.stat-item {{ display: flex; gap: 4px; }}
.stat-item strong {{ color: #1a1a2e; }}

.trends-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px; }}
.trend-card {{ background: #fff; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); border: 1px solid #f0f0f0; transition: transform .2s, box-shadow .2s; }}
.trend-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.1); }}
.card-top {{ display: flex; align-items: center; gap: 10px; margin-bottom: 12px; flex-wrap: wrap; }}
.platform-indicator {{ background: #1a1a2e; color: #fff; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 600; }}
.heat-stars {{ font-size: 14px; letter-spacing: 2px; }}
.views-badge {{ font-size: 12px; color: #9ca3af; background: #f3f4f6; padding: 3px 10px; border-radius: 6px; }}
.trend-title {{ font-size: 16px; font-weight: 600; color: #1a1a2e; margin-bottom: 12px; }}
.trend-content {{ margin-bottom: 16px; }}
.proposal {{ font-size: 13px; color: #4b5563; margin-bottom: 6px; }}
.copy-text {{ font-size: 12px; color: #6b7280; font-style: italic; }}
.card-footer {{ display: flex; justify-content: flex-end; }}
.view-source-btn {{ padding: 6px 14px; background: #1a1a2e; color: #fff; text-decoration: none; border-radius: 6px; font-size: 12px; font-weight: 500; transition: background .2s; }}
.view-source-btn:hover {{ background: #2d3748; }}

.plugin-section {{ margin-bottom: 48px; animation: fadeIn .3s ease; }}
@keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: translateY(0); }} }}

@media (max-width: 768px) {{
    .sidebar {{ display: none; }}
    .main-content {{ margin-left: 0; }}
    .trends-grid {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<div class="sidebar">
    <div class="sidebar-header">
        <h1>🔥 Hellvape Trend Radar</h1>
        <p>Plugin Architecture v1.0</p>
    </div>
    <div style="padding: 0 24px 12px;">
        <button class="nav-btn active" onclick="showAll()" style="width: 100%; padding: 8px; border-radius: 6px; border: 1px solid #e5e7eb; background: #fff; cursor: pointer; font-size: 12px; margin-bottom: 8px;">🏠 All Platforms ({total_trends})</button>
        {filter_buttons}
    </div>
    <div class="sidebar-item active" onclick="showAll()">
        <span class="sidebar-icon">📊</span>
        <span class="sidebar-label">Dashboard</span>
    </div>
    <div class="sidebar-item" onclick="toggleFilters()">
        <span class="sidebar-icon">🔍</span>
        <span class="sidebar-label">Advanced Filters</span>
    </div>
</div>

<div class="main-content">
    <div class="page-header">
        <h2>Plugin-Based Trend Intelligence</h2>
        <p style="color: #6b7280; font-size: 14px; margin-top: 4px;">Every plugin automatically appears here after installation</p>
    </div>
    
    <div class="timestamp-bar">
        <span id="globalTimestamp">{ts}</span>
        <div>
            <button onclick="toggleGenericFilter()" id="filterToggleBtn">关闭自动过滤泛标签</button>
        </div>
    </div>

    <!-- Plugin Sections Generated Dynamically -->
    {plugin_modules}
</div>

<script>
var filterEnabled = true;
var allCards = JSON.parse('{json.dumps(filtered_cards, ensure_ascii=False)}');

function filterByPlatform(platform) {
    var sections = document.querySelectorAll('.plugin-section');
    sections.forEach(function(section) {
        var isVisible = section.id.includes(platform.toLowerCase()) || 
                       section.querySelector('.platform-indicator')?.textContent.includes(platform);
        section.style.display = isVisible ? 'block' : 'none';
    });
}

function showAll() {
    var sections = document.querySelectorAll('.plugin-section');
    sections.forEach(function(s) {{ s.style.display = 'block'; }});
}

function toggleGenericFilter() {
    filterEnabled = !filterEnabled;
    var btn = document.getElementById('filterToggleBtn');
    if(filterEnabled) {{
        btn.textContent = '关闭自动过滤泛标签';
        renderFiltered();
    }} else {{
        btn.textContent = '显示全部（含泛标签）';
        renderAll();
    }}
}

function renderFiltered() {{
    var grid = document.querySelector('.trends-grid');
    var cards = allCards.filter(c => !isGeneric(c.title));
    generateCards(grid, cards);
}}

function renderAll() {{
    var grid = document.querySelector('.trends-grid');
    generateCards(grid, allCards);
}}

function isGeneric(title) {{
    var lower = title.toLowerCase().replace(/[^a-z0-9]/g,'');
    var bl=['viral','trending','explore','fyp','reels','followme','instagood','photooftheday','instalike','beautiful','love','art','happy','picoftheday','nature','cute','style','motivation','fitness','food','travel','selfie','life','model','design','photography','illustration','digitalart','sketch','drawing','painting','handmade','craft','wedding','baby','pets','animals','sunset','beach','mountain','coffee','music','game','movie','book','health','workout','gym','ootd','outfit','makeup','hair','school','weekend','party','holiday','newyear','christmas','halloween'];
    return bl.indexOf(lower)>=0;
}}

function generateCards(grid, cards) {{
    grid.innerHTML = '';
    cards.forEach(function(c) {{
        var viewsHTML = c.views ? '<span class="views-badge">'+c.views+'</span>' : '';
        grid.innerHTML += '<div class="trend-card"><div class="card-top"><span class="platform-indicator">'+c.platform+'</span><span class="heat-stars">'+c.heat+'</span>'+viewsHTML+'</div><h3 class="trend-title">'+c.title+'</h3><div class="trend-content"><p class="proposal"><strong>创意方向:</strong> '+c.proposal+'</p><p class="copy-text"><em>文案草稿:</em> "'+c.copy+'"</p></div><div class="card-footer"><a href="'+c.link+'" target="_blank" class="view-source-btn">查看原文 →</a></div></div>';
    }});
}}

// Auto-detect installed plugins
document.addEventListener('DOMContentLoaded', function() {{
    console.log('Plugins loaded:', {json.dumps(plugins_list, ensure_ascii=False)});
    renderFiltered();
}});
</script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(h)

print(f"OK: index.html generated ({len(h)} bytes)")
print(f"Total trends: {total_trends}, Generic filtered: {generic_count}")
print(f"Plugins registered: {len(plugins_list)}")
