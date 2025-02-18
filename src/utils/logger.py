import os
import logging
from logging.handlers import RotatingFileHandler
from utils.config import Config

class Logger:
    _instance = None
    
    def __new__(cls, name='seo_article_generator'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_logger(name)
        return cls._instance
    
    def __init__(self, name='seo_article_generator'):
        self.config = Config()
        self.log_dir = self.config.get('log_dir', 'logs')
    
    def _setup_logger(self, name):
        """设置日志记录器"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        log_file = os.path.join(self.log_dir, f'{name}.log')
        
        # 创建日志记录器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 创建文件处理器
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """记录信息级别的日志"""
        self.logger.info(message)
    
    def error(self, message):
        """记录错误级别的日志"""
        self.logger.error(message)
    
    def warning(self, message):
        """记录警告级别的日志"""
        self.logger.warning(message)
    
    def debug(self, message):
        """记录调试级别的日志"""
        self.logger.debug(message)