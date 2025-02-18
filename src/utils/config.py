import os
import yaml

class Config:
    def __init__(self):
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        self.config_file = os.path.join(self.config_dir, 'config.yaml')
        self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
        if not os.path.exists(self.config_file):
            # 创建默认配置
            default_config = {
                'deepseek_api_key': '',
                'flux_api_key': '',
                'output_dir': 'output',
                'log_dir': 'logs'
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                yaml.dump(default_config, f, allow_unicode=True)
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置项"""
        self.config[key] = value
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True)