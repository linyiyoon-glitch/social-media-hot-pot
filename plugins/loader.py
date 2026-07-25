import json
import os
from datetime import datetime

class PluginLoader:
    def __init__(self, plugins_dir="plugins"):
        self.plugins_dir = plugins_dir
        
    def load_plugin_data(self, plugin_id):
        """加载指定插件的数据"""
        data_file = os.path.join(self.plugins_dir, f"{plugin_id}_data.json")
        if not os.path.exists(data_file):
            return []
        with open(data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict) and "trends" in data:
                return data["trends"]
            elif isinstance(data, list):
                return data
        return []
        
    def load_all_plugin_data(self):
        """加载所有插件数据"""
        all_trends = []
        for fname in os.listdir(self.plugins_dir):
            if fname.endswith("_data.json") and not fname.startswith("registry"):
                pid = fname.replace("_data.json", "")
                trends = self.load_plugin_data(pid)
                for t in trends:
                    t["_plugin_source"] = pid
                all_trends.extend(trends)
        return all_trends
        
    def save_trend(self, plugin_id, trend_data):
        """保存趋势数据"""
        data_file = os.path.join(self.plugins_dir, f"{plugin_id}_data.json")
        existing = []
        if os.path.exists(data_file):
            with open(data_file, "r", encoding="utf-8") as f:
                existing = json.load(f)
        existing.append(trend_data)
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump({"trends": existing}, f, ensure_ascii=False, indent=2)
