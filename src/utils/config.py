from typing import Optional
import os
import yaml
from pathlib import Path

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'config'):
            self.config_dir = Path(__file__).parent.parent.parent / 'config'
            self.config_file = self.config_dir / 'config.yaml'
            self._load_config()
            self._validate_config()
    
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
    
    def _validate_config(self):
        """验证必要的配置项"""
        required_keys = ['deepseek_api_key', 'flux_api_key']
        for key in required_keys:
            if not self.config.get(key):
                raise ValueError(f"配置项 {key} 不能为空")