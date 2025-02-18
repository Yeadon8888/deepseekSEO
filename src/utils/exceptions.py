class SEOGeneratorException(Exception):
    """基础异常类"""
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class APIError(SEOGeneratorException):
    """API调用相关错误"""
    pass

class ConfigError(SEOGeneratorException):
    """配置相关错误"""
    pass 