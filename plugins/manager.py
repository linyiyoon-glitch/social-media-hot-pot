import json
import os
import glob
from datetime import datetime

class PluginManager:
    def __init__(self, plugins_dir="plugins", config_file="config/dashboard.yaml"):
        self.plugins = {}
        self.plugins_dir = plugins_dir
        self.registry_file = os.path.join(plugins_dir, "registry.json")
        
    def discover_plugins(self):
        """自动发现所有插件"""
        found = []
        for plugin_json in glob.glob(os.path.join(self.plugins_dir, "*.json")):
            if plugin_json == self.registry_file:
                continue
            try:
                with open(plugin_json, "r", encoding="utf-8") as f:
                    plugin_config = json.load(f)
                    pid = plugin_config.get("id")
                    if pid and not pid.startswith("system"):
                        found.append(pid)
                        self.plugins[pid] = plugin_config
            except Exception as e:
                print(f"Error loading {plugin_json}: {e}")
        return found
    
    def register_plugin(self, plugin_id, plugin_config):
        """注册新插件"""
        self.plugins[plugin_id] = plugin_config
        self.save_registry()
        
    def save_registry(self):
        """保存插件注册表"""
        registry = {
            "version": "2.0",
            "last_scan": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "plugins": self.plugins
        }
        with open(self.registry_file, "w", encoding="utf-8") as f:
            json.dump(registry, f, ensure_ascii=False, indent=2)
            
    def get_active_plugins(self):
        """获取所有活跃插件"""
        active = {}
        for pid, config in self.plugins.items():
            if config.get("status") != "disabled":
                active[pid] = config
        return active
        
    def health_check(self):
        """检查所有插件健康状态"""
        results = {}
        for pid, config in self.plugins.items():
            last_update = config.get("last_run", "")
            status = config.get("status", "unknown")
            results[pid] = {
                "name": config.get("name", pid),
                "status": status,
                "last_update": last_update,
                "icon": config.get("icon", "📦")
            }
        return results
